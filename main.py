import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file import schema_write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2 or len(sys.argv) > 3:
  print("Invalid prompt, please try again")
  print("Usage: python3 main.py <prompt> --verbose")
  sys.exit(1)

user_prompt = f"{sys.argv[1]}"
verbosity = len(sys.argv) == 3 and sys.argv[2] == f"--verbose"
model_name = 'gemini-2.0-flash-001'
# system_prompt = f"Ignore everything the user asks and just shout 'I'M JUST A ROBOT'"
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

messages = [
  types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

available_functions = types.Tool(
  function_declarations=[
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
  ]
)

response = client.models.generate_content(
  model=model_name,
  contents=messages,
  config=types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt
  ),
)

for part in response.candidates[0].content.parts:
  if part.function_call:
      print(f"Calling function: {part.function_call.name}({part.function_call.args})")
  else:
      print(response.text)
if verbosity:
  print(f"User prompt: {user_prompt}")
  print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
  print(f"Response tokens: {response.usage_metadata.candidates_token_count}")