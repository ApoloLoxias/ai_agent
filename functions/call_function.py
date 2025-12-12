from google.genai import types

from config import WORKING_DIRECTORY

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    if function_call_part.name == "get_file_content":
        function_result = get_file_content(WORKING_DIRECTORY, **function_call_part.args)
    elif function_call_part.name == "get_files_info":
        function_result = get_files_info(WORKING_DIRECTORY, **function_call_part.args)
    elif function_call_part.name == "run_python_file":
        function_result = run_python_file(WORKING_DIRECTORY, **function_call_part.args)
    elif function_call_part.name == "write_file":
        function_result = write_file(WORKING_DIRECTORY, **function_call_part.args)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )

