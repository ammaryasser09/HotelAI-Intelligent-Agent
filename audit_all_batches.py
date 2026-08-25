import pandas as pd
from pathlib import Path

PROJECT = Path(r"C:\Users\n3101\OneDrive\Desktop\HotelAI-Intelligent-Agent")

MASTER = (
    PROJECT
    / "03_Structured_Data"
    / "CSV"
    / "final"
    / "hotel_faq_final.csv"
)

df = pd.read_csv(MASTER, dtype=str).fillna("")

required = [
    "faq_id",
    "intent_id",
    "language",
    "question_type",
    "question",
    "status",
    "intent_name",
    "ground_truth",
    "category",
    "source",
    "attempts",
    "difficulty",
    "answer",
]

expected_ids = [
    f"FAQ{i:04d}"
    for i in range(1, 769)
]

errors = []

print("=" * 70)
print("HOTEL AI — COMPLETE BATCH 1-24 AUDIT")
print("=" * 70)

print("MASTER ROWS:", len(df))
print("EXPECTED ROWS:", 768)

if len(df) != 768:
    errors.append(f"Wrong master row count: {len(df)}")

if df["faq_id"].tolist() != expected_ids:
    errors.append("FAQ IDs are not exactly FAQ0001 -> FAQ0768")
else:
    print("OK IDs")

duplicates = int(df["faq_id"].duplicated().sum())

if duplicates:
    errors.append(f"Duplicate IDs: {duplicates}")
else:
    print("OK duplicates")

missing_columns = [
    c for c in required
    if c not in df.columns
]

if missing_columns:
    errors.append(f"Missing columns: {missing_columns}")
else:
    print("OK required columns")

empty = {}

for col in required:
    count = int(
        (df[col].astype(str).str.strip() == "").sum()
    )

    if count:
        empty[col] = count

if empty:
    errors.append(f"Required empty values: {empty}")
else:
    print("OK required values")

answer_bad = int(
    (df["answer"] != df["ground_truth"]).sum()
)

if answer_bad:
    errors.append(f"Answer/Ground Truth mismatches: {answer_bad}")
else:
    print("OK Answer == Ground Truth")

attempts = pd.to_numeric(
    df["attempts"],
    errors="coerce"
)

attempts_bad = int(
    (attempts != 0).sum()
)

if attempts_bad:
    errors.append(f"Bad attempts: {attempts_bad}")
else:
    print("OK attempts = 0")


allowed_languages = {
    "English",
    "Arabic",
    "French",
    "Russian",
}

bad_languages = sorted(
    set(df["language"]) - allowed_languages
)

if bad_languages:
    errors.append(f"Bad languages: {bad_languages}")
else:
    print("OK languages")


allowed_question_types = {
    "Direct",
    "Paraphrased",
    "Scenario",
}

bad_question_types = sorted(
    set(df["question_type"]) - allowed_question_types
)

if bad_question_types:
    errors.append(
        f"Bad question types: {bad_question_types}"
    )
else:
    print("OK question types")


allowed_difficulty = {
    "Easy",
    "Medium",
}

bad_difficulty = sorted(
    set(df["difficulty"]) - allowed_difficulty
)

if bad_difficulty:
    errors.append(
        f"Bad difficulty: {bad_difficulty}"
    )
else:
    print("OK difficulty")


allowed_status = {
    "valid",
    "generated",
    "Active",
}

bad_status = sorted(
    set(df["status"]) - allowed_status
)

if bad_status:
    errors.append(
        f"Bad status: {bad_status}"
    )
else:
    print("OK status")


intent_map = {
    "hotel_location": "INT001",
    "hotel_category": "INT002",
    "reception_availability": "INT003",
    "check_in_time": "INT004",
    "check_out_time": "INT005",
    "early_check_in": "INT006",
    "late_check_out": "INT007",
    "identification_required": "INT008",
}

for intent, expected_id in intent_map.items():

    rows = df[df["intent_name"] == intent]

    bad = int(
        (rows["intent_id"] != expected_id).sum()
    )

    if bad:
        errors.append(
            f"{intent}: {bad} bad intent_id"
        )

print()
print("=" * 70)
print("BATCH-BY-BATCH CHECK")
print("=" * 70)

for batch in range(1, 25):

    start = (batch - 1) * 32 + 1
    end = batch * 32

    ids = [
        f"FAQ{i:04d}"
        for i in range(start, end + 1)
    ]

    b = df[df["faq_id"].isin(ids)]

    batch_errors = []

    if len(b) != 32:
        batch_errors.append(
            f"rows={len(b)}"
        )

    if (b["answer"] != b["ground_truth"]).any():
        batch_errors.append("answer mismatch")

    if (
        pd.to_numeric(
            b["attempts"],
            errors="coerce"
        ) != 0
    ).any():
        batch_errors.append("bad attempts")

    if b[required].astype(str).apply(
        lambda x: x.str.strip() == ""
    ).any().any():
        batch_errors.append("empty required value")

    if batch_errors:
        errors.append(
            f"Batch {batch}: {', '.join(batch_errors)}"
        )
        print(
            f"FAIL Batch {batch}: "
            + ", ".join(batch_errors)
        )
    else:
        print(f"PASS Batch {batch}: 32/32")


print()
print("=" * 70)
print("FINAL RESULT")
print("=" * 70)

if errors:

    print("FAIL — PROBLEMS FOUND")
    print()

    for error in errors:
        print("-", error)

else:

    print("PASS — ALL 24 BATCHES ARE VALID")
    print("PASS — MASTER = 768 ROWS")
    print("PASS — IDs = FAQ0001 -> FAQ0768")
    print("PASS — NO DUPLICATES")
    print("PASS — ANSWER == GROUND TRUTH")
    print("PASS — ALL ATTEMPTS = 0")
    print("PASS — NO REQUIRED EMPTY VALUES")
    print("PASS — INTENT MAPPINGS VALID")
    print("PASS — LANGUAGES VALID")
    print("PASS — QUESTION TYPES VALID")
    print("PASS — DIFFICULTY VALID")
    print("PASS — STATUS VALID")
    print("PASS — READ ONLY AUDIT")

print("=" * 70)