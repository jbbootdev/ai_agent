import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic_core import from_json

from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    print("You must provide a prompt.")
    exit(1)
verbose = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] == "--verbose" else None

user_prompt = sys.argv[1]
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

messages = []
messages.append(
    types.Content(
        role="user",
        parts=[
            types.Part(text=user_prompt),
        ],
    )
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_get_file_content,
        schema_run_python_file,
    ]
)

current_iteration = 0
try:
    while current_iteration < 20:
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.function_calls:
            for call in response.function_calls:
                function_call_result = call_function(call, verbose=bool(verbose))
                # ensure the response exists
                fr = function_call_result.parts[0].function_response.response

                messages.append(function_call_result)

                result_text = fr.get("result") if isinstance(fr, dict) else fr

                if fr is None:
                    raise RuntimeError("Function call returned no response")
                if verbose:
                    print(f"-> {result_text}")
                else:
                    print(result_text)
            if verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(
                    f"Response tokens: {response.usage_metadata.candidates_token_count}"
                )

            current_iteration += 1
            continue
        else:
            print(response.text)
            break


except Exception as e:
    print(f"Error: {e}")
