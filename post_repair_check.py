from pathlib import Path
import pandas as pd

PROJECT = Path(r"C:\Users\n3101\OneDrive\Desktop\HotelAI-Intelligent-Agent")
MASTER = PROJECT / "03_Structured_Data" / "CSV" / "final" / "hotel_faq_final.csv"

print("=" * 90)
print("🏨 HOTEL AI — POST-REPAIR QUALITY CHECK — BATCH 22 GATE")
print("=" * 90)

df = pd.read_csv(MASTER, dtype=str).fillna("")

errors = []

# --------------------------------------------------
# 1. Basic structure
# --------------------------------------------------
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

required = [
    "faq_id", "intent_name", "language", "question_type",
    "question", "ground_truth", "answer",
    "status", "difficulty", "attempts", "source"
]

missing_cols = [c for c in required if c not in df.columns]
if missing_cols:
    errors.append(f"Missing columns: {missing_cols}")
else:
    print("✅ Required columns present")

# --------------------------------------------------
# 2. IDs
# --------------------------------------------------
expected_ids = [f"FAQ{i:04d}" for i in range(1, 673)]
actual_ids = df["faq_id"].tolist()

if actual_ids == expected_ids:
    print("✅ IDs correct: FAQ0001 → FAQ0672")
else:
    errors.append("FAQ IDs are not exactly FAQ0001 → FAQ0672")

if df["faq_id"].duplicated().any():
    errors.append("Duplicate FAQ IDs found")
else:
    print("✅ No duplicate FAQ IDs")

# --------------------------------------------------
# 3. Batch 21 protection
# --------------------------------------------------
batch21 = df[df["faq_id"].between("FAQ0641", "FAQ0672")].copy()

if len(batch21) != 32:
    errors.append(f"Batch 21 row count is {len(batch21)}, expected 32")
else:
    print("✅ Batch 21: 32 rows present")

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

# --------------------------------------------------
# 4. Answer / Ground Truth
# --------------------------------------------------
mismatch = df["answer"] != df["ground_truth"]

if mismatch.sum() == 0:
    print("✅ Answer == Ground Truth: 672/672")
else:
    errors.append(f"Answer/Ground Truth mismatches: {mismatch.sum()}")

# --------------------------------------------------
# 5. Required values
# --------------------------------------------------
required_value_cols = [
    "faq_id", "intent_name", "language",
    "question_type", "question",
    "ground_truth", "answer",
    "status", "difficulty",
    "attempts", "source"
]

null_counts = {
    c: int((df[c].str.strip() == "").sum())
    for c in required_value_cols
}

bad_nulls = {k: v for k, v in null_counts.items() if v}

if bad_nulls:
    errors.append(f"Missing required values: {bad_nulls}")
else:
    print("✅ No required NULL/empty values")

# --------------------------------------------------
# 6. Attempts
# --------------------------------------------------
non_numeric_attempts = pd.to_numeric(
    df["attempts"], errors="coerce"
).isna().sum()

non_zero_attempts = (
    pd.to_numeric(df["attempts"], errors="coerce") != 0
).sum()

if non_numeric_attempts:
    errors.append(f"Non-numeric attempts: {non_numeric_attempts}")
elif non_zero_attempts:
    errors.append(f"Non-zero attempts: {non_zero_attempts}")
else:
    print("✅ All attempts = 0")

# --------------------------------------------------
# 7. Intent validation
# --------------------------------------------------
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

bad_intents = sorted(set(df["intent_name"]) - allowed_intents)

if bad_intents:
    errors.append(f"Unknown intents: {bad_intents}")
else:
    print("✅ All intents recognized")

# --------------------------------------------------
# 8. Languages
# --------------------------------------------------
expected_languages = {"Arabic", "English", "French", "Russian"}
bad_languages = sorted(set(df["language"]) - expected_languages)

if bad_languages:
    errors.append(f"Unknown languages: {bad_languages}")
else:
    print("✅ Languages valid")

print("\nLanguage distribution:")
print(df["language"].value_counts().to_string())

# --------------------------------------------------
# 9. Question types
# --------------------------------------------------
expected_types = {"Direct", "Paraphrased", "Scenario"}
bad_types = sorted(set(df["question_type"]) - expected_types)

if bad_types:
    errors.append(f"Unknown question types: {bad_types}")
else:
    print("\n✅ Question types valid")

print(df["question_type"].value_counts().to_string())

# --------------------------------------------------
# 10. Difficulty
# --------------------------------------------------
expected_difficulty = {"Easy", "Medium"}
bad_diff = sorted(set(df["difficulty"]) - expected_difficulty)

if bad_diff:
    errors.append(f"Unknown difficulty values: {bad_diff}")
else:
    print("\n✅ Difficulty values valid")

print(df["difficulty"].value_counts().to_string())

# --------------------------------------------------
# 11. Status
# --------------------------------------------------
expected_status = {"valid", "generated", "Active"}
bad_status = sorted(set(df["status"]) - expected_status)

if bad_status:
    errors.append(f"Unknown status values: {bad_status}")
else:
    print("\n✅ Status values valid")

print(df["status"].value_counts().to_string())

# --------------------------------------------------
# 12. Source files
# --------------------------------------------------
knowledge = PROJECT / "02_Hotel_Knowledge"

source_map = {
    "check_in_check_out.txt":
        knowledge / "Policies" / "check_in_check_out.txt",

    "hotel_information.txt":
        knowledge / "Hotel_Information" / "hotel_information.txt",

    "identification_policy.txt":
        knowledge / "Policies" / "identification_policy.txt",

    "02_Hotel_Knowledge/Booking/booking_confirmation.txt":
        knowledge / "Booking" / "booking_confirmation.txt",

    "02_Hotel_Knowledge/Booking/booking_modification.txt":
        knowledge / "Booking" / "booking_modification.txt",

    "02_Hotel_Knowledge/Cancellation/cancellation_policy.txt":
        knowledge / "Cancellation" / "cancellation_policy.txt",

    "02_Hotel_Knowledge/Payment/payment_methods.txt":
        knowledge / "Payment" / "payment_methods.txt",

    "02_Hotel_Knowledge/Payment/refund_policy.txt":
        knowledge / "Payment" / "refund_policy.txt",

    "02_Hotel_Knowledge/Policies/children_policy.txt":
        knowledge / "Policies" / "children_policy.txt",

    "02_Hotel_Knowledge/Policies/pet_policy.txt":
        knowledge / "Policies" / "pet_policy.txt",

    "02_Hotel_Knowledge/Policies/smoking_policy.txt":
        knowledge / "Policies" / "smoking_policy.txt",
}

missing_sources = []

for source, path in source_map.items():
    if not path.exists():
        missing_sources.append(str(path))

if missing_sources:
    errors.append(f"Missing Knowledge files: {missing_sources}")
else:
    print("✅ All canonical Knowledge sources exist")

# --------------------------------------------------
# FINAL RESULT
# --------------------------------------------------
print("\n" + "=" * 90)
print("🏁 FINAL RESULT")
print("=" * 90)

if errors:
    print("❌ POST-REPAIR CHECK FAILED")
    print("\nProblems:")
    for e in errors:
        print(" -", e)

    print("\n⛔ DO NOT CREATE BATCH 22 YET.")
else:
    print("🎉 POST-REPAIR CHECK PASSED")
    print("✅ Master is clean")
    print("✅ Batch 21 remains protected")
    print("✅ Ready to generate Batch 22")
    print("\n🚀 NEXT STEP: BATCH 22 GENERATION")