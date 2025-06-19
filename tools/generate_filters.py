from typing import Tuple
from pydantic import BaseModel

def retrieve_details_from_mongodb(mongo_details: BaseModel) -> Tuple[str, dict]:
    """
    Generic handler for structured MongoDB data with error handling.

    Args:
        mongo_details (BaseModel): Structured input data.

    Returns:
        Tuple[str, dict]: A tuple containing a user-facing content message and a structured artifact.
    """
    print("===================== In generic MongoDB tool ========================")

    try:
        # Attempt to convert to dict
        data = mongo_details.model_dump()

        content = "Structured data successfully received and processed."
        artifact = {
            "is_data_available": True,
            "data": data,
            "message": content
        }

        return content, artifact

    except Exception as e:
        # Handle unexpected error during processing
        error_message = f"Failed to process input data: {str(e)}"
        artifact = {
            "is_data_available": False,
            "data": {},
            "message": error_message,
            "error": str(e)
        }

        return error_message, artifact
