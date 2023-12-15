import random
import time
import io
from PIL import Image

from telegram import Update, constants, LabeledPrice, InputMediaPhoto
from telegram.ext import CallbackContext

from AnnaDoncovaBackend.settings import YOOKASSA_TOKEN
from app.bot.constants import PARSE_MODE
from app.bot.features.chat import get_chat
from app.bot.features.face_swap_package import get_face_swap_package_by_user_id_and_name, update_face_swap_package
from app.bot.features.message import write_message, get_messages_by_chat_id
from app.bot.features.user import get_user, update_user
from app.bot.helpers import create_new_chat, create_new_message_and_update_user, handle_face_swap, send_images
from app.bot.integrations.openAI import get_response_message, get_response_image
from app.bot.integrations.replicateAI import get_face_swap_image
from app.bot.locales.main import get_localization
from app.bot.utilities import is_time_limit_exceeded, is_messages_limit_exceeded
from app.firebase import db, bucket
from app.models import Model, User, UserQuota, UserSettings, PackageType, Package, FaceSwapPackageName


async def handle_chatgpt(update: Update, user: User, user_quota: UserQuota):
    await write_message(user.current_chat_id, "user", user.id, update.message.text)

    chat = await get_chat(user.current_chat_id)
    messages = await get_messages_by_chat_id(user.current_chat_id)
    sorted_messages = sorted(messages, key=lambda m: m.created_at)
    history = [
                  {
                      'role': 'system',
                      'content': chat.role['description']
                  }
              ] + [
                  {
                      'role': message.sender,
                      'content': message.content
                  } for message in sorted_messages
              ]

    processing_message = await update.message.reply_text(
        text=get_localization(user.language_code).processing_request(),
        reply_to_message_id=update.message.message_id
    )

    await update.message.chat.send_action(action=constants.ChatAction.TYPING)

    try:
        response_message = get_response_message(user.current_model, history)

        # role, content = ["assistant", "Hello! How can I assist you today?"]
        role, content = response_message.role, response_message.content
        transaction = db.transaction()
        await create_new_message_and_update_user(transaction, role, content, user, user_quota)

        header_text = f'💬 {chat.title}\n\n' if user.settings[UserSettings.SHOW_NAME_OF_THE_CHAT] else ''
        footer_text = f'\n\n✉️ {user.monthly_limits[user_quota] + user.additional_usage_quota[user_quota] + 1}' \
            if user.settings[UserSettings.SHOW_USAGE_QUOTA] else ''
        await update.message.reply_text(
            f"{header_text}{content}{footer_text}",
            parse_mode=PARSE_MODE,
            reply_to_message_id=update.message.message_id,
        )
    except Exception as e:
        await update.message.reply_text(
            f"{get_localization(user.language_code).ERROR}: {e}\n\nPlease contact @roman_danilov",
            parse_mode=PARSE_MODE
        )
    finally:
        await processing_message.delete()


async def handle_dalle(update: Update, user: User, user_quota: UserQuota):
    processing_message = await update.message.reply_text(
        text=get_localization(user.language_code).processing_request(),
        reply_to_message_id=update.message.message_id
    )

    await update.message.chat.send_action(action=constants.ChatAction.UPLOAD_PHOTO)

    try:
        response_url = get_response_image(update.message.text)

        if user.monthly_limits[user_quota] > 0:
            user.monthly_limits[user_quota] -= 1
        else:
            user.additional_usage_quota[user_quota] -= 1
        await update_user(user.id, {
            "monthly_limits": user.monthly_limits,
            "additional_usage_quota": user.additional_usage_quota,
        })

        footer_text = f'\n\n✉️ {user.monthly_limits[user_quota] + user.additional_usage_quota[user_quota] + 1}' \
            if user.settings[UserSettings.SHOW_USAGE_QUOTA] else ''
        await update.message.reply_photo(
            caption=f"{get_localization(user.language_code).IMAGE_SUCCESS}{footer_text}",
            photo=response_url,
            parse_mode=PARSE_MODE,
            reply_to_message_id=update.message.message_id,
        )
    except Exception as e:
        await update.message.reply_text(
            f"{get_localization(user.language_code).ERROR}: {e}\n\nPlease contact @roman_danilov",
            parse_mode=PARSE_MODE
        )
    finally:
        await processing_message.delete()


async def handle_video(update: Update, context: CallbackContext):
    pass


async def handle_photo(update: Update, context: CallbackContext):
    user = await get_user(str(update.effective_user.id))

    if context.user_data.get('awaiting_photo', False):
        photo_file = await update.message.photo[-1].get_file()
        photo_data = bytes(await photo_file.download_as_bytearray())
        blob = bucket.blob(f"users/{user.id}.jpeg")
        blob.upload_from_string(photo_data, content_type='image/jpeg')
        context.user_data['awaiting_photo'] = False

        await handle_face_swap(update.message, context, user)


async def handle_message(update: Update, context: CallbackContext):
    if update.edited_message or not update.message or update.message.via_bot or update.message.text.startswith('/'):
        return

    user = await get_user(str(update.effective_user.id))

    try:
        if context.user_data.get('awaiting_quantity', False) and context.user_data.get('awaiting_package', False):
            package_type = context.user_data['awaiting_package']
            quantity = int(update.message.text)
            if ((package_type == PackageType.GPT3 and quantity < 50) or
                (package_type == PackageType.GPT4 and quantity < 50) or
                (package_type == PackageType.CHAT and quantity < 1) or
                (package_type == PackageType.DALLE3 and quantity < 10) or
                (package_type == PackageType.FACE_SWAP and quantity < 10)):
                await update.message.reply_text(
                    get_localization(user.language_code).MIN_ERROR,
                    parse_mode=PARSE_MODE,
                    reply_to_message_id=update.message.message_id,
                )
            else:
                price = Package.get_price(user.currency, package_type, quantity)
                name = ""
                description = ""
                if package_type == PackageType.GPT3:
                    name = get_localization(user.language_code).GPT3_REQUESTS
                    description = get_localization(user.language_code).GPT3_REQUESTS_DESCRIPTION
                elif package_type == PackageType.GPT4:
                    name = get_localization(user.language_code).GPT4_REQUESTS
                    description = get_localization(user.language_code).GPT4_REQUESTS_DESCRIPTION
                elif package_type == PackageType.CHAT:
                    name = get_localization(user.language_code).THEMATIC_CHATS
                    description = get_localization(user.language_code).THEMATIC_CHATS_DESCRIPTION
                elif package_type == PackageType.DALLE3:
                    name = get_localization(user.language_code).DALLE3_REQUESTS
                    description = get_localization(user.language_code).DALLE3_REQUESTS_DESCRIPTION
                elif package_type == PackageType.FACE_SWAP:
                    name = get_localization(user.language_code).FACE_SWAP_REQUESTS
                    description = get_localization(user.language_code).FACE_SWAP_REQUESTS_DESCRIPTION

                await update.message.reply_invoice(
                    title=f"{name} ({quantity})",
                    description=description,
                    payload=f"PACKAGE:{user.id}:{package_type}:{quantity}",
                    provider_token=YOOKASSA_TOKEN,
                    currency=f"{user.currency}",
                    prices=[LabeledPrice(label=name, amount=price * 100)],
                )

                context.user_data['awaiting_quantity'] = False
                context.user_data['awaiting_package'] = False
        elif (context.user_data.get('awaiting_quantity', False) and
              context.user_data.get('awaiting_face_swap_package', False)):
            quota = user.monthly_limits[UserQuota.FACE_SWAP] + user.additional_usage_quota[UserQuota.FACE_SWAP]
            quantity = int(update.message.text)
            name = context.user_data['face_swap_package_name']
            face_swap_package_quantity = len(getattr(FaceSwapPackageName, name)[f"{user.gender}_files"])

            if quota < quantity:
                await update.message.reply_text(
                    text=get_localization(user.language_code).face_swap_package_forbidden(quota),
                    parse_mode=PARSE_MODE
                )
            elif quantity < 1:
                await update.message.reply_text(
                    text=get_localization(user.language_code).FACE_SWAP_MIN_ERROR,
                    parse_mode=PARSE_MODE
                )
            elif face_swap_package_quantity < quantity:
                await update.message.reply_text(
                    text=get_localization(user.language_code).FACE_SWAP_MAX_ERROR,
                    parse_mode=PARSE_MODE
                )
            else:
                user_photo = bucket.blob(f'users/{user.id}.jpeg')
                user_photo.make_public()
                user_photo_link = user_photo.public_url
                face_swap_package = await get_face_swap_package_by_user_id_and_name(user.id, name)
                files = getattr(FaceSwapPackageName, name)[f"{user.gender}_files"]
                images = []
                for _ in range(quantity):
                    random_image_name = random.choice(files)
                    while random_image_name in face_swap_package.used_images:
                        random_image_name = random.choice(files)
                    random_image = bucket.blob(
                        f'face_swap/{user.gender.lower()}/{face_swap_package.name.lower()}/{random_image_name}')
                    random_image.make_public()
                    face_swap_package.used_images.append(random_image_name)
                    image_link = random_image.public_url
                    image_data = random_image.download_as_bytes()
                    image = Image.open(io.BytesIO(image_data))

                    width, height = image.size

                    face_swap_image = get_face_swap_image(width, height, image_link, user_photo_link)
                    images.append(face_swap_image)

                await send_images(update.message, images)

                quantity_to_delete = len(images)
                while user.monthly_limits[UserQuota.FACE_SWAP] > 0 and quantity_to_delete > 0:
                    user.monthly_limits[UserQuota.FACE_SWAP] -= 1
                while user.additional_usage_quota[UserQuota.FACE_SWAP] and quantity_to_delete > 0:
                    user.additional_usage_quota[UserQuota.FACE_SWAP] -= 1

                user_photo.make_private()
                await update_user(user.id, {
                    "monthly_limits": user.monthly_limits,
                    "additional_usage_quota": user.additional_usage_quota,
                })
                await update_face_swap_package(face_swap_package.id, {
                    "used_images": face_swap_package.used_images
                })
                context.user_data['awaiting_quantity'] = False
                context.user_data['awaiting_face_swap_package'] = False
    except ValueError:
        await update.message.reply_text(
            get_localization(user.language_code).VALUE_ERROR,
            parse_mode=PARSE_MODE,
            reply_to_message_id=update.message.message_id,
        )

    if context.user_data.get('awaiting_chat', False):
        transaction = db.transaction()
        await create_new_chat(transaction, user, str(update.message.chat_id))

        context.user_data['awaiting_chat'] = False

    current_time = time.time()

    if user.current_model == Model.GPT3:
        user_quota = UserQuota.GPT3
    elif user.current_model == Model.GPT4:
        user_quota = UserQuota.GPT4
    elif user.current_model == Model.DALLE3:
        user_quota = UserQuota.DALLE3
    elif user.current_model == Model.Face_Swap:
        user_quota = UserQuota.FACE_SWAP
    else:
        return
    need_exit = await is_time_limit_exceeded(update, context, user, current_time) or \
                await is_messages_limit_exceeded(update, user, user_quota)
    if need_exit:
        return
    context.user_data['last_request_time'] = current_time

    if user.current_model == Model.GPT3 or user.current_model == Model.GPT4:
        await handle_chatgpt(update, user, user_quota)
    elif user.current_model == Model.DALLE3:
        await handle_dalle(update, user, user_quota)
    elif user.current_model == Model.Face_Swap and not context.user_data.get('awaiting_face_swap_package', False):
        await handle_face_swap(update.message, context, user)
