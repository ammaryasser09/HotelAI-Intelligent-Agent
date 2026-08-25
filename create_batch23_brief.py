from pathlib import Path
import json

PROJECT = Path(
    r"C:\Users\n3101\OneDrive\Desktop\HotelAI-Intelligent-Agent"
)

BATCH_DIR = (
    PROJECT
    / "03_Structured_Data"
    / "CSV"
    / "batches"
)

OUTPUT = BATCH_DIR / "batch_0705_0736_generation_brief.json"

START_ID = 705
END_ID = 736

INTENTS = [
    "hotel_location",
    "hotel_category",
    "reception_availability",
    "check_in_time",
    "check_out_time",
    "early_check_in",
    "late_check_out",
    "identification_required",
]

LANGUAGES = [
    "English",
    "Arabic",
    "French",
    "Russian",
]

# ============================================================
# SAFETY
# ============================================================

if not PROJECT.exists():
    raise FileNotFoundError(f"Project not found:\n{PROJECT}")

if not BATCH_DIR.exists():
    raise FileNotFoundError(f"Batch directory not found:\n{BATCH_DIR}")

# ============================================================
# CREATE 32-ROW PLAN
# ============================================================

rows = []

faq_number = START_ID

for intent in INTENTS:
    for language in LANGUAGES:

        rows.append(
            {
                "faq_id": f"FAQ{faq_number:04d}",
                "intent_name": intent,
                "language": language,
            }
        )

        faq_number += 1

# ============================================================
# VALIDATION
# ============================================================

if len(rows) != 32:
    raise RuntimeError(
        f"Expected 32 records, got {len(rows)}"
    )

expected_ids = [
    f"FAQ{i:04d}"
    for i in range(START_ID, END_ID + 1)
]

actual_ids = [
    row["faq_id"]
    for row in rows
]

if actual_ids != expected_ids:
    raise RuntimeError(
        "Batch 23 IDs are incorrect."
    )

# ============================================================
# BRIEF
# ============================================================

brief = {
    "batch_number": 23,
    "start_id": "FAQ0705",
    "end_id": "FAQ0736",
    "row_count": 32,
    "records": rows,
}

# ============================================================
# WRITE
# ============================================================

with open(
    OUTPUT,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        brief,
        f,
        ensure_ascii=False,
        indent=2
    )

# ============================================================
# RESULT
# ============================================================

print("=" * 90)
print("🏨 HOTEL AI — BATCH 23 GENERATION BRIEF")
print("=" * 90)

print(f"OUTPUT : {OUTPUT}")
print("ROWS   : 32")
print("IDS    : FAQ0705 → FAQ0736")

print("\n🎯 INTENTS")
for intent in INTENTS:
    print(f"  {intent}: 4")

print("\n🌐 LANGUAGES")
for language in LANGUAGES:
    print(f"  {language}: 8")

print("\n🛡️ SAFETY CHECKS")
print("✅ Master was NOT modified")
print("✅ Batch 21 was NOT modified")
print("✅ Batch 22 was NOT modified")
print("✅ No CSV was modified")
print("✅ Brief only")
print("✅ 32 IDs verified")

print("\n" + "=" * 90)
print("🎉 BATCH 23 BRIEF CREATED")
print("=" * 90)
print("🚀 NEXT STEP: RUN generate_batch23.py")
print("=" * 90)