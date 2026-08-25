from pathlib import Path
import pandas as pd

PROJECT = Path(r"C:\Users\n3101\OneDrive\Desktop\HotelAI-Intelligent-Agent")

MASTER = (
    PROJECT
    / "03_Structured_Data"
    / "CSV"
    / "final"
    / "hotel_faq_final.csv"
)

print("=" * 90)
print("🏨 HOTEL AI — POST-MERGE QUALITY CHECK — BATCH 23 GATE")
print("=" * 90)

# ============================================================
# 1. FILE CHECK
# ============================================================

if not MASTER.exists():
    raise FileNotFoundError(
        f"Master file not found:\n{MASTER}"
    )

df = pd.read_csv(MASTER, dtype=str).fillna("")

errors = []

print(f"MASTER : {MASTER}")
print(f"Rows   : {len(df)}")
print(f"Columns: {len(df.columns)}")

# ============================================================
# 2. REQUIRED COLUMNS
# ============================================================

required_columns = [
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

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    errors.append(
        f"Missing columns: {missing_columns}"
    )
else:
    print("✅ Required columns present")

if len(df) != 736:
    errors.append(
        f"Master row count = {len(df)}, expected 736"
    )
else:
    print("✅ Master = 736 rows")

# ============================================================
# 3. FAQ IDS
# ============================================================

expected_ids = [
    f"FAQ{i:04d}"
    for i in range(1, 737)
]

actual_ids = df["faq_id"].tolist()

if actual_ids == expected_ids:
    print("✅ IDs correct: FAQ0001 → FAQ0736")
else:
    errors.append(
        "FAQ IDs are not exactly FAQ0001 → FAQ0736"
    )

if df["faq_id"].duplicated().any():
    errors.append("Duplicate FAQ IDs found")
else:
    print("✅ No duplicate FAQ IDs")

# ============================================================
# 4. BATCH 21
# ============================================================

batch21_ids = [
    f"FAQ{i:04d}"
    for i in range(641, 673)
]

batch21 = df[
    df["faq_id"].isin(batch21_ids)
].copy()

if len(batch21) != 32:
    errors.append(
        f"Batch 21 row count = {len(batch21)}, expected 32"
    )
else:
    print("✅ Batch 21: 32 rows present")

if not batch21.empty:

    if not (batch21["status"] == "Active").all():
        errors.append("Batch 21 status changed")
    else:
        print("✅ Batch 21 status preserved")

    if not (batch21["difficulty"] == "Medium").all():
        errors.append("Batch 21 difficulty changed")
    else:
        print("✅ Batch 21 difficulty preserved")

    if not (batch21["attempts"] == "0").all():
        errors.append("Batch 21 attempts changed")
    else:
        print("✅ Batch 21 attempts preserved")

# ============================================================
# 5. BATCH 22
# ============================================================

batch22_ids = [
    f"FAQ{i:04d}"
    for i in range(673, 705)
]

batch22 = df[
    df["faq_id"].isin(batch22_ids)
].copy()

if len(batch22) != 32:
    errors.append(
        f"Batch 22 row count = {len(batch22)}, expected 32"
    )
else:
    print("✅ Batch 22: 32 rows present")

if not batch22.empty:

    if not (batch22["status"] == "generated").all():
        errors.append("Batch 22 status changed")
    else:
        print("✅ Batch 22 status = generated")

    if not (batch22["difficulty"] == "Easy").all():
        errors.append("Batch 22 difficulty changed")
    else:
        print("✅ Batch 22 difficulty = Easy")

    if not (batch22["attempts"] == "0").all():
        errors.append("Batch 22 attempts changed")
    else:
        print("✅ Batch 22 attempts = 0")

    batch22_mismatch = (
        batch22["answer"] != batch22["ground_truth"]
    ).sum()

    if batch22_mismatch:
        errors.append(
            f"Batch 22 Answer/Ground Truth mismatches: "
            f"{batch22_mismatch}"
        )
    else:
        print("✅ Batch 22 Answer == Ground Truth")

# ============================================================
# 6. BATCH 23
# ============================================================

batch23_ids = [
    f"FAQ{i:04d}"
    for i in range(705, 737)
]

batch23 = df[
    df["faq_id"].isin(batch23_ids)
].copy()

if len(batch23) != 32:
    errors.append(
        f"Batch 23 row count = {len(batch23)}, expected 32"
    )
else:
    print("✅ Batch 23: 32 rows present")

if not batch23.empty:

    if not (batch23["status"] == "generated").all():
        errors.append(
            "Batch 23 status is not generated"
        )
    else:
        print("✅ Batch 23 status = generated")

    if not (batch23["difficulty"] == "Easy").all():
        errors.append(
            "Batch 23 difficulty is not Easy"
        )
    else:
        print("✅ Batch 23 difficulty = Easy")

    if not (batch23["attempts"] == "0").all():
        errors.append(
            "Batch 23 attempts are not all 0"
        )
    else:
        print("✅ Batch 23 attempts = 0")

    batch23_mismatch = (
        batch23["answer"] != batch23["ground_truth"]
    ).sum()

    if batch23_mismatch:
        errors.append(
            f"Batch 23 Answer/Ground Truth mismatches: "
            f"{batch23_mismatch}"
        )
    else:
        print("✅ Batch 23 Answer == Ground Truth")

# ============================================================
# 7. WHOLE MASTER ANSWER / GROUND TRUTH
# ============================================================

master_mismatch = (
    df["answer"] != df["ground_truth"]
).sum()

if master_mismatch:
    errors.append(
        f"Answer/Ground Truth mismatches: {master_mismatch}"
    )
else:
    print("✅ Answer == Ground Truth: 736/736")

# ============================================================
# 8. REQUIRED VALUES
# ============================================================

empty_values = {}

for col in required_columns:

    count = int(
        (
            df[col]
            .astype(str)
            .str.strip()
            == ""
        ).sum()
    )

    if count:
        empty_values[col] = count

if empty_values:
    errors.append(
        f"Missing required values: {empty_values}"
    )
else:
    print("✅ No required NULL/empty values")

# ============================================================
# 9. ATTEMPTS
# ============================================================

attempts_numeric = pd.to_numeric(
    df["attempts"],
    errors="coerce"
)

non_numeric = int(
    attempts_numeric.isna().sum()
)

if non_numeric:
    errors.append(
        f"Non-numeric attempts: {non_numeric}"
    )

non_zero = int(
    (attempts_numeric != 0).sum()
)

if non_zero:
    errors.append(
        f"Non-zero attempts: {non_zero}"
    )
else:
    print("✅ All attempts = 0")

# ============================================================
# 10. INTENTS
# ============================================================

allowed_intents = {
    "booking_confirmation",
    "booking_modification",
    "cancellation_policy",
    "check_in_time",
    "check_out_time",
    "early_check_in",
    "hotel_category",
    "hotel_location",
    "identification_required",
    "late_check_out",
    "payment_methods",
    "pet_policy",
    "refund_policy",
    "reception_availability",
    "smoking_policy",
    "children_policy",
}

bad_intents = sorted(
    set(df["intent_name"]) - allowed_intents
)

if bad_intents:
    errors.append(
        f"Unknown intents: {bad_intents}"
    )
else:
    print("✅ All intents recognized")

# ============================================================
# 11. INTENT ID MAPPING
# ============================================================

expected_intent_map = {
    "hotel_location": "INT001",
    "hotel_category": "INT002",
    "reception_availability": "INT003",
    "check_in_time": "INT004",
    "check_out_time": "INT005",
    "early_check_in": "INT006",
    "late_check_out": "INT007",
    "identification_required": "INT008",
}

intent_mapping_errors = False

for intent_name, expected_id in expected_intent_map.items():

    rows = df[
        df["intent_name"] == intent_name
    ]

    if len(rows) == 0:
        continue

    bad = rows[
        rows["intent_id"] != expected_id
    ]

    if len(bad):
        intent_mapping_errors = True

        errors.append(
            f"Invalid intent_id for {intent_name}: "
            f"expected {expected_id}, found "
            f"{sorted(bad['intent_id'].unique().tolist())}"
        )

if not intent_mapping_errors:
    print("✅ All intent_id mappings valid")

# ============================================================
# 12. BATCH 23 INTENT DISTRIBUTION + MAPPING
# ============================================================

for intent_name, expected_id in expected_intent_map.items():

    rows = batch23[
        batch23["intent_name"] == intent_name
    ]

    if len(rows) != 4:
        errors.append(
            f"Batch 23 {intent_name}: "
            f"expected 4 rows, found {len(rows)}"
        )
        continue

    if not (rows["intent_id"] == expected_id).all():
        errors.append(
            f"Batch 23 invalid intent_id "
            f"for {intent_name}"
        )

print("✅ Batch 23 intent_id mappings checked")

batch23_empty_mapping = {}

if not batch23.empty:

    empty_intent_id = int(
        (
            batch23["intent_id"]
            .astype(str)
            .str.strip()
            == ""
        ).sum()
    )

    empty_category = int(
        (
            batch23["category"]
            .astype(str)
            .str.strip()
            == ""
        ).sum()
    )

    if empty_intent_id:
        batch23_empty_mapping["intent_id"] = empty_intent_id

    if empty_category:
        batch23_empty_mapping["category"] = empty_category

if batch23_empty_mapping:
    errors.append(
        f"Batch 23 empty intent_id/category: "
        f"{batch23_empty_mapping}"
    )
else:
    print(
        "✅ Batch 23 intent_id/category populated"
    )

# ============================================================
# 13. LANGUAGES
# ============================================================

allowed_languages = {
    "Arabic",
    "English",
    "French",
    "Russian",
}

bad_languages = sorted(
    set(df["language"]) - allowed_languages
)

if bad_languages:
    errors.append(
        f"Unknown languages: {bad_languages}"
    )
else:
    print("✅ Languages valid")

print("\nLanguage distribution:")
print(
    df["language"]
    .value_counts()
    .to_string()
)

# ============================================================
# 14. QUESTION TYPES
# ============================================================

allowed_question_types = {
    "Direct",
    "Paraphrased",
    "Scenario",
}

bad_question_types = sorted(
    set(df["question_type"])
    - allowed_question_types
)

if bad_question_types:
    errors.append(
        f"Unknown question types: "
        f"{bad_question_types}"
    )
else:
    print("\n✅ Question types valid")

print(
    df["question_type"]
    .value_counts()
    .to_string()
)

# ============================================================
# 15. DIFFICULTY
# ============================================================

allowed_difficulty = {
    "Easy",
    "Medium",
}

bad_difficulty = sorted(
    set(df["difficulty"])
    - allowed_difficulty
)

if bad_difficulty:
    errors.append(
        f"Unknown difficulty values: "
        f"{bad_difficulty}"
    )
else:
    print("\n✅ Difficulty values valid")

print(
    df["difficulty"]
    .value_counts()
    .to_string()
)

# ============================================================
# 16. STATUS
# ============================================================

allowed_status = {
    "valid",
    "generated",
    "Active",
}

bad_status = sorted(
    set(df["status"])
    - allowed_status
)

if bad_status:
    errors.append(
        f"Unknown status values: {bad_status}"
    )
else:
    print("\n✅ Status values valid")

print(
    df["status"]
    .value_counts()
    .to_string()
)

# ============================================================
# 17. CATEGORY
# ============================================================

allowed_categories = {
    "Hotel FAQ",
    "Hotel Information",
    "Check-in / Check-out",
    "Identification",
    "check_in_time",
    "check_out_time",
    "early_check_in",
    "late_check_out",
    "hotel_location",
    "hotel_category",
    "reception_availability",
    "identification_required",
}

bad_categories = sorted(
    set(df["category"]) - allowed_categories
)

if bad_categories:
    errors.append(
        f"Unknown category values: {bad_categories}"
    )
else:
    print("✅ Categories valid")

# ============================================================
# 18. KNOWLEDGE SOURCES
# ============================================================

knowledge = PROJECT / "02_Hotel_Knowledge"

source_paths = [
    knowledge / "Policies" / "check_in_check_out.txt",
    knowledge / "Hotel_Information" / "hotel_information.txt",
    knowledge / "Policies" / "identification_policy.txt",
    knowledge / "Booking" / "booking_confirmation.txt",
    knowledge / "Booking" / "booking_modification.txt",
    knowledge / "Cancellation" / "cancellation_policy.txt",
    knowledge / "Payment" / "payment_methods.txt",
    knowledge / "Payment" / "refund_policy.txt",
    knowledge / "Policies" / "children_policy.txt",
    knowledge / "Policies" / "pet_policy.txt",
    knowledge / "Policies" / "smoking_policy.txt",
]

missing_sources = [
    str(path)
    for path in source_paths
    if not path.exists()
]

if missing_sources:
    errors.append(
        f"Missing Knowledge files: {missing_sources}"
    )
else:
    print("✅ All canonical Knowledge sources exist")

if (
    df["source"]
    .astype(str)
    .str.strip()
    == ""
).any():
    errors.append("Empty source values found")
else:
    print("✅ No empty source values")

# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 90)
print("🏁 FINAL RESULT")
print("=" * 90)

if errors:

    print("❌ POST-MERGE CHECK FAILED")
    print("\nProblems:")

    for error in errors:
        print(f" - {error}")

    print(
        "\n⛔ DO NOT CREATE BATCH 24 YET"
    )

    raise SystemExit(1)

print("🎉 POST-MERGE CHECK PASSED")
print("✅ Master = 736 rows")
print("✅ IDs = FAQ0001 → FAQ0736")
print("✅ No duplicate IDs")
print("✅ Batch 21 protected")
print("✅ Batch 22 valid")
print("✅ Batch 23 valid")
print("✅ Answer == Ground Truth: 736/736")
print("✅ All required values present")
print("✅ All attempts = 0")
print("✅ All intents valid")
print("✅ All intent_id mappings valid")
print("✅ All languages valid")
print("✅ All question types valid")
print("✅ All difficulty values valid")
print("✅ All status values valid")
print("✅ All categories valid")
print("✅ All Knowledge sources exist")
print("✅ Audit is READ-ONLY")
print()
print("🚀 BATCH 23 COMPLETE")
print("🚀 SAFE TO START BATCH 24")
print("=" * 90)

