import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    pwd = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    parent_dir = os.path.dirname(full_path)

    if not full_path.startswith(pwd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path[-3:] == ".py":
        return f'Error: "{file_path}" is not a Python file.'


    arguments = ["python", full_path]
    for arg in args:
        arguments.append(arg)

    try:
        completed_process = subprocess.run(arguments, capture_output=True, timeout=30, cwd = pwd)
        exit_code = completed_process.returncode
        output = completed_process.stdout
        error = completed_process.stderr
        if not output and not error:
            return "No output produced"
        if not  exit_code == 0:
            return f"STDOUT: {output}\nSTDERR: {error}\nProcess exited with code {exit_code}"
        return f"STDOUT: {output}\nSTDERR: {error}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
