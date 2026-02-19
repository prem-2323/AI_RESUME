import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY_B"),
    base_url="https://openrouter.ai/api/v1"
)

def generate_response(prompt: str):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",   # safe default model
            messages=[
                {"role": "system", "content": "You are an expert career advisor and resume expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
