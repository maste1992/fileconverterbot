import os
import uuid

TEMP_DIR = 'temp_files'

def ensure_temp_dir():
    """Ensures the temporary directory exists."""
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

def get_temp_path(extension):
    """Generates a unique temporary file path with the given extension."""
    ensure_temp_dir()
    filename = f"{uuid.uuid4()}.{extension}"
    return os.path.abspath(os.path.join(TEMP_DIR, filename))

def cleanup_files(*paths):
    """Deletes files at the given paths."""
    for path in paths:
        if path and os.path.exists(path):
            try:
                os.remove(path)
                print(f"Deleted temporary file: {path}")
            except Exception as e:
                print(f"Error deleting file {path}: {e}")
