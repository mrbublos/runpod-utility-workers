import os
import base64
import gzip
from loguru import logger

def decode_and_save_file(file_path, base64_data, chunk_size=8192):
    """
    Decodes Base64 data and saves it to a file in chunks.
    
    Args:
        file_path (str): The path to save the file to
        base64_data (str): The Base64-encoded file data
        chunk_size (int): The chunk size for processing
        
    Returns:
        str: The path to the saved file
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Process in chunks to handle large files
        with open(file_path, 'wb') as f:
            # Remove any whitespace from the Base64 string
            base64_data = ''.join(base64_data.split())
            
            # Calculate total length and process in chunks
            total_length = len(base64_data)
            
            for i in range(0, total_length, chunk_size):
                end = min(i + chunk_size, total_length)
                chunk = base64_data[i:end]
                decoded_chunk = base64.b64decode(chunk)
                f.write(decoded_chunk)
        
        return file_path
    
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise

def compress_file(file_path):
    """
    Compresses a file using gzip.
    
    Args:
        file_path (str): The path to the file to compress
        
    Returns:
        str: The path to the compressed file
    """
    compressed_path = f"{file_path}.gz"
    
    try:
        with open(file_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb') as f_out:
                f_out.writelines(f_in)
        
        # Remove original file
        os.remove(file_path)
        
        return compressed_path
    
    except Exception as e:
        logger.error(f"Error compressing file: {str(e)}")
        raise