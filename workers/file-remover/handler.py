import os
import runpod
from runpod.serverless.utils.rp_validator import validate
from runpod.serverless.modules.rp_logger import RunPodLogger
from schema import INPUT_SCHEMA
import shutil

logger = RunPodLogger()

def handler(event):
    job_id = event['id']

    validated_input = validate(event['input'], INPUT_SCHEMA)

    folder = os.getenv("USER_DATA_FOLDER")

    if 'errors' in validated_input:
        return {
            'error': validated_input['errors']
        }

    input = validated_input["validated_input"]
    user_id = input['user_id']

    try:
        folder_path = f"{folder}/{user_id}"
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)

        return {
            'job_id': job_id,
            'user_id': user_id,
            'success': True,
        }
    except Exception as e:
        logger.error(f"Error removing user data for {user_id}: {e}", job_id)
        return {
            "success": False,
        }

if __name__ == "__main__":
    runpod.serverless.start(
        {
            'handler': handler
        }
    )