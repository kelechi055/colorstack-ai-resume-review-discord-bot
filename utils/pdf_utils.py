from pdf2image import convert_from_bytes
import fitz
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

def extract_text_and_formatting(file: bytes) -> dict:
    with fitz.open(stream=file, filetype="pdf") as doc:
        text = ""
        formatting_info = []
        for page in doc:
            text += page.get_text()
            # Extract formatting details for each text block
            for block in page.get_text("dict")["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            formatting_info.append({
                                "text": span["text"],
                                "font": span["font"],
                                "size": span["size"],
                                "bbox": span["bbox"],
                            })
    return {"text": text, "formatting": formatting_info}

def analyze_font_consistency(formatting_info):
    font_set = set()
    for item in formatting_info:
        font_set.add(item["font"])

    if len(font_set) > 1:
        return {
            "issue": True,
            "feedback": f"Multiple fonts detected: {', '.join(font_set)}. Consider using a single font for consistency.",
            "score": 4
        }
    else:
        return {
            "issue": False,
            "feedback": "Font is consistent throughout the document.",
            "score": 10
        }

def check_single_page(file: bytes) -> bool:
    with fitz.open(stream=file, filetype="pdf") as doc:
        return len(doc) == 1