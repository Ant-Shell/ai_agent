import os

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