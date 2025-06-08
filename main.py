import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2 or len(sys.argv) > 3:
  print("Invalid prompt, please try again")
  print("Usage: python3 main.py <prompt> --verbose")
  sys.exit(1)

user_prompt = f"{sys.argv[1]}"
verbosity = len(sys.argv) == 3 and sys.argv[2] == f"--verbose"

messages = [
  types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
  model='gemini-2.0-flash-001',
  contents=messages,
)

print(response.text)
if verbosity:
  print(f"User prompt: {user_prompt}")
  print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
  print(f"Response tokens: {response.usage_metadata.candidates_token_count}")