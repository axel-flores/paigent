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
from config import WORKING_DIR, MAX_ITERS


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

    if not args:
        print("PAIGENT Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("Error: api key not found in .env file")
        sys.exit(1)

    try:
        client = genai.Client(api_key=gemini_api_key)

        messages = [
            types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
        ]

        for i in range(MAX_ITERS):
            response = generate_content(client, messages, available_functions, args)
            if response:
                print("Final response:")
                print(response)
                break
        else:
            print(f"Warning: Reached maximum iterations ({MAX_ITERS}) without final response")


    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def generate_content(client, messages, available_functions, args):
    verbose=args.verbose


    response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
                )
        )

    if verbose:
        print(f"User prompt:{args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        #print(response.text if response.text else "No response received.")
        return response.text
    

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="tool", parts=function_responses))
    # function_call_result = call_function(response.function_calls, verbose=args.verbose)
    # func_response = function_call_result.parts[0].function_response.response

    # if not func_response:
    #     print("Error: No function response received.")
    #     return
        

                
def call_function(function_call, verbose=False):

    functions_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    
    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

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
        args["working_directory"] = WORKING_DIR  # Inject working directory
        result = function(**args)
        
        if verbose:
            print(f"Function {function_name} result: {result}")

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
        error_msg = f"Function execution failed: {str(e)}"
        if verbose:
            print(f"Error in {function_name}: {error_msg}")
        
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": error_msg},
                )
            ],
        )


    

if __name__ == "__main__":
    main()
