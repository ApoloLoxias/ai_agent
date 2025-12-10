import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMNI_API_KEY variable not set on .env")

client = genai.Client(api_key = api_key)

def main():
    response = client.models.generate_content(
        model='gemini-2.5-flash', contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )
    if response is None:
        raise RuntimeError("response is None")
    if response.usage_metadata is None:
        raise RuntimeError("response.usage_metadata is None")
    print(response.text)
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
