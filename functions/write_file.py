import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if not valid_target_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        parent_dir = os.path.dirname(target_file_path)
        if parent_dir != "":
            os.makedirs(parent_dir, 0o755, exist_ok=True)
        with open(target_file_path, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name='write_file',
    description='Writes or overwrites content to a specified file path. Automatically creates parent directories if they don\'t exist.',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=[
            'working_directory',
            'file_path',
            'content',
        ],
        properties={
            'working_directory': types.Schema(
                type=types.Type.STRING,
                description='The absolute base directory path where the file is allowed to be written.',
            ),
            'file_path': types.Schema(
                type=types.Type.STRING,
                description='Path to the writable file',
            ),
            'content': types.Schema(
                type=types.Type.STRING,
                description='Writable file content',
            ),
        },
    ),
)