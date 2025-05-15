import os
import json
from loguru import logger
from utils.validation import validate_input, validate_path
from utils.file_ops import decode_and_save_file, compress_file
from utils.metadata import generate_metadata

def handler(event):
    """
    Main handler function for the file saver worker.
    
    Args:
        event (dict): The event payload containing the request parameters
        
    Returns:
        dict: Response containing success status, file path, metadata, and any error messages
    """
    try:
        # Validate input
        input_data = validate_input(event)
        
        # Validate path
        destination_path = validate_path(
            input_data.destination_folder, 
            input_data.filename
        )
        
        # Decode and save file
        file_path = decode_and_save_file(
            destination_path,
            input_data.file_data
        )
        
        # Generate metadata
        metadata = generate_metadata(file_path)
        
        # Compress if requested
        if input_data.compress:
            file_path = compress_file(file_path)
            metadata["compressed"] = True
        else:
            metadata["compressed"] = False
        
        # Return success response
        return {
            "success": True,
            "file_path": file_path,
            "metadata": metadata,
            "error": None
        }
        
    except Exception as e:
        # Log error
        logger.error(f"Error processing request: {str(e)}")
        
        # Return error response
        return {
            "success": False,
            "file_path": None,
            "metadata": None,
            "error": str(e)
        }

if __name__ == "__main__":
    # Configure logger
    logger.add("file_saver.log", rotation="10 MB")
    
    # Example usage
    test_event = {
        "destination_folder": "/tmp/test",
        "filename": "test.txt",
        "file_data": "SGVsbG8gV29ybGQh",  # "Hello World!" in Base64
        "compress": False
    }
    
    result = handler(test_event)
    print(json.dumps(result, indent=2))