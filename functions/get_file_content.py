import os
from google.genai import types

def get_file_content(working_directory, file_path):
  working_directory_path = os.path.abspath(working_directory)
  full_file_path = os.path.abspath(os.path.join(working_directory, file_path))

  try:
    if os.path.commonpath([working_directory_path, full_file_path]) != working_directory_path:
      return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_file_path):
      return f'Error: File not found or is not a regular file: "{file_path}"'
    
    MAX_CHARS = 10000

    with open(full_file_path, "r") as f:
        file_content_string = f.read(MAX_CHARS)
        if len(file_content_string):
          return file_content_string + f"[...File '{file_path}' truncated at 10000 characters]"
        return file_content_string

  except Exception as e:
    return f"Error: {e}"
  
schema_get_file_content = types.FunctionDeclaration(
  name="get_file_content",
  description="Read file contents in the specified directory, constrained to the working directory.",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="The file path to read file contents from, relative to the working directory. If not provided, read files in the working directory itself.",
      ),
    },
    required=["file_path"]
  ),
)