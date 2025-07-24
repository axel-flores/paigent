import os
from config import MAX_CHARS

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