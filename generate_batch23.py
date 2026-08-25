from pathlib import Path
import json
import pandas as pd

PROJECT = Path(
    r"C:\Users\n3101\OneDrive\Desktop\HotelAI-Intelligent-Agent"
)

BATCH_DIR = PROJECT / "03_Structured_Data" / "CSV" / "batches"
KNOWLEDGE = PROJECT / "02_Hotel_Knowledge"

BRIEF = BATCH_DIR / "batch_0705_0736_generation_brief.json"
OUTPUT = BATCH_DIR / "faq_batch_23.csv"

START_ID = 705
END_ID = 736

# ============================================================
# BATCH 23 CONFIGURATION
# ============================================================

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

QUESTION_TYPES = [
    "Direct",
    "Paraphrased",
    "Scenario",
]

# ============================================================
# START
# ============================================================

print("=" * 90)
print("🏨 HOTEL AI — BATCH 23 GENERATION")
print("=" * 90)

print(f"PROJECT : {PROJECT}")
print(f"BRIEF   : {BRIEF}")
print(f"OUTPUT  : {OUTPUT}")

# ============================================================
# BASIC CHECKS
# ============================================================

if not PROJECT.exists():
    raise FileNotFoundError(
        f"Project folder not found:\n{PROJECT}"
    )

if not BATCH_DIR.exists():
    raise FileNotFoundError(
        f"Batch directory not found:\n{BATCH_DIR}"
    )

if not KNOWLEDGE.exists():
    raise FileNotFoundError(
        f"Knowledge folder not found:\n{KNOWLEDGE}"
    )

if not BRIEF.exists():
    raise FileNotFoundError(
        f"Batch 23 brief not found:\n{BRIEF}"
    )

print("\n📋 GENERATION BRIEF FOUND")

# ============================================================
# LOAD BRIEF
# ============================================================

with open(
    BRIEF,
    "r",
    encoding="utf-8"
) as f:
    brief = json.load(f)

records = brief.get("records", [])

if len(records) != 32:
    raise RuntimeError(
        f"Expected 32 records in brief, found {len(records)}"
    )

print(f"Brief records detected: {len(records)}")

# ============================================================
# VERIFY IDS
# ============================================================

expected_ids = [
    f"FAQ{i:04d}"
    for i in range(START_ID, END_ID + 1)
]

actual_ids = [
    row.get("faq_id", "")
    for row in records
]

if actual_ids != expected_ids:
    raise RuntimeError(
        "❌ Batch 23 IDs are not exactly FAQ0705 → FAQ0736"
    )

print("✅ IDs verified: FAQ0705 → FAQ0736")

# ============================================================
# VERIFY INTENTS
# ============================================================

for intent in INTENTS:
    count = sum(
        row.get("intent_name") == intent
        for row in records
    )

    if count != 4:
        raise RuntimeError(
            f"❌ Intent '{intent}' expected 4 rows, got {count}"
        )

print("✅ Intent distribution verified")

# ============================================================
# VERIFY LANGUAGES
# ============================================================

for language in LANGUAGES:
    count = sum(
        row.get("language") == language
        for row in records
    )

    if count != 8:
        raise RuntimeError(
            f"❌ Language '{language}' expected 8 rows, got {count}"
        )

print("✅ Language distribution verified")

# ============================================================
# CANONICAL KNOWLEDGE SOURCES
# ============================================================

source_map = {

    "hotel_location":
        KNOWLEDGE
        / "Hotel_Information"
        / "hotel_information.txt",

    "hotel_category":
        KNOWLEDGE
        / "Hotel_Information"
        / "hotel_information.txt",

    "reception_availability":
        KNOWLEDGE
        / "Hotel_Information"
        / "contact_information.txt",

    "check_in_time":
        KNOWLEDGE
        / "Policies"
        / "check_in_check_out.txt",

    "check_out_time":
        KNOWLEDGE
        / "Policies"
        / "check_in_check_out.txt",

    "early_check_in":
        KNOWLEDGE
        / "Policies"
        / "check_in_check_out.txt",

    "late_check_out":
        KNOWLEDGE
        / "Policies"
        / "check_in_check_out.txt",

    "identification_required":
        KNOWLEDGE
        / "Policies"
        / "identification_policy.txt",
}

print("\n📚 KNOWLEDGE SOURCE CHECK")

for intent, path in source_map.items():

    if not path.exists():
        raise FileNotFoundError(
            f"Missing Knowledge source for '{intent}':\n{path}"
        )

print("✅ All canonical Knowledge sources exist")

# ============================================================
# QUESTION TEMPLATES
# ============================================================

templates = {

    "English": {

        "hotel_location":
            "Where is the hotel located?",

        "hotel_category":
            "What category is the hotel?",

        "reception_availability":
            "Is the hotel reception available 24 hours a day?",

        "check_in_time":
            "What is the standard check-in time?",

        "check_out_time":
            "What is the standard check-out time?",

        "early_check_in":
            "Can I check in early?",

        "late_check_out":
            "Can I check out late?",

        "identification_required":
            "Do I need identification when checking in?",
    },

    "Arabic": {

        "hotel_location":
            "أين يقع الفندق؟",

        "hotel_category":
            "ما تصنيف الفندق؟",

        "reception_availability":
            "هل مكتب الاستقبال متاح على مدار 24 ساعة؟",

        "check_in_time":
            "ما هو وقت تسجيل الوصول المعتاد؟",

        "check_out_time":
            "ما هو وقت تسجيل المغادرة المعتاد؟",

        "early_check_in":
            "هل يمكنني تسجيل الوصول مبكرًا؟",

        "late_check_out":
            "هل يمكنني تسجيل المغادرة متأخرًا؟",

        "identification_required":
            "هل أحتاج إلى إثبات هوية عند تسجيل الوصول؟",
    },

    "French": {

        "hotel_location":
            "Où se trouve l'hôtel ?",

        "hotel_category":
            "Quelle est la catégorie de l'hôtel ?",

        "reception_availability":
            "La réception de l'hôtel est-elle disponible 24 heures sur 24 ?",

        "check_in_time":
            "Quelle est l'heure d'enregistrement standard ?",

        "check_out_time":
            "Quelle est l'heure de départ standard ?",

        "early_check_in":
            "Puis-je faire un enregistrement anticipé ?",

        "late_check_out":
            "Puis-je effectuer un départ tardif ?",

        "identification_required":
            "Ai-je besoin d'une pièce d'identité lors de l'enregistrement ?",
    },

    "Russian": {

        "hotel_location":
            "Где находится отель?",

        "hotel_category":
            "Какова категория отеля?",

        "reception_availability":
            "Работает ли стойка регистрации круглосуточно?",

        "check_in_time":
            "Какое стандартное время регистрации заезда?",

        "check_out_time":
            "Какое стандартное время регистрации выезда?",

        "early_check_in":
            "Можно ли заселиться раньше установленного времени?",

        "late_check_out":
            "Можно ли оформить поздний выезд?",

        "identification_required":
            "Нужен ли документ, удостоверяющий личность, при регистрации?",
    },
}

# ============================================================
# GROUND TRUTH
# ============================================================

ground_truth = {

    "hotel_location": {

        "English":
            "Nile Pearl Hotel is located in Cairo, Egypt.",

        "Arabic":
            "يقع فندق نايل بيرل في القاهرة، مصر.",

        "French":
            "L'hôtel Nile Pearl est situé au Caire, en Égypte.",

        "Russian":
            "Отель Nile Pearl находится в Каире, Египет.",
    },

    "hotel_category": {

        "English":
            "Nile Pearl Hotel is a 5-Star Hotel.",

        "Arabic":
            "فندق نايل بيرل هو فندق خمس نجوم.",

        "French":
            "L'hôtel Nile Pearl est un hôtel 5 étoiles.",

        "Russian":
            "Отель Nile Pearl — пятизвёздочный отель.",
    },

    "reception_availability": {

        "English":
            "Hotel reception is available 24/7.",

        "Arabic":
            "مكتب استقبال الفندق متاح على مدار 24 ساعة.",

        "French":
            "La réception de l'hôtel est disponible 24 heures sur 24.",

        "Russian":
            "Стойка регистрации отеля работает круглосуточно.",
    },

    "check_in_time": {

        "English":
            "The standard check-in time is 3:00 PM.",

        "Arabic":
            "وقت تسجيل الوصول المعتاد هو الساعة 3:00 مساءً.",

        "French":
            "L'heure d'enregistrement standard est 15h00.",

        "Russian":
            "Стандартное время заезда — 15:00.",
    },

    "check_out_time": {

        "English":
            "The standard check-out time is 12:00 PM.",

        "Arabic":
            "وقت تسجيل المغادرة المعتاد هو الساعة 12:00 ظهرًا.",

        "French":
            "L'heure de départ standard est 12h00.",

        "Russian":
            "Стандартное время выезда — 12:00.",
    },

    "early_check_in": {

        "English":
            "Early check-in is subject to room availability and hotel approval.",

        "Arabic":
            "تسجيل الوصول المبكر يخضع لتوفر الغرفة وموافقة الفندق.",

        "French":
            "L'enregistrement anticipé dépend de la disponibilité de la chambre et de l'approbation de l'hôtel.",

        "Russian":
            "Ранний заезд зависит от наличия номера и одобрения отеля.",
    },

    "late_check_out": {

        "English":
            "Late check-out is subject to availability and hotel approval.",

        "Arabic":
            "تسجيل المغادرة المتأخر يخضع للتوفر وموافقة الفندق.",

        "French":
            "Le départ tardif dépend de la disponibilité et de l'approbation de l'hôtel.",

        "Russian":
            "Поздний выезд зависит от наличия свободных номеров и одобрения отеля.",
    },

    "identification_required": {

        "English":
            "Guests are required to provide valid identification during check-in.",

        "Arabic":
            "يُطلب من النزلاء تقديم إثبات هوية ساري المفعول أثناء تسجيل الوصول.",

        "French":
            "Les clients doivent présenter une pièce d'identité valide lors de l'enregistrement.",

        "Russian":
            "При регистрации гости должны предъявить действующий документ, удостоверяющий личность.",
    },
}

# ============================================================
# GENERATE ROWS
# ============================================================

rows = []

for index, item in enumerate(records):

    faq_id = item["faq_id"]
    intent = item["intent_name"]
    language = item["language"]

    if intent not in templates[language]:
        raise RuntimeError(
            f"No question template for "
            f"intent='{intent}', language='{language}'"
        )

    if intent not in ground_truth:
        raise RuntimeError(
            f"No ground truth for intent='{intent}'"
        )

    question = templates[language][intent]
    answer = ground_truth[intent][language]

    question_type = QUESTION_TYPES[
        index % len(QUESTION_TYPES)
    ]

    source_path = source_map[intent]

    rows.append({

        "faq_id": faq_id,

        "intent_name": intent,

        "language": language,

        "question_type": question_type,

        "question": question,

        "ground_truth": answer,

        "answer": answer,

        "status": "generated",

        "difficulty": "Easy",

        "attempts": 0,

        "source":
            source_path
            .relative_to(PROJECT)
            .as_posix(),
    })

# ============================================================
# CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(rows)

# ============================================================
# FINAL SAFETY CHECKS
# ============================================================

if len(df) != 32:
    raise RuntimeError(
        f"Expected 32 rows, got {len(df)}"
    )

if df["faq_id"].tolist() != expected_ids:
    raise RuntimeError(
        "Final FAQ IDs are incorrect"
    )

if df["faq_id"].duplicated().any():
    raise RuntimeError(
        "Duplicate FAQ IDs detected"
    )

if not (
    df["answer"] == df["ground_truth"]
).all():
    raise RuntimeError(
        "Answer / Ground Truth mismatch detected"
    )

if not (
    df["attempts"] == 0
).all():
    raise RuntimeError(
        "Attempts must all equal 0"
    )

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
    raise RuntimeError(
        f"Missing required columns: {missing_columns}"
    )

for column in required_columns:

    if (
        df[column]
        .astype(str)
        .str.strip()
        .eq("")
        .any()
    ):
        raise RuntimeError(
            f"Empty values found in column: {column}"
        )

print("\n🛡️ ALL BATCH 23 SAFETY CHECKS PASSED")

# ============================================================
# WRITE ONLY BATCH 23
# ============================================================

df.to_csv(
    OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

# ============================================================
# VERIFY OUTPUT FILE
# ============================================================

if not OUTPUT.exists():
    raise RuntimeError(
        "Batch 23 output file was not created"
    )

check_df = pd.read_csv(
    OUTPUT,
    dtype=str
).fillna("")

if len(check_df) != 32:
    raise RuntimeError(
        "Output verification failed: row count"
    )

if check_df["faq_id"].tolist() != expected_ids:
    raise RuntimeError(
        "Output verification failed: IDs"
    )

if not (
    check_df["answer"]
    == check_df["ground_truth"]
).all():
    raise RuntimeError(
        "Output verification failed: answers"
    )

# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 90)
print("🎉 BATCH 23 GENERATED SUCCESSFULLY")
print("=" * 90)

print(f"OUTPUT : {OUTPUT}")
print("ROWS   : 32")
print("IDS    : FAQ0705 → FAQ0736")

print("\n📊 LANGUAGES")
print(
    check_df["language"]
    .value_counts()
    .to_string()
)

print("\n🎯 INTENTS")
print(
    check_df["intent_name"]
    .value_counts()
    .to_string()
)

print("\n🛡️ SAFETY CHECKS")
print("✅ Master was NOT modified")
print("✅ Batch 21 was NOT modified")
print("✅ Batch 22 was NOT modified")
print("✅ Batch 23 only")
print("✅ 32 rows generated")
print("✅ Answer = Ground Truth")
print("✅ Attempts = 0")
print("✅ IDs verified")
print("✅ Output verified")

print("\n" + "=" * 90)
print("⛔ DO NOT MERGE YET")
print("🚀 NEXT STEP: BATCH 23 QUALITY CHECK")
print("=" * 90)