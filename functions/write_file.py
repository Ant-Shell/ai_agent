import os
from google.genai import types

def write_file(working_directory, file_path, content):
  working_directory_path = os.path.abspath(working_directory)
  full_file_path = os.path.abspath(os.path.join(working_directory, file_path))

  try:
    if os.path.commonpath([working_directory_path, full_file_path]) != working_directory_path:
      return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
    
    with open(full_file_path, "w") as f:
      f.write(content)
      return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
  except Exception as e:
    return f"Error: {e}"
  
schema_write_file = types.FunctionDeclaration(
  name="write_file",
  description="Write or overwrite files in the specified directory, constrained to the working directory.",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="The file path to write or overwrite files, relative to the working directory. This is required.",
      ),
      "content": types.Schema(
        type=types.Type.STRING,
        description="The content to write or overwrite to the file. This is required."
      ),
    },
    required=["file_path", "content"]
  ),
)