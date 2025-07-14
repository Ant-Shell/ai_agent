import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2 or len(sys.argv) > 3:
  print("Invalid prompt, please try again")
  print("Usage: python3 main.py <prompt> --verbose")
  sys.exit(1)

user_prompt = f"{sys.argv[1]}"
verbose = len(sys.argv) == 3 and sys.argv[2] == f"--verbose"
model_name = 'gemini-2.0-flash-001'

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

functions_map = {
   "schema_get_files_info": get_files_info,
   "schema_get_file_content": get_file_content,
   "schema_run_python_file": run_python_file,
   "schema_write_file": write_file,
}

def call_function(function_call_part, verbose=False):
  function_name = function_call_part.name
  function_args = function_call_part.args

  if function_name not in functions_map:
    return types.Content(
      role="tool",
      parts=[
        types.Part.from_function_response(
          name=function_name,
          response={"error": f"Unknown function: {function_name}"},
        )
      ],
    )
  
  if verbose:
    print(f"Calling function: {function_name}({function_args})")
  else:
    print(f" - Calling function: {function_name}")

  function_call = functions_map[function_call_part.name]
  modified_args = {**function_args, "working_directory": "./calculator"}
  function_result = function_call(**modified_args)
  return types.Content(
    role="tool",
    parts=[
      types.Part.from_function_response(
        name=function_name,
        response={"result": function_result},
      )
    ],
  )

count = 0
while count <= 20:
  try: 
    response = client.models.generate_content(
      model=model_name,
      contents=messages,
      config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
      ),
    )
    messages.append(response.candidates[0].content)
    for function_call_part in response.candidates[0].content.parts:
      if function_call_part.function_call:
        if verbose:
          print(f" - Calling function: {function_call_part.function_call.name}")
        function_call_result = call_function(function_call_part.function_call, verbose)
        messages.append(types.Content(role='tool', parts=function_call_result.parts))
      
        if not function_call_result.parts[0].function_response.response:
          raise Exception("Function call result missing expected response structure")
      
        if verbose:
          print(f" -> Result: {function_call_result.parts[0].function_response.response}")

    if response.text:
      print(f"Final response: {response.text}" )
      break
    count += 1
  except Exception as e:
    print(f"An error occurred: {e}")
    break

if verbose:
  print(f"User prompt: {user_prompt}")
  print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
  print(f"Response tokens: {response.usage_metadata.candidates_token_count}")