from .advanced_extractor import extract_fields_with_ml

def process_image(image_path, form_type):
    return extract_fields_with_ml(image_path, form_type)