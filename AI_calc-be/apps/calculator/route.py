from fastapi import APIRouter, HTTPException  # Added HTTPException for error handling
import base64
from io import BytesIO
from .utils import analyze_image  # Adjusted import to be relative
from schema import ImageData
from PIL import Image  # type: ignore

app = APIRouter()

@app.post('/calculate')
async def run(data: ImageData):
    try:
        # Decode the base64 image
        image_data = base64.b64decode(data.image.split(',')[1])
    except Exception as e:
        print("Error decoding image data:", str(e))
        raise HTTPException(status_code=400, detail="Invalid image data format.")
    
    try:
        # Load image from bytes
        image_bytes = BytesIO(image_data)
        image = Image.open(image_bytes)
    except Exception as e:
        print("Error opening image:", str(e))
        raise HTTPException(status_code=400, detail="Could not open image. Please check the image format.")

    try:
        # Analyze the image
        responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
        
        # Prepare the response data
        response_data = []
        for response in responses:
            response_data.append(response)
        
        print('Response in route: ', response_data)  # Updated to print `response_data`
        
        return {
            "message": "Image Processed",
            "type": "success",
            "data": response_data,
        }
    except Exception as e:
        print("Error analyzing image:", str(e))
        raise HTTPException(status_code=500, detail="Error processing image.")
