import random

from app.bot.constants import GPT3_DAILY_LIMIT_MESSAGES
from app.bot.locales.texts import Texts


class English(Texts):
    START = """
Hi there! 👋

The bot allows you to access AI and neural networks
Here you can perform a wide variety of natural language tasks, such as:
1. ~~TODO~~

You can ask questions in any language. If you want to change the language in messages from me - use command /language

✉️ **TODO**
🌅 *TODO*
🎆 TODO
"""
    LANGUAGE = "Language:"
    CHOOSE_LANGUAGE = "Selected language: English 🇺🇸"
    MODE = "Mode:"
    ALREADY_MAKE_REQUEST = "You've already made a request. Please wait ⚠️"
    READY_FOR_NEW_REQUEST = "You can ask the next request 😌"
    CLOSE = "Close 🚪"

    @staticmethod
    def profile(subscription_type: str, current_model: str, daily_limits: dict) -> str:
        return f"""
Subscription type: {subscription_type}
Current model: {current_model} /mode
GPT-3.5 requests for today: {daily_limits['GPT3']}/{GPT3_DAILY_LIMIT_MESSAGES}
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
