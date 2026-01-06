import os


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        listed_dir = []
        for item in os.listdir(target_dir):
            full_path = os.path.join(target_dir, item)
            result = f"  - {item}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}"
            listed_dir.append(result)
        end_result = "\n".join(listed_dir)
        
        return end_result
    except Exception as e:
        return f"Error listing files {e}"

