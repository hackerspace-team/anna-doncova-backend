import random
import time
import io
from datetime import datetime, timezone

from PIL import Image

from telegram import Update, constants, LabeledPrice
from telegram.ext import CallbackContext

from AnnaDoncovaBackend.settings import YOOKASSA_TOKEN
from app.bot.constants import PARSE_MODE
from app.bot.features.chat import get_chat
from app.bot.features.face_swap_package import get_face_swap_package_by_user_id_and_name, update_face_swap_package
from app.bot.features.feedback import write_feedback
from app.bot.features.message import write_message, get_messages_by_chat_id
from app.bot.features.promo_code import get_promo_code_by_name, write_promo_code, \
    get_used_promo_code_by_user_id_and_promo_code_id, write_used_promo_code
from app.bot.features.subscription import write_subscription
from app.bot.features.transaction import write_transaction
from app.bot.features.user import get_user, update_user
from app.bot.helpers import create_new_chat, create_new_message_and_update_user, handle_face_swap, send_images, \
    send_message_to_admins, create_subscription, process_voice_message, reply_with_voice
from app.bot.integrations.openAI import get_response_message, get_response_image
from app.bot.integrations.replicateAI import get_face_swap_image
from app.bot.keyboards import build_promo_code_admin_date_keyboard, build_chat_gpt_continue_generating_keyboard
from app.bot.locales.main import get_localization, language_codes
from app.bot.utilities import is_time_limit_exceeded, is_messages_limit_exceeded, is_awaiting_something
from app.firebase import db, bucket
from app.models.common import Model, Currency
from app.models.face_swap_package import FaceSwapPackageName
from app.models.package import PackageType, Package
from app.models.promo_code import PromoCodeType
from app.models.subscription import SubscriptionType, SubscriptionStatus
from app.models.transaction import TransactionType, ServiceType
from app.models.user import User, UserQuota, UserSettings


async def handle_chatgpt(update: Update, context: CallbackContext, user: User, user_quota: UserQuota):
    text = context.user_data.get('recognized_text', None)
    if text is None:
        text = update.message.text

    await write_message(user.current_chat_id, "user", user.id, text)

    chat = await get_chat(user.current_chat_id)
    messages = await get_messages_by_chat_id(user.current_chat_id)
    sorted_messages = sorted(messages, key=lambda m: m.created_at)
    history = [
                  {
                      'role': 'system',
                      'content': getattr(get_localization(user.language_code), chat.role)["instruction"]
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

    if user.settings[UserSettings.TURN_ON_VOICE_MESSAGES]:
        await update.message.chat.send_action(action=constants.ChatAction.RECORD_VOICE)
    else:
        await update.message.chat.send_action(action=constants.ChatAction.TYPING)

    try:
        response = await get_response_message(user.current_model, history)
        message = response['message']
        if user_quota == UserQuota.GPT3:
            service = ServiceType.GPT3
            input_price = response['input_tokens'] * 0.000001
            output_price = response['output_tokens'] * 0.000002
        elif user_quota == UserQuota.GPT4:
            service = ServiceType.GPT4
            input_price = response['input_tokens'] * 0.00001
            output_price = response['output_tokens'] * 0.00003
        else:
            raise NotImplemented

        total_price = round(input_price + output_price, 6)
        await write_transaction(user_id=user.id,
                                type=TransactionType.EXPENSE,
                                service=service,
                                amount=total_price,
                                currency=Currency.USD,
                                quantity=1)

        role, content = message.role, message.content
        transaction = db.transaction()
        await create_new_message_and_update_user(transaction, role, content, user, user_quota)

        if user.settings[UserSettings.TURN_ON_VOICE_MESSAGES]:
            reply_markup = build_chat_gpt_continue_generating_keyboard(user.language_code)
            await reply_with_voice(update,
                                   content,
                                   user.id,
                                   reply_markup if response['finish_reason'] == 'length' else None)
        else:
            header_text = f'💬 {chat.title}\n\n' if user.settings[UserSettings.SHOW_NAME_OF_THE_CHAT] else ''
            footer_text = f'\n\n✉️ {user.monthly_limits[user_quota] + user.additional_usage_quota[user_quota] + 1}' \
                if user.settings[UserSettings.SHOW_USAGE_QUOTA] else ''
            reply_markup = build_chat_gpt_continue_generating_keyboard(user.language_code)
            await update.message.reply_text(
                f"{header_text}{content}{footer_text}",
                parse_mode=PARSE_MODE,
                reply_markup=reply_markup if response['finish_reason'] == 'length' else None,
                reply_to_message_id=update.message.message_id,
            )
    except Exception as e:
        await update.message.reply_text(
            f"{get_localization(user.language_code).ERROR}: {e}\n\nPlease contact @roman_danilov",
            parse_mode=PARSE_MODE
        )
    finally:
        await processing_message.delete()


async def handle_dalle(update: Update, context: CallbackContext, user: User, user_quota: UserQuota):
    text = context.user_data.get('recognized_text', None)
    if text is None:
        text = update.message.text

    processing_message = await update.message.reply_text(
        text=get_localization(user.language_code).processing_request(),
        reply_to_message_id=update.message.message_id
    )

    await update.message.chat.send_action(action=constants.ChatAction.UPLOAD_PHOTO)

    try:
        response_url = await get_response_image(text)

        if user.monthly_limits[user_quota] > 0:
            user.monthly_limits[user_quota] -= 1
        else:
            user.additional_usage_quota[user_quota] -= 1

        await update_user(user.id, {
            "monthly_limits": user.monthly_limits,
            "additional_usage_quota": user.additional_usage_quota,
        })
        await write_transaction(user_id=user.id,
                                type=TransactionType.EXPENSE,
                                service=ServiceType.DALLE3,
                                amount=0.040,
                                currency=Currency.USD,
                                quantity=1)

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


async def handle_voice(update: Update, context: CallbackContext):
    user = await get_user(str(update.effective_user.id))

    if user.additional_usage_quota[UserQuota.VOICE_MESSAGES]:
        voice_file = await update.message.voice.get_file()

        text = await process_voice_message(voice_file.file_path, user.id)

        context.user_data['recognized_text'] = text
        await handle_message(update, context)
        context.user_data['recognized_text'] = None
    else:
        await update.message.reply_text(text=get_localization(user.language_code).VOICE_MESSAGES_FORBIDDEN,
                                        parse_mode=PARSE_MODE)


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
    text = context.user_data.get('recognized_text', None)
    if text is None:
        text = update.message.text

    if update.edited_message or not update.message or update.message.via_bot or text.startswith('/'):
        return

    user = await get_user(str(update.effective_user.id))

    try:
        if context.user_data.get('awaiting_quantity', False) and context.user_data.get('awaiting_package', False):
            package_type = context.user_data['awaiting_package']
            quantity = int(text)
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
            quantity = int(text)
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
                await update.message.chat.send_action(action=constants.ChatAction.UPLOAD_PHOTO)

                user_photo = bucket.blob(f'users/{user.id}.jpeg')
                user_photo.make_public()
                user_photo_link = user_photo.public_url
                face_swap_package = await get_face_swap_package_by_user_id_and_name(user.id, name)
                files = getattr(FaceSwapPackageName, name)[f"{user.gender}_files"]
                images = []
                for _ in range(quantity):
                    random_image_name = random.choice(files)
                    while random_image_name in face_swap_package.used_images[user.gender]:
                        random_image_name = random.choice(files)
                    face_swap_package.used_images[user.gender].append(random_image_name)

                    random_image = bucket.blob(
                        f'face_swap/{user.gender.lower()}/{face_swap_package.name.lower()}/{random_image_name}')
                    random_image.make_public()
                    image_link = random_image.public_url
                    image_data = random_image.download_as_bytes()
                    image = Image.open(io.BytesIO(image_data))

                    width, height = image.size

                    face_swap_response = await get_face_swap_image(width, height, image_link, user_photo_link)
                    images.append(face_swap_response['image'])

                    await write_transaction(user_id=user.id,
                                            type=TransactionType.EXPENSE,
                                            service=ServiceType.FACE_SWAP,
                                            amount=round(0.000225 * face_swap_response['seconds'], 6),
                                            currency=Currency.USD,
                                            quantity=1)

                await send_images(update.message, images)

                quantity_to_delete = len(images)
                user.monthly_limits[UserQuota.FACE_SWAP] = max(
                    user.monthly_limits[UserQuota.FACE_SWAP] - quantity_to_delete,
                    0
                )
                user.additional_usage_quota[UserQuota.FACE_SWAP] = max(
                    user.additional_usage_quota[UserQuota.FACE_SWAP] - quantity_to_delete,
                    0
                )

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
            text=get_localization(user.language_code).VALUE_ERROR,
            parse_mode=PARSE_MODE,
            reply_to_message_id=update.message.message_id,
        )

    if context.user_data.get('awaiting_chat', False):
        transaction = db.transaction()
        await create_new_chat(transaction, user, str(update.message.chat_id), update.message.text)

        context.user_data['awaiting_chat'] = False
    elif context.user_data.get('awaiting_feedback', False):
        await write_feedback(user.id, text)
        message = (f"#feedback\n\n"
                   f"🚀 Новая обратная связь от пользователя: {user.id} 🚀\n\n"
                   f"{text}")
        await send_message_to_admins(update.get_bot(), message)
        context.user_data['awaiting_feedback'] = False

        await update.message.reply_text(
            text=get_localization(user.language_code).FEEDBACK_SUCCESS,
            parse_mode=PARSE_MODE,
            reply_to_message_id=update.message.message_id,
        )
    elif context.user_data.get('awaiting_promo_code', False):
        promo_code_name = text
        promo_code = await get_promo_code_by_name(promo_code_name)
        if promo_code:
            current_date = datetime.now(timezone.utc)
            if current_date <= promo_code.until:
                used_promo_code = await get_used_promo_code_by_user_id_and_promo_code_id(user.id, promo_code.id)
                if used_promo_code:
                    await update.message.reply_text(
                        text=get_localization(user.language_code).PROMO_CODE_ALREADY_USED_ERROR,
                        parse_mode=PARSE_MODE,
                        reply_to_message_id=update.message.message_id,
                    )
                else:
                    if promo_code.type == PromoCodeType.SUBSCRIPTION:
                        if user.subscription_type == SubscriptionType.FREE:
                            subscription = await write_subscription(user.id,
                                                                    promo_code.details['subscription_type'],
                                                                    promo_code.details['subscription_period'],
                                                                    SubscriptionStatus.WAITING,
                                                                    user.currency,
                                                                    0)

                            transaction = db.transaction()
                            await create_subscription(transaction,
                                                      subscription.id,
                                                      subscription.user_id,
                                                      "")
                        else:
                            await update.message.reply_text(
                                text="Нельзя, уже есть подписочка",
                                parse_mode=PARSE_MODE,
                                reply_to_message_id=update.message.message_id,
                            )
                    await write_used_promo_code(user.id, promo_code.id)
                    await update.message.reply_text(
                        text=get_localization(user.language_code).PROMO_CODE_SUCCESS,
                        parse_mode=PARSE_MODE,
                        reply_to_message_id=update.message.message_id,
                    )
            else:
                await update.message.reply_text(
                    text=get_localization(user.language_code).PROMO_CODE_EXPIRED_ERROR,
                    parse_mode=PARSE_MODE,
                    reply_to_message_id=update.message.message_id,
                )
        else:
            await update.message.reply_text(
                text=get_localization(user.language_code).PROMO_CODE_NOT_FOUND_ERROR,
                parse_mode=PARSE_MODE,
                reply_to_message_id=update.message.message_id,
            )
    elif context.user_data.get('awaiting_promo_code_name', False):
        promo_code_name = text.upper()
        promo_code = await get_promo_code_by_name(promo_code_name)
        if promo_code:
            await update.message.reply_text(
                text=get_localization(user.language_code).PROMO_CODE_NAME_EXISTS_ERROR,
                parse_mode=PARSE_MODE,
                reply_to_message_id=update.message.message_id,
            )
        else:
            context.user_data['promo_code_name'] = promo_code_name
            context.user_data['awaiting_promo_code_name'] = False
            context.user_data['awaiting_promo_code_date'] = True
            reply_markup = build_promo_code_admin_date_keyboard(user.language_code)
            await update.message.reply_text(
                text=get_localization(user.language_code).PROMO_CODE_CHOOSE_DATE,
                reply_markup=reply_markup,
                parse_mode=PARSE_MODE,
                reply_to_message_id=update.message.message_id,
            )
    elif context.user_data.get('awaiting_promo_code_date', False):
        try:
            promo_code_until_date = datetime.strptime(text, "%d.%m.%Y")
            promo_code_name = context.user_data['promo_code_name']
            promo_code_type = context.user_data['promo_code_type']
            details = {}
            if context.user_data['promo_code_type'] == PromoCodeType.SUBSCRIPTION:
                details['subscription_type'] = context.user_data['promo_code_subscription_type']
                details['subscription_period'] = context.user_data['promo_code_subscription_period']
            # elif context.user_data['promo_code_type'] == PromoCodeType.PACKAGE:
            #     pass

            await write_promo_code(
                created_by_user_id=user.id,
                name=promo_code_name,
                type=promo_code_type,
                details=details,
                until=promo_code_until_date
            )
            await update.message.reply_text(
                text=get_localization(user.language_code).PROMO_CODE_SUCCESS_ADMIN,
                parse_mode=PARSE_MODE
            )

            context.user_data['awaiting_promo_code_date'] = False
            context.user_data['promo_code_name'] = False
            context.user_data['promo_code_type'] = False
            context.user_data['promo_code_subscription_type'] = False
            context.user_data['promo_code_subscription_period'] = False
        except ValueError:
            await update.message.reply_text(
                text=get_localization(user.language_code).PROMO_CODE_DATE_VALUE_ERROR,
                parse_mode=PARSE_MODE,
                reply_to_message_id=update.message.message_id
            )

    current_time = time.time()

    if user.current_model == Model.GPT3:
        user_quota = UserQuota.GPT3
    elif user.current_model == Model.GPT4:
        user_quota = UserQuota.GPT4
    elif user.current_model == Model.DALLE3:
        user_quota = UserQuota.DALLE3
    elif user.current_model == Model.FACE_SWAP:
        user_quota = UserQuota.FACE_SWAP
    else:
        return
    need_exit = await is_time_limit_exceeded(update, context, user, current_time) or \
                await is_messages_limit_exceeded(update, user, user_quota) or \
                is_awaiting_something(context)
    if need_exit:
        return
    context.user_data['last_request_time'] = current_time

    if user.current_model == Model.GPT3 or user.current_model == Model.GPT4:
        await handle_chatgpt(update, context, user, user_quota)
    elif user.current_model == Model.DALLE3:
        await handle_dalle(update, context, user, user_quota)
    elif user.current_model == Model.FACE_SWAP and not context.user_data.get('awaiting_face_swap_package', False):
        await handle_face_swap(update.message, context, user)
