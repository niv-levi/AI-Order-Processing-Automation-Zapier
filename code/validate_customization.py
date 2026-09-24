material = str(input_data.get("material", "")).strip()
size = str(input_data.get("size", "")).strip()
engraving = str(input_data.get("engraving", "")).strip()

try:
    confidence = float(input_data.get("extraction_confidence", 0))
except (TypeError, ValueError):
    confidence = 0.0

missing_fields = []

if not material:
    missing_fields.append("material")

if not size:
    missing_fields.append("size")

if not engraving:
    missing_fields.append("engraving")

if missing_fields:
    validation_status = "needs_review"
    validation_reason = "Missing required fields: " + ", ".join(missing_fields)
elif confidence < 0.80:
    validation_status = "needs_review"
    validation_reason = f"Extraction confidence ({confidence}) is below required threshold (0.80)"
else:
    validation_status = "approved"
    validation_reason = "All required customization fields are present and confidence is sufficient."

output = {
    "validation_status": validation_status,
    "missing_fields": ", ".join(missing_fields),
    "validation_reason": validation_reason,
    "received_material": material,
    "received_size": size,
    "received_engraving": engraving,
    "received_confidence": confidence
}
