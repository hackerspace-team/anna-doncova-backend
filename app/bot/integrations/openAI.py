import openai

from AnnaDoncovaBackend import settings
from app.models import Model

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


def get_default_max_tokens(model: str) -> int:
    base = 1024
    if model == Model.GPT3 or model == Model.GPT4:
        return base // 2

    return base


def get_response_message(current_model: str, history: list):
    max_tokens = get_default_max_tokens(current_model)

    response = client.chat.completions.create(
        model=current_model,
        messages=history,
        max_tokens=max_tokens,
    )

    return response.choices[0].message


def get_response_image(prompt: str):
    response = client.images.generate(
        model=Model.DALLE3,
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    return response.data[0].url
