import os
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    try:
        wd_abs_path = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(working_directory, file_path))

        if (
            not target_abs.startswith(wd_abs_path + os.sep)
            and target_abs != wd_abs_path
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_abs):
            return f'Error: File is not found or is not a regular file: "{file_path}"'

        with open(target_abs, "r") as f:
            content = f.read(MAX_CHARS)
            remainder = f.read(1)

        if remainder:
            return (
                content + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )

        return content
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Represents the file path to the file you wish to read.",
            ),
        },
    ),
)
