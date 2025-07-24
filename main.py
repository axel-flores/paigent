import argparse
import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from prompts import system_prompt

def main():
    load_dotenv()  # Load environment variables from .env file
    # print("Hello from paigent!")
   
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('user_prompt', help='prompt o instrucciones a realizar')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("Error: api key not found in .env file")
        sys.exit(1)

    try:
        client = genai.Client(api_key=gemini_api_key)

        messages = [
            types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
        ]

        response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
                )
        )

        if args.verbose:
            print(f"User prompt:{args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        if response.function_calls:  # más pythónico que len() > 0
            for call in response.function_calls:
                print(f"Calling function: {call.name}({call.args})")
        else:
            print(response.text)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
