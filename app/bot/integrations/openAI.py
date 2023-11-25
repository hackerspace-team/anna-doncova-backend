import openai

from AnnaDoncovaBackend import settings

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


def get_response_message(current_model: str, history: list):
    response = client.chat.completions.create(
        model=current_model,
        messages=history
    )

    return response.choices[0].message
