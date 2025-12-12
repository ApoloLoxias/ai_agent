import os

def write_file(working_directory, file_path, content):
    pwd = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    parent_dir = os.path.dirname(full_path)

    if not full_path.startswith(pwd):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.isdir(parent_dir):
        try:
            os.makedirs(os.path.dirname(full_path))
        except Exception as e:
            return f"Error: {e}"

    try:
        with open(full_path, mode = "w") as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'   
    except Exception as e:
        return f"Error: {e}"