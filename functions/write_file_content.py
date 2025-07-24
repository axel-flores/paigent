import os

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