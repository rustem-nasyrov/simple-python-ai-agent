import os
import argparse
from google.genai import types
from dotenv import load_dotenv
from google import genai
from prompts import system_prompt

from functions.get_files_info import schema_get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbouse output")
args = parser.parse_args()
user_prompt = args.user_prompt

available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
)

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=messages,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        temperature=0,
        tools=[available_functions],
    )
)

if args.verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if response.function_calls is not None:
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")
else:
    print(response.text)
