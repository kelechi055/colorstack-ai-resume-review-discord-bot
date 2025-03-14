from pdf2image import convert_from_bytes
import fitz
from io import BytesIO
import base64
import logging
import sys
import os

# Convert PDF to Image (Base64)
def convert_pdf_to_image(file: bytes) -> str:
    try:
        # Check if we're on Heroku or similar platform
        if 'DYNO' in os.environ:
            # Heroku has Poppler installed via Aptfile
            images = convert_from_bytes(file, first_page=1, last_page=1)
        else:
            # Try to use default path
            try:
                images = convert_from_bytes(file, first_page=1, last_page=1)
            except Exception as e:
                logging.warning(f"Default Poppler path failed: {e}")
                # Try platform-specific paths
                if sys.platform == 'win32':
                    # Windows - try common installation path
                    poppler_path = os.path.join(os.getcwd(), 'poppler', 'bin')
                    if not os.path.exists(poppler_path):
                        poppler_path = r"C:\Program Files\poppler\bin"
                    images = convert_from_bytes(file, first_page=1, last_page=1, poppler_path=poppler_path)
                elif sys.platform == 'darwin':
                    # macOS - try Homebrew path
                    images = convert_from_bytes(file, first_page=1, last_page=1, poppler_path="/usr/local/bin")
                else:
                    # Linux - try common paths
                    images = convert_from_bytes(file, first_page=1, last_page=1)
        
        buffered = BytesIO()
        images[0].save(buffered, format="PNG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        logging.info("Converted PDF to Base64 image successfully")
        return img_base64
    except Exception as e:
        logging.error(f"Error converting PDF to image: {e}")
        # Return a placeholder image or raise the exception
        raise

def extract_text_and_formatting(file: bytes) -> dict:
    with fitz.open(stream=file, filetype="pdf") as doc:
        text = ""
        formatting_info = []
        for page in doc:
            text += page.get_text()
            page_dict = page.get_text("dict")
            
            # Log the entire structure of the page_dict
            logging.info(f"Page dict structure: {page_dict}")

            # Check if 'blocks' exists and is a list
            if "blocks" in page_dict:
                if isinstance(page_dict["blocks"], list):
                    for block in page_dict["blocks"]:
                        if "lines" in block:
                            for line in block["lines"]:
                                for span in line["spans"]:
                                    formatting_info.append({
                                        "text": span["text"],
                                        "font": span["font"],
                                        "size": span["size"],
                                        "bbox": span["bbox"],
                                    })
                else:
                    logging.error("'blocks' is not a list.")
            else:
                logging.warning("No valid 'blocks' found in page dict.")
                
    result = {"text": text, "formatting": formatting_info}
    logging.info(f"Extracted data: {result}")
    return result

def analyze_font_consistency(formatting_info):
    font_set = set()
    for item in formatting_info:
        logging.info(f"ITEM: {item['font']}")
        font_set.add(item["font"])

    if len(font_set) > 1:
        feedback = f"Multiple fonts detected: {', '.join(font_set)}. Consider using a single font for consistency."
        logging.info(feedback)
        return {
            "issue": True,
            "feedback": feedback,
            "score": 4
        }
    else:
        feedback = "Font is consistent throughout the document."
        logging.info(feedback)
        return {
            "issue": False,
            "feedback": feedback,
            "score": 10
        }

def check_single_page(file: bytes) -> bool:
    with fitz.open(stream=file, filetype="pdf") as doc:
        page_count = len(doc)
        logging.info(f"Detected {page_count} pages in the PDF.")
        return page_count == 1