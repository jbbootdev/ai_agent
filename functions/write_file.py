# python
import os
from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        absolute_target = os.path.abspath(os.path.join(working_directory, file_path))

        if (
            not absolute_target.startswith(absolute_working_directory + os.sep)
            and absolute_target != absolute_working_directory
        ):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        parent = os.path.dirname(absolute_target) or absolute_working_directory
        os.makedirs(parent, exist_ok=True)

        with open(absolute_target, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Represents the file path to the file you wish to read.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The contents that will be written to the file",
            ),
        },
    ),
)
