import random
import re

from app.bot.locales.texts import Texts
from app.models import User, SubscriptionType, UserQuota, UserGender, Currency, SubscriptionPeriod, Subscription, \
    PackageType


class English(Texts):
    START = """
🤖 Welcome to the future of AI with GPTsTurboBot 🎉

The bot allows you to access AI and neural networks.
Embark on a journey through the realms of AI with:
✉️ Unlimited ChatGPT 3 queries... Well, almost! Check out our 'Free' tier
🧠 The wisdom of ChatGPT 4, if you're feeling extra brainy today
🎨 Artistic creations with DALL-E 3 that will make Picasso look twice
😜 And, ever wanted to swap faces with Mona Lisa? Just ask for our Face Swap feature

Here's a quick guide to get you started:
✉️ To get a text response, simply type your request into the chat
🌅 To generate an image, first choose your AI model in /mode, then let your imagination run wild!
🔄 Swap between different neural networks with /mode to suit your creative needs
🔍 Use /info to learn more about what each AI model can do
👁️‍🗨️ Dive into /catalog to pick a specialized assistant tailored to your tasks
📊 Check your usage and subscription details with /profile
🔧 Personalize your experience further in /settings

And there's more! Just tap /commands to see all the magical AI commands at your disposal.
Let AI be your co-pilot in this adventure! 🚀
"""
    COMMANDS = """
🤖 Here's what you can explore:

🚀 /start - *About me*
🌐 /language - Engage with any language, ***set system messages*.
🧠 /mode - *Swap neural network models* on the fly with — *ChatGPT3*, *ChatGPT4*, *DALLE-3*, or *Face Swap*!
📜 /info - Curious about what each model can do? Here you'll find all the answers.
💼 /profile - *Check your profile* to see your usage quota and more.
🔧 /settings - *Customize your experience* for a seamless user experience.
💳 /subscribe or /buy - *Learn about our plans and perks* or opt for individual packages.
🎭 /catalog - *Pick a specialized assistant* for tasks tailored just for you.
💬 /chats - *Create, switch, or delete context-specific chats*.

Just type away or use a command to begin your AI journey! 🌟
"""
    LANGUAGE = "Language:"
    CHOOSE_LANGUAGE = "Selected language: English 🇺🇸"

    # AI
    MODE = "Mode:"
    INFO = """
🤖 Let's check out what each model can do for you:

✉️ *ChatGPT3: The Versatile Communicator*
- _Small Talk to Deep Conversations_: Ideal for chatting about anything from daily life to sharing jokes.
- _Educational Assistant_: Get help with homework, language learning, or complex topics like coding.
- _Personal Coach_: Get motivation, fitness tips, or even meditation guidance.
- _Creative Writer_: Need a post, story, or even a song? ChatGPT3 can whip it up in seconds.
- _Travel Buddy_: Ask for travel tips, local cuisines, or historical facts about your next destination.
- _Business Helper_: Draft emails, create business plans, or brainstorm marketing ideas.
- _Role Play_: Engage in creative role-playing scenarios for entertainment or storytelling.
- _Quick Summaries_: Summarize long articles or reports into concise text.

🧠 *ChatGPT4: The Advanced Intellect*
- _In-Depth Analysis_: Perfect for detailed research, technical explanations, or exploring hypothetical scenarios.
- _Problem Solver_: Get help with advanced math problems, programming bugs, or scientific queries.
- _Language Expert_: Translate complex texts or practice conversational skills in various languages.
- _Creative Consultant_: Develop plot ideas for your posts, script dialogues, or explore artistic concepts.
- _Health and Wellness_: Discuss wellness and mental health topics in-depth.
- _Personalized Recommendations_: Get book, movie, or travel recommendations based on your interests.

🎨 *DALLE-3: The Creative Genius*
- _Art on Demand_: Generate unique art from descriptions – perfect for illustrators or those seeking inspiration.
- _Ad Creator_: Produce eye-catching images for advertising or social media content.
- _Educational Tool_: Visualize complex concepts for better understanding in education.
- _Interior Design_: Get ideas for room layouts or decoration themes.
- _Fashion Design_: Create clothing designs or fashion illustrations.
- _Personalized Comics_: Create comic strips or cartoon characters from your stories.
- _Product Mockups_: Create mockups for product ideas or inventions.

🤡 *Face Swap: The Entertainment Master*
- _Fun Reimaginations_: See how you'd look in different historical eras or as various movie characters.
- _Personalized Greetings_: Create unique birthday cards or invitations with personalized images.
- _Role Play_: Experiment with different looks for role-playing games or virtual meetings.
- _Memes and Content Creation_: Spice up your social media with funny or imaginative face-swapped pictures.
- _Digital Makeovers_: Experiment with new haircuts or makeup styles.
- _Celebrity Mashups_: Combine your face with celebrities for fun comparisons.

To change a model use /mode 😉
"""
    ALREADY_MAKE_REQUEST = "You've already made a request. Please wait ⚠️"
    READY_FOR_NEW_REQUEST = "You can ask the next request 😌"
    IMAGE_SUCCESS = """
✨ Here's your image creation! 🎨
"""

    # Settings
    SETTINGS = "Settings:"
    SHOW_NAME_OF_THE_CHAT = "Show name of the chat"
    SHOW_USAGE_QUOTA_IN_MESSAGES = "Show usage quota in messages"
    TURN_ON_VOICE_MESSAGES_FROM_RESPONDS = "Turn on voice messages from responds"

    # Subscription
    MONTH_1 = "1 month"
    MONTHS_3 = "3 months"
    MONTHS_6 = "6 months"
    DISCOUNT = "Discount"
    NO_DISCOUNT = "No discount"
    SUBSCRIPTION_SUCCESS = """
🎉 Hooray! You're All Set! 🚀

Your subscription is now as active as a caffeinated squirrel! 🐿️☕ Welcome to the club of awesomeness. Here's what's going to happen next:
- A world of possibilities just opened up. 🌍✨
- Your AI pals are gearing up to assist you. 🤖👍
- Get ready to dive into a sea of features and fun. 🌊🎉

Thank you for embarking on this fantastic journey with us! Let's make some magic happen! 🪄🌟
"""

    # Package
    GPT3_REQUESTS = "✉️ GPT3 requests"
    GPT3_REQUESTS_DESCRIPTION = "Unleash the power of GPT 3 for witty chats, smart advice, and endless fun! 🤖✨"
    GPT4_REQUESTS = "🧠 GPT4 requests"
    GPT4_REQUESTS_DESCRIPTION = "Experience GPT4's advanced intelligence for deeper insights and groundbreaking conversations. 🧠🌟"
    THEMATIC_CHATS = "💬 Thematic chats"
    THEMATIC_CHATS_DESCRIPTION = "Turn ideas into art with DALLE3 – where your imagination becomes stunning visual reality! 🎨🌈"
    DALLE3_REQUESTS = "🖼 DALLE3 images"
    DALLE3_REQUESTS_DESCRIPTION = "Dive into topics you love with Thematic Chats, guided by AI in a world of tailored discussions. 📚🗨️"
    FACE_SWAP_REQUESTS = "📷 Images with face replacement"
    FACE_SWAP_REQUESTS_DESCRIPTION = "Enter the playful world of Face Swap for laughs and surprises in every image! 😂🔄"
    ACCESS_TO_CATALOG = "🎭 Access to a roles catalog"
    ACCESS_TO_CATALOG_DESCRIPTION = "Unlock a universe of specialized AI assistants with access to our exclusive catalog, where every role is tailored to fit your unique needs and tasks"
    ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES = "🎙 Answers and requests with voice messages"
    ANSWERS_AND_REQUESTS_WITH_VOICE_MESSAGES_DESCRIPTION = "Experience the ease and convenience of voice communication with our AI: Send and receive voice messages for a more dynamic and expressive interaction"
    FAST_ANSWERS = "⚡ Fast answers"
    FAST_ANSWERS_DESCRIPTION = "Quick Messages feature offers lightning-fast, accurate AI responses, ensuring you're always a step ahead in communication"
    MIN_ERROR = "Oops! It looks like the number entered is below our minimum threshold. Please enter a value that meets or exceeds the minimum required. Let's try that again! 🔄"
    VALUE_ERROR = "Whoops! That doesn't seem like a number. 🤔 Could you please enter a numeric value? Let's give it another go! 🔢"
    PACKAGE_SUCCESS = """
🎉 Cha-Ching! Payment Success! 💳

Your payment just zoomed through like a superhero! 🦸‍ You've successfully unlocked the awesome power of your chosen package. Get ready for a rollercoaster of AI fun and excitement! 🎢

Remember, with great power comes great... well, you know how it goes. Let's make some magic happen! ✨🪄
"""

    # Catalog
    CATALOG = """
🎭 Step Right Up to Our Role Catalogue Extravaganza! 🌟

Ever dreamt of having an AI sidekick specialized just for you? Our catalog is like a magical wardrobe, each role a unique outfit tailored for your adventures in AI land! 🧙‍♂️✨

Choose from an array of AI personas, each with its own flair and expertise. Whether you need a brainstorm buddy, a creative muse, or a factual wizard, we've got them all!

👉 Ready to meet your match? Just hit the button below and let the magic begin! 🎩👇
"""
    CATALOG_FORBIDDEN_ERROR = """
🔒 Whoops! Looks like you've hit a VIP-only zone! 🌟

You're just a click away from unlocking our treasure trove of AI roles, but it seems you don't have the golden key yet. No worries, though! You can grab it easily.

🚀 Head over to /subscribe for some fantastic subscription options, or check out /buy if you're in the mood for some a la carte AI delights.

Once you're all set up, our catalog of AI wonders will be waiting for you – your ticket to an extraordinary world of AI possibilities! 🎫✨
"""
    PERSONAL_ASSISTANT = "🤖 Personal assistant"
    CREATIVE_WRITER = "🖋️ Creative writer"
    LANGUAGE_TUTOR = "🗣️ Language tutor"
    TECHNICAL_ADVISOR = "💻 Technical advisor"

    # Chats
    SHOW_CHATS = "Show chats"
    CREATE_CHAT = "Create a new chat"
    CREATE_CHAT_FORBIDDEN = """
🚫 Oops!

Looks like you've hit the limit for creating new chats. But don't worry, the world of endless chats is just a click away! 🌍✨

Head over to /subscribe or /buy to unlock the power of multiple chats. More chats, more fun! 🎉
"""
    TYPE_CHAT_NAME = "Type your chat name"
    SWITCH_CHAT = "Switch between chats"
    SWITCH_CHAT_FORBIDDEN = """
"🔄 Switching Gears? Hold That Thought! ⚙️

You're currently in your one and only chat universe. It's a cozy place, but why not expand your horizons? 🌌

To hop between multiple thematic chats, just get your pass from /subscribe or /buy. Let the chat-hopping begin! 🐇
"""
    DELETE_CHAT = "Delete a chat"
    DELETE_CHAT_FORBIDDEN = """
🗑️ Delete This Chat? That's Lonely Talk! 💬

This is your sole chat kingdom, and a kingdom needs its king or queen! Deleting it would be like canceling your own party. 🎈

How about adding more chats to your realm instead? Check out /subscribe or /buy to build your chat empire! 👑
"""
    DELETE_CHAT_SUCCESS = "🗑️ Chat Successfully Deleted! 🎉"

    # Face swap
    TELL_ME_YOUR_GENDER = "Tell me your gender:"
    YOUR_GENDER = "Your gender:"
    MALE = "Male 🚹"
    FEMALE = "Female 🚺"
    SEND_ME_YOUR_PICTURE = """
📸 *Ready for a Photo Transformation? Here's How to Get Started!*

👍 *Ideal Photo Guidelines*:
- Clear, high-quality selfie.
- Only one person should be in the selfie.

👎 *Please Avoid These Types of Photos*:
- Group photos.
- Animals.
- Children under 18 years.
- Full body shots.
- Nude or inappropriate images.
- Sunglasses or any face-obscuring items.
- Blurry, out-of-focus images.
- Videos and animations.
- Compressed or altered images.

Once you've got the perfect shot, upload your photo and let the magic happen 🌟
"""
    CHOOSE_YOUR_PACKAGE = """
🌟*Let's Get Creative with Your Photos!*

*First step:* Choose Your Adventure! 🚀

Ready? Let's dive into a world of imagination! 🌈 Just *select a package below* and start your photo adventure 👇
    """
    CELEBRITIES = "Celebrities ⭐️"
    FACE_SWAP_MIN_ERROR = """
🤨 *Hold on there, partner!*

Looks like you're trying to request fewer than 1 image. In the world of creativity, we need at least 1 to get the ball rolling!

🌟 *Tip*: Type a number greater than 0 to start the magic. Let's unleash those creative ideas!
"""
    FACE_SWAP_MAX_ERROR = """
🚀 *Whoa, aiming high, I see!* But, uh-oh...

You're asking for more images than we have.

🧐 *How about this?* Let's try a number within the package limit!
"""

    ERROR = "I've got an error"
    BACK = "Back ◀️"
    CLOSE = "Close 🚪"
    EXIT = "Exit ❌"

    @staticmethod
    def profile(subscription_type: SubscriptionType,
                gender: UserGender,
                current_model: str,
                monthly_limits,
                additional_usage_quota) -> str:
        emojis = Subscription.get_emojis()

        quotas = User.get_quotas(monthly_limits, additional_usage_quota)
        gender_info = ""
        if gender == UserGender.MALE:
            gender_info = "Gender: Male 👕"
        elif gender == UserGender.FEMALE:
            gender_info = "Gender: Female 👚"

        return f"""
Profile 👤

Subscription type: {subscription_type} {emojis[subscription_type]}
{gender_info}
Current model: {current_model}
Change model: /mode

GPT-3.5 requests for month: {quotas[UserQuota.GPT3]}/{User.DEFAULT_MONTHLY_LIMITS[subscription_type][UserQuota.GPT3]}
GPT-4.0 requests for month: {quotas[UserQuota.GPT4]}/{User.DEFAULT_MONTHLY_LIMITS[subscription_type][UserQuota.GPT4]}
Additional chats: {quotas[UserQuota.ADDITIONAL_CHATS]}
DALL-E 3 images for month: {quotas[UserQuota.DALLE3]}/{User.DEFAULT_MONTHLY_LIMITS[subscription_type][UserQuota.DALLE3]}
Face swap images for month: {quotas[UserQuota.FACE_SWAP]}/{User.DEFAULT_MONTHLY_LIMITS[subscription_type][UserQuota.FACE_SWAP]}
Subscribe: /subscribe
Buy additional requests: /buy
"""

    @staticmethod
    def subscribe(currency: Currency):
        prices = Subscription.get_prices(currency)

        return f"""
🤖Ready to supercharge your digital journey? Here's what's on the menu:

- *Standard* ⭐: For just {prices[SubscriptionType.STANDARD]}, step into the AI playground! Perfect for daily musings, creative bursts, and those "just curious" moments. Chat up a storm with ChatGPT 3, conjure images from thin air with DALLE-3, and swap faces faster than you can say "cheese"! 🧀

- *VIP* 🔥: Got grander ambitions? {prices[SubscriptionType.VIP]} unlocks deeper dialogues, more complex image creation, and access to a wider array of digital personas. It's the power user's delight, offering a premium lane on the AI highway. 🛣️

- *Platinum* 💎: For the connoisseurs, {prices[SubscriptionType.PLATINUM]} grants you the keys to the AI kingdom! Max out on ChatGPT 4 prompts, create thematic chat rooms, and get exclusive access to the latest AI innovations. It's all you can AI, and then some! 🍽️

Pick your potion and hit the button below to subscribe:
"""

    @staticmethod
    def choose_how_many_months_to_subscribe(subscription_type: SubscriptionType):
        emojis = Subscription.get_emojis()

        return f"""
You're choosing *{subscription_type}* {emojis[subscription_type]}

Please select the subscription period by clicking on the button:
"""

    @staticmethod
    def cycles_subscribe():
        return {
            SubscriptionPeriod.MONTH1: English.MONTH_1,
            SubscriptionPeriod.MONTHS3: English.MONTHS_3,
            SubscriptionPeriod.MONTHS6: English.MONTHS_6,
        }

    @staticmethod
    def confirmation_subscribe(subscription_type: SubscriptionType, subscription_period: SubscriptionPeriod):
        cycles = English.cycles_subscribe()

        return f"You're about to activate your subscription for {cycles[subscription_period]}."

    # Package
    @staticmethod
    def buy():
        return """
🤖 Welcome to the AI Shopping Spree! 🛍

Welcome to the shop zone, where each button tap unlocks a world of AI wonders!
🧠 *ChatGPT3 & ChatGPT4*: Engage in deep, thought-provoking conversations. Your new AI buddies await!
🎨 *DALLE-3 Magic*: Transform ideas into stunning visuals. It's like painting with AI!
👤 *Face Swap Fun*: Play with identities in images. It's never been this exciting!
🗣️ *Voice Messages*: Say it out loud! Chatting with AI has never sounded better.
💬 *Thematic Chats*: Dive into specialized topics and explore dedicated chat realms.
🎭 *Role Catalog Access*: Need a specific assistant? Browse our collection and find your perfect AI match.
⚡ *Quick Messages*: Fast, efficient, and always on point. AI communication at lightning speed.

Hit a button and embark on an extraordinary journey with AI! It's time to redefine what's possible. 🌌🛍️
"""

    @staticmethod
    def choose_min(package_type: PackageType):
        return f"""
🚀 Fantastic!

You've selected the {package_type} package
🌟 Please type in the number of requests you'd like to go for
"""

    # Chats
    @staticmethod
    def chats(current_chat_name: str, total_chats: int, available_to_create_chats: int):
        return f"""
🗨️ *Current Chat: {current_chat_name}* 🌟

Welcome to the dynamic world of AI-powered chats! Here's what you can do:

- Create New Thematic Chats: Immerse yourself in focused discussions tailored to your interests.
- Switch Between Chats: Effortlessly navigate through your different chat landscapes.
- Delete Chats: Clean up by removing the chats you no longer need.

📈 Total Chats: *{total_chats}* | Chats Available to Create: *{available_to_create_chats}*

Ready to tailor your chat experience? Explore the options below and let the conversations begin! 🚀👇
"""

    # Face swap
    @staticmethod
    def choose_face_swap_package(name: str, available_images, total_images: int, used_images: int) -> str:
        remain_images = total_images - used_images
        return f"""
*{name}*

You've got a treasure trove of *{total_images} images* in your pack, ready to unleash your creativity! 🌟

🌠 *Your available generations*: {available_images} images. Need more? Explore /buy and /subscribe!
🔍 *Used so far*: {used_images} images. Wow, you're on a roll!
🚀 *Remaining*: {remain_images} images. {'Looks like you have used them all' if remain_images == 0 else 'So much potential'}!

👉 Want more? Type the number of new images to add or press the *Back* button to explore different exciting packages.
"""

    @staticmethod
    def face_swap_package_forbidden(available_images: int):
        return f"""
🔔 *Oops, a little hiccup!* 🚧

Looks like you've got only *{available_images} generations* left in your arsenal.

💡 *Pro Tip*: Sometimes, less is more! Try a smaller number, or give /buy and /subscribe a whirl for unlimited possibilities!
"""

    @staticmethod
    def wait_for_another_request(seconds: int) -> str:
        return f"Please wait for another {seconds} seconds before sending the next question ⏳"

    @staticmethod
    def processing_request():
        texts = [
            "I'm currently consulting my digital crystal ball for the best answer... 🔮",
            "One moment please, I'm currently training my hamsters to generate your answer... 🐹",
            "I'm currently rummaging through my digital library for the perfect answer. Bear with me... 📚",
            "Hold on, I'm channeling my inner AI guru for your answer... 🧘",
            "Please wait while I consult with the internet overlords for your answer... 👾",
            "Compiling the wisdom of the ages... or at least what I can find on the internet... 🌐",
            "Just a sec, I'm putting on my thinking cap... Ah, that's better. Now, let's see... 🎩",
            "I'm rolling up my virtual sleeves and getting down to business. Your answer is coming up... 💪",
            "Running at full steam! My AI gears are whirring to fetch your answer... 🚂",
            "Diving into the data ocean to fish out your answer. Be right back... 🌊🎣",
            "I'm consulting with my virtual elves. They're usually great at finding answers... 🧝",
            "Engaging warp drive for hyper-speed answer retrieval. Hold on tight... 🚀",
            "I'm in the kitchen cooking up a fresh batch of answers. This one's gonna be delicious... 🍳",
            "Taking a quick trip to the cloud and back. Hope to bring back some smart raindrops of info... ☁️",
            "Planting your question in my digital garden. Let's see what grows... 🌱🤖"
        ]

        return random.choice(texts)
