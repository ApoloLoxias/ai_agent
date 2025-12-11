import os


def get_files_info(working_directory, directory = "."):
    pwd = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    if not full_path.startswith(pwd):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    try:
        files = os.listdir(full_path)
        file_string = ""
        for file in files:
            file_path = os.path.join(full_path, file)
            file_string += f"- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}\n"
        return file_string
    except Exception as e:
        return f"Error: {e}"