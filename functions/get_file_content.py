import os

from config import MAX_CHAR


def get_file_content(working_directory, file_path):
    pwd = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not full_path.startswith(pwd):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(full_path) as file:
            file_content = file.read()
            if len (file_content) > MAX_CHAR:
                file_content = file_content[0:MAX_CHAR] + f'\n[...File "{file_path}" truncated at {MAX_CHAR} characters]'
            return file_content
    except Exception as e:
        return f"Error: {e}"