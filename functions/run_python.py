import os
import subprocess
from config import MAX_CHARS

def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)

    working_abs = os.path.abspath(working_directory)
    target_abs = os.path.abspath(full_path)

    rel_path = os.path.relpath(target_abs, working_abs)

    if rel_path.startswith('..'):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith('.py'):
        return f'Error: File "{file_path}" is not a Python file.'

    try:
        completed_process = subprocess.run(["python", file_path] + args, capture_output=True, timeout=30, text=True, cwd=working_directory)

        stdout = f"STDOUT: {completed_process.stdout}"
        stderr = f"STDERR: {completed_process.stderr}"
        exit_code = completed_process.returncode

        if exit_code != 0:
            return f"Process exited with code {exit_code}"
        
        if not stdout.strip() and not stderr.strip():
            return "No output produced"
        
        return f"{stdout}\n{stderr}"
        
    except Exception as e:
        return f"Error: executing Python file: {e}"

    
