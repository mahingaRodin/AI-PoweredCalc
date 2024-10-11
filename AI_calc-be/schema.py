from pydantic import BaseModel  # type: ignore
from typing import Dict

class ImageData(BaseModel):
    image: str  # Base64 encoded image string
    dict_of_vars: Dict[str, str]  # Dictionary with string keys and string values
