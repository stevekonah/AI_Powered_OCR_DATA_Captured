import torch
from PIL import Image
import pytesseract
import json

# Optional: Install transformers, donut, and required OCR dependencies.
# pip install pytorch torchvision transformers pillow

def extract_fields_with_donut(image_path, form_type):
    try:
        from transformers import DonutProcessor, VisionEncoderDecoderModel
        processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
        model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
        image = Image.open(image_path).convert("RGB")
        task_prompt = "<s_docvqa><s_question>{}</s_question><s_answer>".format(form_type)
        pixel_values = processor(image, return_tensors="pt").pixel_values
        input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt").input_ids
        outputs = model.generate(pixel_values, decoder_input_ids=input_ids, max_length=512)
        output = processor.batch_decode(outputs, skip_special_tokens=True)[0]
        # Parse Donut output to dict (your form-specific post-process here)
        # Example: {"Name": "...", "Date": "..."}
        result = json.loads(output)
        return result
    except Exception as e:
        print(f"Donut extraction failed: {e}")
        return None

def extract_fields_with_layoutlm(image_path, form_type):
    try:
        from transformers import LayoutLMv3Processor, LayoutLMv3ForTokenClassification
        processor = LayoutLMv3Processor.from_pretrained("microsoft/layoutlmv3-base", apply_ocr=True)
        model = LayoutLMv3ForTokenClassification.from_pretrained("microsoft/layoutlmv3-base")
        image = Image.open(image_path).convert("RGB")
        encoding = processor(image, return_tensors="pt")
        outputs = model(**encoding)
        preds = outputs.logits.argmax(-1).squeeze().tolist()
        # Map predictions to fields (custom logic here)
        # For demo, fallback to classic OCR
        return None
    except Exception as e:
        print(f"LayoutLM extraction failed: {e}")
        return None

def extract_fields_with_ocr(image_path, form_type):
    # Classic OCR as last resort
    with open(f"form_templates/{form_type}.json", "r") as f:
        template = json.load(f)
    text = pytesseract.image_to_string(Image.open(image_path))
    lines = [l for l in text.splitlines() if l.strip()]
    result = {}
    for idx, field in enumerate(template.get("fields", [])):
        val = lines[idx] if idx < len(lines) else ""
        result[field["name"]] = val.strip()
    return result

def extract_fields(image_path, form_type):
    # Try Donut, then LayoutLM, then OCR
    data = extract_fields_with_donut(image_path, form_type)
    if data: return data
    data = extract_fields_with_layoutlm(image_path, form_type)
    if data: return data
    return extract_fields_with_ocr(image_path, form_type)