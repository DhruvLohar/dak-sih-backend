import logging
from celery import shared_task
from PIL import Image
import google.generativeai as genai
import os
import io

logger = logging.getLogger(__name__)

@shared_task
def hello_world():
    logger.info("run hua")
    print("hello")

@shared_task
def stamp_vision_response(image_path):
    # Configure the API key
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    try:
        # Load image
        image = None
        with Image.open(image_path) as img:
            image = img
        
        # Delete image file after loading
        # os.remove(image_path)
        
        # Define the prompt for the Gemini model
        prompt = f"""
        Analyze the uploaded image and identify if it is a valid stamp. If valid, perform the following tasks:

        Use global knowledge and external references to gather additional details about the stamp, including historical, cultural, or philatelic significance.

        - Name of the Stamp
        - Date of Issue
        - Price
        - Brief Description or Special Details (50 words at max)

        If the image is blurry or cannot be recognized as a stamp, respond with an error message indicating: 

        {{"error": "Invalid image. Please try again."}}

        Output Example (Valid Image):   
        {{   "name": "Mahatma Gandhi Commemorative Stamp",   
            "date_of_issue": "1948-08-15",   
            "price": "10 Rupees",   
            "description": "Issued to commemorate Mahatma Gandhi's contributions; features a portrait of Gandhi." 
        }}     

        Output Example (Invalid Image):
        {{   
            "error": "Invalid image. Please try again." 
        }}     

        Process the image carefully and ensure accurate information is extracted.
        """

        # Process the image and generate a response
        response = genai.GenerativeModel("gemini-1.5-flash").generate_content([prompt, image])
        return response.text
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        return {"error": "Invalid image. Please try again."}
