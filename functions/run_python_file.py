import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not abs_file_path[-3:] == ".py":
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", abs_file_path]
        if args:
            command.extend(args)
        
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)

        output = ""

        if not result.returncode == 0:
            output += f"Process exited with code {result.returncode}\n"
        if not result.stdout and not result.stderr:
            output += f"No output produced\n"
        else:
            output += f"STDOUT: {result.stdout}\n"
            output += f"STDERR: {result.stderr}\n"
        
        return output
    except Exception as e:
        return f"Error: executing Python file {file_path}: {e}"