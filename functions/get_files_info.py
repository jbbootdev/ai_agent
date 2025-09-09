import os

def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        abs_working = os.path.abspath(working_directory)
        abs_target = os.path.abspath(full_path)

        if not (abs_target == abs_working or abs_target.startswith(abs_working + os.sep)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_target):
            return f'Error: "{directory} is not a directory'

        entries = os.listdir(abs_target)
        lines = []

        for name in sorted(entries):
            entry_path = os.path.join(abs_target, name)
            try:
                size = os.path.getsize(entry_path)
                is_dir = os.path.isdir(entry_path)
                lines.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")
            except Exception as e:
                lines.append(f"- {name}: Error: {str(e)}")

        return "\n".join(lines)
    except Exception as e:
        return f"Error: {str(e)}"

