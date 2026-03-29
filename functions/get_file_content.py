import os

from config import CHARACTER_LIMIT

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if not valid_target_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_file_path) as opened_file:
            contents = opened_file.read(CHARACTER_LIMIT)
            if opened_file.read(1):
                contents += f'[...File "{file_path}" truncated at {CHARACTER_LIMIT} characters]'
            return contents
    except Exception as e:
        return f'Error: {e}'