import os
import argparse
from google.genai import types
from dotenv import load_dotenv
from google import genai

from functions.call_function import call_function
from prompts import system_prompt

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
user_prompt = args.user_prompt

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],
)

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
response = None
max_iter = 20

for iteration in range(max_iter):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0,
            tools=[available_functions],
        )
    )

    if response and len(response.candidates) > 0:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if args.verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Iteration: {iteration + 1}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls:
        function_responses = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, args.verbose)
            if len(function_call_result.parts) == 0:
                raise Exception("Error: function call result parts are empty.")
            if function_call_result.parts[0].function_response is None:
                raise Exception("Error: there is no function response in the first part of function call result.")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Error: the response of the function response in the function call result is empty.")
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(types.Part(function_response=function_call_result.parts[0].function_response))
        messages.append(types.Content(role="user", parts=function_responses))
    else:
        print(response.text)
        break
else:
    print("Error: Reached maximum iterations without final response.")
