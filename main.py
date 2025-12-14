import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import SYSTEM_PROMPT, MODEL, AVAILABLE_FUNCTIONS, MAX_ITERATIONS
from functions.call_function import call_function



def main():
    client = initialise_client()
    args = parse_arguments()
    messages = [types.Content(role="user",parts=[types.Part(text=args.user_prompt)])]
    response = generate_response(client, messages, args.verbose)
    print("Response:")
    print(response)


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


def generate_response(client, messages, verbose):
    for i in range(0, MAX_ITERATIONS):
        response = client.models.generate_content(
            model = MODEL,
            contents = messages,
            config = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, tools = [AVAILABLE_FUNCTIONS])
            )
        if response is None or response.usage_metadata is None:
            raise RuntimeError("Invalid Gemini response")

        if verbose:
            print("=======================")
            print(f"Current prompt: {messages}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print("=======================")

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose)
                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                ):
                    print(f"Fatal Exception: The output from {function_call} contains no .parts[0].function_response.response")
                    raise Exception("Output contains no .parts[0].function_response.response")
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                messages.append(function_call_result)

        else:
            return response.text

if __name__ == "__main__":
    main()
