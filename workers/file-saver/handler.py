import os
import runpod
from runpod.serverless.utils.rp_validator import validate
from runpod.serverless.modules.rp_logger import RunPodLogger
from schema import INPUT_SCHEMA
import base64
import uuid

logger = RunPodLogger()

def handler(event):
    job_id = event['id']

    validated_input = validate(event['input'], INPUT_SCHEMA)

    if 'errors' in validated_input:
        return {
            'error': validated_input['errors']
        }

    input = validated_input["validated_input"]
    user_id = input['user_id']

    try:
        extension = input['extension']
        data = base64.b64decode(input['data'])
        file_name = str(uuid.uuid4())
        folder = os.getenv("USER_DATA_FOLDER")
        file_path = f"{folder}/{user_id}/{file_name}.{extension}"

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            file.write(data)

        return {
            'job_id': job_id,
            'user_id': user_id,
            'success': True,
        }
    except Exception as e:
        logger.error(f"Error saving file for {user_id}: {e}", job_id)
        return {
            "success": False,
        }

if __name__ == "__main__":
    runpod.serverless.start(
        {
            'handler': handler
        }
    )