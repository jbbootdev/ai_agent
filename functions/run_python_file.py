# python
import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    abs_work = os.path.normcase(os.path.abspath(working_directory))
    abs_target = os.path.normcase(
        os.path.abspath(os.path.join(working_directory, file_path))
    )

    # Ensure abs_target is within abs_work
    if not (abs_target == abs_work or abs_target.startswith(abs_work + os.sep)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_target):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        cmd = ["python", file_path, *args]
        completed = subprocess.run(
            cmd,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        stdout = completed.stdout or ""
        stderr = completed.stderr or ""

        parts = []
        if stdout:
            parts.append(f"STDOUT:\n{stdout}".rstrip())
        if stderr:
            parts.append(f"STDERR:\n{stderr}".rstrip())
        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")
        if not parts:
            return "No output produced."
        return "\n".join(parts)

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
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
