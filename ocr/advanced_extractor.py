from PIL import Image
import pytesseract
import json

# Placeholder for DL-based field extraction
def extract_fields_with_ml(image_path, form_type):
    # In production: Use LayoutLM, Donut, or custom model here
    # For now: fallback to classic OCR+template
    with open(f"form_templates/{form_type}.json", "r") as f:
        template = json.load(f)
    text = pytesseract.image_to_string(Image.open(image_path))
    lines = [l for l in text.splitlines() if l.strip()]
    result = {}
    for idx, field in enumerate(template.get("fields", [])):
        val = lines[idx] if idx < len(lines) else ""
        result[field["name"]] = val.strip()
    return result