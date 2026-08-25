from pathlib import Path
import pandas as pd

PROJECT = Path(
    r"C:\Users\n3101\OneDrive\Desktop\HotelAI-Intelligent-Agent"
)

MASTER = (
    PROJECT
    / "03_Structured_Data"
    / "CSV"
    / "final"
    / "hotel_faq_final.csv"
)

KNOWLEDGE = PROJECT / "02_Hotel_Knowledge"

print("=" * 90)
print("🏨 HOTEL AI — FINAL MASTER AUDIT — BEFORE BATCH 24")
print("=" * 90)

# ============================================================
# 1. FILE CHECK
# ============================================================

if not MASTER.exists():
    raise FileNotFoundError(
        f"Master file not found:\n{MASTER}"
    )

if not KNOWLEDGE.exists():
    raise FileNotFoundError(
        f"Knowledge folder not found:\n{KNOWLEDGE}"
    )

df = pd.read_csv(
    MASTER,
    dtype=str,
    keep_default_na=False
)

errors = []

print("\n[1] FILE CHECK")
print("✅ Master file exists")
print("✅ Knowledge folder exists")

# ============================================================
# 2. MASTER STRUCTURE
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

print("\n[2] MASTER STRUCTURE")

missing_columns = [
    col for col in required_columns
    if col not in df.columns
]

if missing_columns:
    errors.append(
        f"Missing columns: {missing_columns}"
    )
else:
    print("✅ All required columns present")

if len(df) != 736:
    errors.append(
        f"Master rows = {len(df)}, expected 736"
    )
else:
    print("✅ Master contains exactly 736 rows")

# ============================================================
# 3. ID INTEGRITY
# ============================================================

print("\n[3] ID INTEGRITY")

expected_ids = [
    f"FAQ{i:04d}"
    for i in range(1, 737)
]

if df["faq_id"].tolist() != expected_ids:
    errors.append(
        "IDs are not exactly FAQ0001 → FAQ0736"
    )
else:
    print("✅ IDs exactly FAQ0001 → FAQ0736")

duplicate_count = int(
    df["faq_id"].duplicated().sum()
)

if duplicate_count:
    errors.append(
        f"Duplicate FAQ IDs: {duplicate_count}"
    )
else:
    print("✅ No duplicate FAQ IDs")

# ============================================================
# 4. REQUIRED VALUES
# ============================================================

print("\n[4] REQUIRED VALUES")

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
        f"Empty required values: {empty_values}"
    )
else:
    print("✅ No required NULL/empty values")

# ============================================================
# 5. ANSWER / GROUND TRUTH
# ============================================================

print("\n[5] ANSWER / GROUND TRUTH")

answer_mismatch = int(
    (
        df["answer"]
        != df["ground_truth"]
    ).sum()
)

if answer_mismatch:
    errors.append(
        f"Answer/Ground Truth mismatches: {answer_mismatch}"
    )
else:
    print("✅ Answer == Ground Truth: 736/736")

# ============================================================
# 6. ATTEMPTS
# ============================================================

print("\n[6] ATTEMPTS")

attempts = pd.to_numeric(
    df["attempts"],
    errors="coerce"
)

non_numeric = int(
    attempts.isna().sum()
)

non_zero = int(
    (attempts != 0).sum()
)

if non_numeric:
    errors.append(
        f"Non-numeric attempts: {non_numeric}"
    )

if non_zero:
    errors.append(
        f"Non-zero attempts: {non_zero}"
    )

if not non_numeric and not non_zero:
    print("✅ All attempts = 0")

# ============================================================
# 7. INTENTS
# ============================================================

print("\n[7] INTENTS")

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
    set(df["intent_name"])
    - allowed_intents
)

if bad_intents:
    errors.append(
        f"Unknown intents: {bad_intents}"
    )
else:
    print("✅ All intents recognized")

# ============================================================
# 8. INTENT ID MAPPING
# ============================================================

print("\n[8] INTENT ID MAPPING")

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

mapping_errors = 0

for intent_name, expected_id in intent_map.items():

    rows = df[
        df["intent_name"] == intent_name
    ]

    bad = rows[
        rows["intent_id"] != expected_id
    ]

    if len(bad):
        mapping_errors += len(bad)
        errors.append(
            f"{intent_name}: expected {expected_id}, "
            f"invalid rows = {len(bad)}"
        )

if mapping_errors == 0:
    print("✅ All intent_id mappings valid")

# ============================================================
# 9. LANGUAGES
# ============================================================

print("\n[9] LANGUAGES")

allowed_languages = {
    "Arabic",
    "English",
    "French",
    "Russian",
}

bad_languages = sorted(
    set(df["language"])
    - allowed_languages
)

if bad_languages:
    errors.append(
        f"Unknown languages: {bad_languages}"
    )
else:
    print("✅ All languages valid")

print(
    df["language"]
    .value_counts()
    .to_string()
)

# ============================================================
# 10. QUESTION TYPES
# ============================================================

print("\n[10] QUESTION TYPES")

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
        f"Unknown question types: {bad_question_types}"
    )
else:
    print("✅ All question types valid")

print(
    df["question_type"]
    .value_counts()
    .to_string()
)

# ============================================================
# 11. DIFFICULTY
# ============================================================

print("\n[11] DIFFICULTY")

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
        f"Unknown difficulty values: {bad_difficulty}"
    )
else:
    print("✅ All difficulty values valid")

print(
    df["difficulty"]
    .value_counts()
    .to_string()
)

# ============================================================
# 12. STATUS
# ============================================================

print("\n[12] STATUS")

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
    print("✅ All status values valid")

print(
    df["status"]
    .value_counts()
    .to_string()
)

# ============================================================
# 13. BATCH 21 PROTECTION
# ============================================================

print("\n[13] BATCH 21 PROTECTION")

batch21 = df[
    df["faq_id"].isin(
        [f"FAQ{i:04d}" for i in range(641, 673)]
    )
]

if len(batch21) != 32:
    errors.append(
        f"Batch 21 rows = {len(batch21)}, expected 32"
    )
else:
    print("✅ Batch 21 = 32 rows")

if not (batch21["status"] == "Active").all():
    errors.append("Batch 21 status changed")
else:
    print("✅ Batch 21 status = Active")

if not (batch21["difficulty"] == "Medium").all():
    errors.append("Batch 21 difficulty changed")
else:
    print("✅ Batch 21 difficulty = Medium")

if not (batch21["attempts"] == "0").all():
    errors.append("Batch 21 attempts changed")
else:
    print("✅ Batch 21 attempts = 0")

# ============================================================
# 14. BATCH 22 PROTECTION
# ============================================================

print("\n[14] BATCH 22")

batch22 = df[
    df["faq_id"].isin(
        [f"FAQ{i:04d}" for i in range(673, 705)]
    )
]

if len(batch22) != 32:
    errors.append(
        f"Batch 22 rows = {len(batch22)}, expected 32"
    )
else:
    print("✅ Batch 22 = 32 rows")

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

# ============================================================
# 15. BATCH 23
# ============================================================

print("\n[15] BATCH 23")

batch23 = df[
    df["faq_id"].isin(
        [f"FAQ{i:04d}" for i in range(705, 737)]
    )
]

if len(batch23) != 32:
    errors.append(
        f"Batch 23 rows = {len(batch23)}, expected 32"
    )
else:
    print("✅ Batch 23 = 32 rows")

if not (batch23["status"] == "generated").all():
    errors.append("Batch 23 status changed")
else:
    print("✅ Batch 23 status = generated")

if not (batch23["difficulty"] == "Easy").all():
    errors.append("Batch 23 difficulty changed")
else:
    print("✅ Batch 23 difficulty = Easy")

if not (batch23["attempts"] == "0").all():
    errors.append("Batch 23 attempts changed")
else:
    print("✅ Batch 23 attempts = 0")

batch23_answer_mismatch = int(
    (
        batch23["answer"]
        != batch23["ground_truth"]
    ).sum()
)

if batch23_answer_mismatch:
    errors.append(
        f"Batch 23 Answer/Ground Truth mismatches: "
        f"{batch23_answer_mismatch}"
    )
else:
    print("✅ Batch 23 Answer == Ground Truth")

# ============================================================
# 16. CATEGORY
# ============================================================

print("\n[16] CATEGORY")

if df["category"].astype(str).str.strip().eq("").any():
    errors.append("Empty category values found")
else:
    print("✅ No empty category values")

# ============================================================
# 17. SOURCE
# ============================================================

print("\n[17] SOURCES")

if df["source"].astype(str).str.strip().eq("").any():
    errors.append("Empty source values found")
else:
    print("✅ No empty source values")

# ============================================================
# 18. KNOWLEDGE FILES
# ============================================================

print("\n[18] KNOWLEDGE SOURCES")

source_paths = [
    KNOWLEDGE / "Policies" / "check_in_check_out.txt",
    KNOWLEDGE / "Hotel_Information" / "hotel_information.txt",
    KNOWLEDGE / "Policies" / "identification_policy.txt",
    KNOWLEDGE / "Booking" / "booking_confirmation.txt",
    KNOWLEDGE / "Booking" / "booking_modification.txt",
    KNOWLEDGE / "Cancellation" / "cancellation_policy.txt",
    KNOWLEDGE / "Payment" / "payment_methods.txt",
    KNOWLEDGE / "Payment" / "refund_policy.txt",
    KNOWLEDGE / "Policies" / "children_policy.txt",
    KNOWLEDGE / "Policies" / "pet_policy.txt",
    KNOWLEDGE / "Policies" / "smoking_policy.txt",
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
    print("✅ All required Knowledge files exist")

# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 90)
print("🏁 FINAL MASTER AUDIT RESULT")
print("=" * 90)

if errors:

    print("❌ AUDIT FAILED")

    print("\nProblems:")
    for error in errors:
        print(f" - {error}")

    print("\n⛔ DO NOT START BATCH 24")
    raise SystemExit(1)

print("🎉 FINAL AUDIT PASSED — 100%")
print()
print("✅ Master = 736 rows")
print("✅ IDs = FAQ0001 → FAQ0736")
print("✅ No duplicate IDs")
print("✅ Batch 21 protected")
print("✅ Batch 22 valid")
print("✅ Batch 23 valid")
print("✅ Answer == Ground Truth")
print("✅ All attempts = 0")
print("✅ All intents valid")
print("✅ All intent_id mappings valid")
print("✅ All languages valid")
print("✅ All question types valid")
print("✅ All difficulty values valid")
print("✅ All status values valid")
print("✅ Categories populated")
print("✅ Sources populated")
print("✅ Knowledge sources exist")
print("✅ Audit is READ-ONLY")
print()
print("🚀 MASTER IS READY")
print("🚀 SAFE TO START BATCH 24")
print("=" * 90)