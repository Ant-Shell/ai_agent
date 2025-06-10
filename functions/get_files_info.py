import os

def get_files_info(working_directory, directory=None):
  working_directory_path = os.path.abspath(working_directory)
  directory_path = os.path.abspath(os.path.join(working_directory, directory)) if directory != None else working_directory_path

  try:
    if os.path.commonpath([working_directory_path, directory_path]) != working_directory_path:
      return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(directory_path):
      return f'Error: "{directory}" is not a directory'
    
    os_list = os.listdir(directory_path)
    result = list(
      map(
        lambda x: f"- {x}: file_size={get_filesize(directory_path, x)}, is_dir={is_directory(directory_path, x)}", os_list
        )
      )
    return '\n'.join(result)
  except Exception as e:
    return f"Error: {e}"

def get_filesize(path, file):
  absolute_path = os.path.join(path, file)
  return os.path.getsize(absolute_path)

def is_directory(path, file):
  absolute_path = os.path.join(path, file)
  return os.path.isdir(absolute_path)

