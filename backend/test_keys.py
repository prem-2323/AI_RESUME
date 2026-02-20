import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def test_key(key_name):
    key = os.getenv(key_name)
    print(f"Testing {key_name}: {key[:10]}...")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=key,
    )
    try:
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=5
        )
        print(f"{key_name} works: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"{key_name} failed: {e}")
        return False

test_key("OPENROUTER_API_KEY")
test_key("OPENROUTER_API_KEY_B")
