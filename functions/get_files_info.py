import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        dir_contents = os.listdir(target_dir)
        result = [f"Result for {"current" if directory == "." else directory} directory:"]
        for content in dir_contents:
            if content.startswith("__"):
                continue
            content_path = os.path.normpath(os.path.join(target_dir, content))
            result.append(f"  - {content}: file_size={os.path.getsize(content_path)} bytes, is_dir={os.path.isdir(content_path)}")
        return "\n".join(result)
    except Exception as e:
        return f"Error: {e}"