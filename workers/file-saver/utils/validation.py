import os
import re
from pydantic import BaseModel, Field, validator
from typing import Optional

class FileInput(BaseModel):
    """
    Pydantic model for validating file saver input.
    """
    destination_folder: str
    filename: str
    file_data: str
    compress: Optional[bool] = False
    
    @validator('destination_folder')
    def validate_destination_folder(cls, v):
        if not v:
            raise ValueError("Destination folder cannot be empty")
        return v
    
    @validator('filename')
    def validate_filename(cls, v):
        if not v:
            raise ValueError("Filename cannot be empty")
        if re.search(r'[<>:"|?*]', v):
            raise ValueError("Filename contains invalid characters")
        return v
    
    @validator('file_data')
    def validate_file_data(cls, v):
        if not v:
            raise ValueError("File data cannot be empty")
        # Basic check for Base64 format
        if not re.match(r'^[A-Za-z0-9+/]+={0,2}$', v):
            raise ValueError("File data is not valid Base64")
        return v

def validate_input(event):
    """
    Validates the input event using the Pydantic model.
    
    Args:
        event (dict): The event payload
        
    Returns:
        FileInput: Validated input data
    """
    return FileInput(**event)

def validate_path(destination_folder, filename):
    """
    Validates and normalizes the destination path.
    
    Args:
        destination_folder (str): The destination folder
        filename (str): The filename
        
    Returns:
        str: The full normalized path
    """
    # Check for path traversal attempts before normalization
    if '..' in destination_folder.split('/') or '..' in destination_folder.split('\\'):
        raise ValueError("Path traversal detected in destination folder")
    
    # Normalize path after checking for traversal
    destination_folder = os.path.normpath(destination_folder)
    
    # Create full path
    full_path = os.path.join(destination_folder, filename)
    
    # Create directory if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)
    
    return full_path