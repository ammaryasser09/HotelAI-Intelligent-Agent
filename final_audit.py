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

print("=" * 95)
print("🏨 HOTEL AI — FINAL MASTER AUDIT — BEFORE BATCH 23")
print("=" * 95)

errors = []

# ============================================================
# 1. FILE EXISTENCE
# ============================================================

print("\n[1] FILE CHECK")

if not MASTER.exists():
    errors.append(f"MASTER FILE NOT FOUND: {MASTER}")
else:
    print("✅ Master file exists")

if not KNOWLEDGE.exists():
    errors.append(f"KNOWLEDGE FOLDER NOT FOUND: {KNOWLEDGE}")
else:
    print("✅ Knowledge folder exists")


# ============================================================
# STOP IF MASTER DOES NOT EXIST
# ============================================================

if not MASTER.exists():
    print("\n❌ AUDIT CANNOT CONTINUE")
    print("=" * 95)
    raise SystemExit(1)


# ============================================================
# LOAD MASTER
# ============================================================

df = pd.read_csv(MASTER, dtype=str).fillna("")

print("\n[2] MASTER STRUCTURE")
print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")


# ============================================================
# 2. REQUIRED COLUMNS
# ============================================================

required_columns = [
    "faq_id",
    "intent_name",
    "language",
    "question_type",
    "question",
    "ground_truth",
    "answer",
    "status",
    "difficulty",
    "attempts",
    "source",
]

missing_columns = [
    c for c in required_columns
    if c not in df.columns
]

if missing_columns:
    errors.append(
        f"Missing columns: {missing_columns}"
    )
else:
    print("✅ All required columns present")


# ============================================================
# 3. EXACT ROW COUNT
# ============================================================

if len(df) == 704:
    print("✅ Master contains exactly 704 rows")
else:
    errors.append(
        f"Expected 704 rows, found {len(df)}"
    )


# ============================================================
# 4. EXACT IDS
# ============================================================

print("\n[3] ID INTEGRITY")

expected_ids = [
    f"FAQ{i:04d}"
    for i in range(1, 705)
]

actual_ids = df["faq_id"].tolist()

if actual_ids == expected_ids:
    print("✅ IDs exactly FAQ0001 → FAQ0704")
else:
    errors.append(
        "FAQ IDs are not exactly FAQ0001 → FAQ0704"
    )

duplicate_ids = df[
    df["faq_id"].duplicated(keep=False)
]

if duplicate_ids.empty:
    print("✅ No duplicate FAQ IDs")
else:
    errors.append(
        f"Duplicate FAQ IDs found: "
        f"{duplicate_ids['faq_id'].tolist()}"
    )


# ============================================================
# 5. BATCH 21
# ============================================================

print("\n[4] BATCH 21 PROTECTION")

batch21 = df[
    df["faq_id"].between("FAQ0641", "FAQ0672")
].copy()

if len(batch21) == 32:
    print("✅ Batch 21 contains 32 rows")
else:
    errors.append(
        f"Batch 21 has {len(batch21)} rows; expected 32"
    )

if len(batch21) == 32:

    if (batch21["status"] == "Active").all():
        print("✅ Batch 21 status = Active")
    else:
        errors.append(
            "Batch 21 status was changed"
        )

    if (batch21["difficulty"] == "Medium").all():
        print("✅ Batch 21 difficulty = Medium")
    else:
        errors.append(
            "Batch 21 difficulty was changed"
        )

    if (batch21["attempts"] == "0").all():
        print("✅ Batch 21 attempts = 0")
    else:
        errors.append(
            "Batch 21 attempts were changed"
        )


# ============================================================
# 6. BATCH 22
# ============================================================

print("\n[5] BATCH 22 VALIDATION")

batch22 = df[
    df["faq_id"].between("FAQ0673", "FAQ0704")
].copy()

if len(batch22) == 32:
    print("✅ Batch 22 contains 32 rows")
else:
    errors.append(
        f"Batch 22 has {len(batch22)} rows; expected 32"
    )

if len(batch22) == 32:

    if (batch22["status"] == "generated").all():
        print("✅ Batch 22 status = generated")
    else:
        errors.append(
            "Batch 22 status is incorrect"
        )

    if (batch22["difficulty"] == "Easy").all():
        print("✅ Batch 22 difficulty = Easy")
    else:
        errors.append(
            "Batch 22 difficulty is incorrect"
        )

    if (batch22["attempts"] == "0").all():
        print("✅ Batch 22 attempts = 0")
    else:
        errors.append(
            "Batch 22 attempts are not all 0"
        )

    batch22_mismatch = (
        batch22["answer"]
        != batch22["ground_truth"]
    )

    if batch22_mismatch.sum() == 0:
        print("✅ Batch 22 Answer == Ground Truth")
    else:
        errors.append(
            f"Batch 22 Answer/Ground Truth mismatches: "
            f"{int(batch22_mismatch.sum())}"
        )


# ============================================================
# 7. GLOBAL ANSWER / GROUND TRUTH
# ============================================================

print("\n[6] ANSWER / GROUND TRUTH")

global_mismatch = (
    df["answer"]
    != df["ground_truth"]
)

mismatch_count = int(global_mismatch.sum())

if mismatch_count == 0:
    print("✅ Answer == Ground Truth: 704/704")
else:
    errors.append(
        f"Answer/Ground Truth mismatches: "
        f"{mismatch_count}"
    )


# ============================================================
# 8. REQUIRED VALUES
# ============================================================

print("\n[7] REQUIRED VALUES")

required_value_columns = [
    "faq_id",
    "intent_name",
    "language",
    "question_type",
    "question",
    "ground_truth",
    "answer",
    "status",
    "difficulty",
    "attempts",
    "source",
]

empty_values = {}

for column in required_value_columns:

    count = int(
        (
            df[column]
            .astype(str)
            .str.strip()
            == ""
        ).sum()
    )

    if count > 0:
        empty_values[column] = count

if empty_values:
    errors.append(
        f"Missing required values: {empty_values}"
    )
else:
    print("✅ No required NULL/empty values")


# ============================================================
# 9. ATTEMPTS
# ============================================================

print("\n[8] ATTEMPTS")

attempts = pd.to_numeric(
    df["attempts"],
    errors="coerce"
)

non_numeric = int(attempts.isna().sum())
non_zero = int((attempts != 0).sum())

if non_numeric == 0:
    print("✅ All attempts are numeric")
else:
    errors.append(
        f"Non-numeric attempts: {non_numeric}"
    )

if non_zero == 0:
    print("✅ All attempts = 0")
else:
    errors.append(
        f"Non-zero attempts: {non_zero}"
    )


# ============================================================
# 10. INTENTS
# ============================================================

print("\n[9] INTENTS")

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

if not bad_intents:
    print("✅ All intents recognized")
else:
    errors.append(
        f"Unknown intents: {bad_intents}"
    )


# ============================================================
# 11. LANGUAGES
# ============================================================

print("\n[10] LANGUAGES")

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

if not bad_languages:
    print("✅ All languages valid")
else:
    errors.append(
        f"Unknown languages: {bad_languages}"
    )

print(
    df["language"]
    .value_counts()
    .to_string()
)


# ============================================================
# 12. QUESTION TYPES
# ============================================================

print("\n[11] QUESTION TYPES")

allowed_question_types = {
    "Direct",
    "Paraphrased",
    "Scenario",
}

bad_question_types = sorted(
    set(df["question_type"])
    - allowed_question_types
)

if not bad_question_types:
    print("✅ All question types valid")
else:
    errors.append(
        f"Unknown question types: {bad_question_types}"
    )

print(
    df["question_type"]
    .value_counts()
    .to_string()
)


# ============================================================
# 13. DIFFICULTY
# ============================================================

print("\n[12] DIFFICULTY")

allowed_difficulty = {
    "Easy",
    "Medium",
}

bad_difficulty = sorted(
    set(df["difficulty"])
    - allowed_difficulty
)

if not bad_difficulty:
    print("✅ All difficulty values valid")
else:
    errors.append(
        f"Unknown difficulty values: {bad_difficulty}"
    )

print(
    df["difficulty"]
    .value_counts()
    .to_string()
)


# ============================================================
# 14. STATUS
# ============================================================

print("\n[13] STATUS")

allowed_status = {
    "valid",
    "generated",
    "Active",
}

bad_status = sorted(
    set(df["status"])
    - allowed_status
)

if not bad_status:
    print("✅ All status values valid")
else:
    errors.append(
        f"Unknown status values: {bad_status}"
    )

print(
    df["status"]
    .value_counts()
    .to_string()
)


# ============================================================
# 15. KNOWLEDGE SOURCES
# ============================================================

print("\n[14] KNOWLEDGE SOURCES")

source_paths = {

    "hotel_information.txt":
        KNOWLEDGE
        / "Hotel_Information"
        / "hotel_information.txt",

    "contact_information.txt":
        KNOWLEDGE
        / "Hotel_Information"
        / "contact_information.txt",

    "check_in_check_out.txt":
        KNOWLEDGE
        / "Policies"
        / "check_in_check_out.txt",

    "identification_policy.txt":
        KNOWLEDGE
        / "Policies"
        / "identification_policy.txt",

    "booking_confirmation.txt":
        KNOWLEDGE
        / "Booking"
        / "booking_confirmation.txt",

    "booking_modification.txt":
        KNOWLEDGE
        / "Booking"
        / "booking_modification.txt",

    "cancellation_policy.txt":
        KNOWLEDGE
        / "Cancellation"
        / "cancellation_policy.txt",

    "payment_methods.txt":
        KNOWLEDGE
        / "Payment"
        / "payment_methods.txt",

    "refund_policy.txt":
        KNOWLEDGE
        / "Payment"
        / "refund_policy.txt",

    "children_policy.txt":
        KNOWLEDGE
        / "Policies"
        / "children_policy.txt",

    "pet_policy.txt":
        KNOWLEDGE
        / "Policies"
        / "pet_policy.txt",

    "smoking_policy.txt":
        KNOWLEDGE
        / "Policies"
        / "smoking_policy.txt",
}

missing_sources = []

for name, path in source_paths.items():

    if not path.exists():
        missing_sources.append(
            f"{name} -> {path}"
        )

if not missing_sources:
    print("✅ All required Knowledge files exist")
else:
    errors.append(
        f"Missing Knowledge files: {missing_sources}"
    )


# ============================================================
# 16. SOURCE COLUMN EMPTY CHECK
# ============================================================

empty_sources = int(
    (
        df["source"]
        .astype(str)
        .str.strip()
        == ""
    ).sum()
)

if empty_sources == 0:
    print("✅ No empty source values")
else:
    errors.append(
        f"Empty source values: {empty_sources}"
    )


# ============================================================
# FINAL AUDIT RESULT
# ============================================================

print("\n" + "=" * 95)
print("🏁 FINAL AUDIT RESULT")
print("=" * 95)

if errors:

    print("❌ FINAL AUDIT FAILED")
    print("\nProblems found:")

    for i, error in enumerate(errors, 1):
        print(f"{i}. {error}")

    print("\n⛔ DO NOT CREATE BATCH 23")
    print("⛔ DO NOT MODIFY THE MASTER")

else:

    print("🎉 FINAL AUDIT PASSED — 100%")
    print()
    print("✅ Master = 704 rows")
    print("✅ IDs = FAQ0001 → FAQ0704")
    print("✅ No duplicate IDs")
    print("✅ Batch 21 protected")
    print("✅ Batch 22 valid")
    print("✅ Answer == Ground Truth: 704/704")
    print("✅ No required empty values")
    print("✅ All attempts = 0")
    print("✅ All intents valid")
    print("✅ All languages valid")
    print("✅ All question types valid")
    print("✅ All difficulty values valid")
    print("✅ All status values valid")
    print("✅ All Knowledge sources exist")
    print("✅ Audit is READ-ONLY")
    print()
    print("🚀 MASTER IS READY")
    print("🚀 SAFE TO START BATCH 23")

print("=" * 95)