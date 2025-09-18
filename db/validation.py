import json

def load_form_template(form_type):
    try:
        with open(f"form_templates/{form_type}.json", "r") as f:
            return json.load(f)
    except Exception:
        return None

def validate_field(form_type, field_name, value):
    template = load_form_template(form_type)
    if not template:
        return False
    for field in template["fields"]:
        if field["name"] == field_name:
            if field["type"] == "text":
                return isinstance(value, str) and len(value) > 0
            if field["type"] == "date":
                import re
                # Simple YYYY-MM-DD validation
                return bool(re.match(r"\d{4}-\d{2}-\d{2}", value))
            if field["type"] == "number":
                try:
                    int(value)
                    return True
                except Exception:
                    return False
    return False