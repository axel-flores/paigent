import os
from config import MAX_CHARS

def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)

    working_abs = os.path.abspath(working_directory)
    target_abs = os.path.abspath(full_path)

    rel_path = os.path.relpath(target_abs, working_abs)

    if rel_path.startswith('..'):
        return (f'\tError: Cannot list "{directory}" as it is outside the permitted working directory')
    
    if not os.path.isdir(full_path):
        return (f'\tError: "{directory}" is not a directory')
    
    dir_contents = os.listdir(full_path)

    try:
        content_string = "\n".join(list(map(lambda x: f"- {x}: file_size={os.path.getsize(os.path.join(full_path, x))} bytes, is_dir={os.path.isdir(os.path.join(full_path, x))}", dir_contents)))
    except Exception as e:
        return f'\tError: {e}'


    return content_string

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)

    working_abs = os.path.abspath(working_directory)
    target_abs = os.path.abspath(full_path)

    rel_path = os.path.relpath(target_abs, working_abs)

    if rel_path.startswith('..'):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(full_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
    except Exception as e:
        return f'Error: {e}'

    return file_content_string


def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)

    working_abs = os.path.abspath(working_directory)
    target_abs = os.path.abspath(full_path)

    rel_path = os.path.relpath(target_abs, working_abs)

    if rel_path.startswith('..'):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(os.path.dirname(full_path)):
        return f'Error: Directory does not exist: "{os.path.dirname(full_path)}"'

    try:
        with open(full_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'

    # os.path.abspath(): Get an absolute path from a relative path
    # os.path.join(): Join two paths together safely (handles slashes)
    # .startswith(): Check if a string starts with a substring
    # os.path.isdir(): Check if a path is a directory
    # os.listdir(): List the contents of a directory
    # os.path.getsize(): Get the size of a file
    # os.path.isfile(): Check if a path is a file
    # .join(): Join a list of strings together with a separator
