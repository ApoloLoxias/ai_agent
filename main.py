import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import SYSTEM_PROMPT, MODEL, AVAILABLE_FUNCTIONS



def main():
    client = initialise_client()
    args = parse_arguments()
    messages = [types.Content(role="user",parts=[types.Part(text=args.user_prompt)])]
    response = generate_response(client, messages)
    print_output(args.user_prompt, response, args.verbose)


def initialise_client():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMNI_API_KEY variable not set on .env")
    return genai.Client(api_key = api_key)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt", type = str, help = "User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def generate_response(client, messages):
    response = client.models.generate_content(
        model = MODEL,
        contents = messages,
        config = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, tools = [AVAILABLE_FUNCTIONS])
        )
    if response is None or response.usage_metadata is None:
        raise RuntimeError("Invalid Gemini response")
    return response

def print_output(user_prompt, response, verbose):
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print("=======================")
    if response.function_calls:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
