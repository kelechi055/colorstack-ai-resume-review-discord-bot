from pdf2image import convert_from_bytes
from io import BytesIO
import base64
import logging

# Convert PDF to Image (Base64)
def convert_pdf_to_image(file: bytes) -> str:
    images = convert_from_bytes(file, first_page=1, last_page=1)
    buffered = BytesIO()
    images[0].save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    logging.info("Converted PDF to Base64 image successfully")
    return img_base64