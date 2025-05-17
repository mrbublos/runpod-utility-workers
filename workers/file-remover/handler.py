import os
from pathlib import Path
from typing import Dict

from loguru import logger
from utils.validation import RemovalRequest
from utils.security import is_safe_path, check_permissions
from utils.file_ops import remove_path

async def handler(event: Dict) -> Dict:
    """
    RunPod handler function for file/folder removal.
    
    Args:
        event: Dictionary containing the job parameters
        
    Returns:
        dict: Response containing success status and metadata
    """
    try:
        # Validate input
        request = RemovalRequest(**event["input"])
        target_path = request.get_full_path()
        
        # Security checks
        if not is_safe_path(target_path, request.allowed_root):
            return {
                "error": "Invalid or unsafe path specified",
                "success": False
            }
            
        if not check_permissions(target_path):
            return {
                "error": "Insufficient permissions",
                "success": False
            }
            
        # Perform removal
        metadata = await remove_path(target_path, request.recursive)
        
        return {
            "success": True,
            "removed_path": str(target_path),
            "metadata": metadata
        }
        
    except Exception as e:
        logger.exception("Error in file removal handler")
        return {
            "error": str(e),
            "success": False
        }