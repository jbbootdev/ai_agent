#python
import os



def write_file(working_directory, file_path, content):
    try:
        absolute_working_directory = os.path.abspath(working_directory)
        absolute_target = os.path.abspath(os.path.join(working_directory, file_path))

        if not absolute_target.startswith(absolute_working_directory + os.sep) and absolute_target != absolute_working_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        parent = os.path.dirname(absolute_target) or absolute_working_directory
        os.makedirs(parent, exist_ok=True)

        with open(absolute_target, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"
