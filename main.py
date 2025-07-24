import argparse
import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.function_declarations import *
# from functions import get_files_info, get_file_content, run_python_file, write_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file
from functions.write_file_content import write_file
from prompts import system_prompt


def main():
    load_dotenv()  # Load environment variables from .env file
    # print("Hello from paigent!")
   
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
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

        if not response.function_calls:
            print(response.text if response.text else "No response received.")
            return
        
        function_call_result = call_function(response.function_calls, verbose=args.verbose)
        func_response = function_call_result.parts[0].function_response.response

        if not func_response:
            print("Error: No function response received.")
            return
            
        if args.verbose:
            print(f"User prompt:{args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        print(f"-> {func_response}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def call_function(function_call_part, verbose=False):
    functions_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    if verbose:
        for call in function_call_part:
            print(f"Calling function: {call.name}({call.args})")
    else:
        print(f" - Calling function: {function_call_part[0].name}")

    function_call = function_call_part[0]
    function_name = function_call.name

    if function_name not in functions_dict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    try:
        function = functions_dict[function_name]

        args = dict(function_call.args) if function_call.args else {}
        args["working_directory"] = "./calculator"
        result = function(**args)
        
       #print(function_name, "args:", args, "\nresult:", result)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": result},
                )
            ],
        )
    
    except Exception as e:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Function execution failed: {str(e)}"},
                )
            ],
        )


    

if __name__ == "__main__":
    main()
