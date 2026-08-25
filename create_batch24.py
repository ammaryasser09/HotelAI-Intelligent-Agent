from pathlib import Path
import pandas as pd

PROJECT = Path(r"C:\Users\n3101\OneDrive\Desktop\HotelAI-Intelligent-Agent")

MASTER = (
    PROJECT / "03_Structured_Data" / "CSV" / "final"
    / "hotel_faq_final.csv"
)

OUT = (
    PROJECT / "03_Structured_Data" / "CSV" / "batches"
    / "hotel_faq_batch24.csv"
)

# Batch 24 = FAQ0737 -> FAQ0768
INTENTS = [
    ("hotel_location", "INT001"),
    ("hotel_category", "INT002"),
    ("reception_availability", "INT003"),
    ("check_in_time", "INT004"),
    ("check_out_time", "INT005"),
    ("early_check_in", "INT006"),
    ("late_check_out", "INT007"),
    ("identification_required", "INT008"),
]

LANGUAGES = ["English", "Arabic", "French", "Russian"]

# Safety check
df = pd.read_csv(MASTER, dtype=str).fillna("")

if len(df) != 736:
    raise RuntimeError(f"Master changed unexpectedly: {len(df)} rows")

if df["faq_id"].iloc[-1] != "FAQ0736":
    raise RuntimeError("Master does not end at FAQ0736")

rows = []
faq_number = 737

for intent_name, intent_id in INTENTS:
    for language in LANGUAGES:

        faq_id = f"FAQ{faq_number:04d}"

        rows.append({
            "faq_id": faq_id,
            "intent_id": intent_id,
            "language": language,
            "question_type": "",
            "question": "",
            "status": "generated",
            "intent_name": intent_name,
            "ground_truth": "",
            "category": intent_name,
            "source": "",
            "attempts": "0",
            "difficulty": "Easy",
            "answer": "",
        })

        faq_number += 1

batch = pd.DataFrame(rows)

OUT.parent.mkdir(parents=True, exist_ok=True)
batch.to_csv(OUT, index=False, encoding="utf-8-sig")

print("=== BATCH 24 SCAFFOLD CREATED ===")
print("Rows:", len(batch))
print("First ID:", batch.faq_id.iloc[0])
print("Last ID:", batch.faq_id.iloc[-1])
print("Master rows:", len(df))
print("Master modified: NO")
print("Output:", OUT)
print()
print("IMPORTANT: questions/answers are NOT generated yet.")
print("Next step: populate Batch 24 from Knowledge sources.")
