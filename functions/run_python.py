import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
  working_directory_path = os.path.abspath(working_directory)
  full_file_path = os.path.abspath(os.path.join(working_directory, file_path))

  try:
    if os.path.commonpath([working_directory_path, full_file_path]) != working_directory_path:
      return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_file_path):
      return f'Error: File "{file_path}" not found.'
    if os.path.splitext(file_path)[1] != '.py':
      return f'Error: "{file_path}" is not a Python file.'

    result = subprocess.run(["python3", file_path], timeout=30, capture_output=True, cwd=working_directory_path, text=True)
    stdout = result.stdout
    stderr = result.stderr
    returncode = result.returncode
    
    if stdout == '' and stderr == '' and returncode == 0:
      return "No output produced."
    
    output_sections = []
    if stdout:
        output_sections.append(f"STDOUT: {stdout}".rstrip())
    if stderr:
        output_sections.append(f"STDERR: {stderr}".rstrip())
    if returncode != 0:
        output_sections.append(f"Process exited with code {returncode}")
    return '\n'.join(output_sections)
  
  except Exception as e:
    return f"Error: executing Python file: {e}"
  
schema_run_python_file = types.FunctionDeclaration(
  name="run_python_file",
  description="Execute Python files with optional arguments in the specified directory, constrained to the working directory.",
  parameters=types.Schema(
    type=types.Type.OBJECT,
    properties={
      "file_path": types.Schema(
        type=types.Type.STRING,
        description="The file path to execute Python files with optional arguments, relative to the working directory. If not provided, execute files in the working directory itself.",
      ),
    },
    required=["file_path"]
  ),
)