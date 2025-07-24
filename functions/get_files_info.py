import os
from google.genai import types
from config import MAX_CHARS

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

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


    # os.path.abspath(): Get an absolute path from a relative path
    # os.path.join(): Join two paths together safely (handles slashes)
    # .startswith(): Check if a string starts with a substring
    # os.path.isdir(): Check if a path is a directory
    # os.listdir(): List the contents of a directory
    # os.path.getsize(): Get the size of a file
    # os.path.isfile(): Check if a path is a file
    # .join(): Join a list of strings together with a separator
