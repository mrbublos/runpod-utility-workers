import os
import datetime
import magic

def generate_metadata(file_path):
    """
    Generates metadata for a file.
    
    Args:
        file_path (str): The path to the file
        
    Returns:
        dict: The file metadata
    """
    try:
        # Get file size
        size = os.path.getsize(file_path)
        
        # Get file type
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(file_path)
        
        # Get creation time
        created_at = datetime.datetime.now().isoformat()
        
        return {
            "size": size,
            "mime_type": mime_type,
            "created_at": created_at
        }
    
    except Exception as e:
        # Return basic metadata if error occurs
        return {
            "size": 0,
            "mime_type": "unknown",
            "created_at": datetime.datetime.now().isoformat()
        }