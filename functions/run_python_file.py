import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if not valid_target_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not target_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        command = ['python', target_file_path]
        if args is not None:
            command.extend(args)
        process = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = []
        if process.returncode != 0:
            output.append(f"Process exited with code {process.returncode}")
        if not process.stdout and not process.stderr:
            output.append(f'No output produced')
        if process.stdout:
            output.append(f'STDOUT: {process.stdout}')
        if process.stderr:
            output.append(f'STDERR: {process.stderr}')
        return '\n'.join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"