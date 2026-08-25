import pandas as pd
from pathlib import Path

PROJECT = Path(r"C:\Users\n3101\OneDrive\Desktop\HotelAI-Intelligent-Agent")

BATCH = (
    PROJECT
    / "03_Structured_Data"
    / "CSV"
    / "batches"
    / "hotel_faq_batch24.csv"
)

df = pd.read_csv(BATCH, dtype=str).fillna("")

content = {

"hotel_location": {
"English": (
"Where is Nile Pearl Hotel located?",
"Cairo, Egypt."
),
"Arabic": (
"أين يقع فندق نايل بيرل؟",
"يقع فندق نايل بيرل في القاهرة، مصر."
),
"French": (
"Où se trouve le Nile Pearl Hotel ?",
"Le Nile Pearl Hotel est situé au Caire, en Égypte."
),
"Russian": (
"Где находится отель Nile Pearl?",
"Отель Nile Pearl находится в Каире, Египет."
),
},

"hotel_category": {
"English": (
"What category is Nile Pearl Hotel?",
"Nile Pearl Hotel is a 5-Star Hotel."
),
"Arabic": (
"ما هي فئة فندق نايل بيرل؟",
"فندق نايل بيرل هو فندق 5 نجوم."
),
"French": (
"Quelle est la catégorie du Nile Pearl Hotel ?",
"Le Nile Pearl Hotel est un hôtel 5 étoiles."
),
"Russian": (
"Какой категории отель Nile Pearl?",
"Nile Pearl Hotel — пятизвездочный отель."
),
},

"reception_availability": {
"English": (
"Is the hotel reception available 24/7?",
"Yes. Hotel reception operates 24/7."
),
"Arabic": (
"هل مكتب الاستقبال متاح على مدار الساعة؟",
"نعم. يعمل مكتب الاستقبال في الفندق على مدار 24 ساعة طوال أيام الأسبوع."
),
"French": (
"La réception de l'hôtel est-elle ouverte 24h/24 et 7j/7 ?",
"Oui. La réception de l'hôtel fonctionne 24h/24 et 7j/7."
),
"Russian": (
"Работает ли стойка регистрации круглосуточно?",
"Да. Стойка регистрации отеля работает круглосуточно."
),
},

"check_in_time": {
"English": (
"What time is standard check-in?",
"Standard check-in time is 3:00 PM."
),
"Arabic": (
"ما هو وقت تسجيل الوصول المعتاد؟",
"وقت تسجيل الوصول المعتاد هو الساعة 3:00 مساءً."
),
"French": (
"À quelle heure est l'enregistrement standard ?",
"L'heure d'enregistrement standard est 15h00."
),
"Russian": (
"Во сколько начинается стандартная регистрация заезда?",
"Стандартное время заезда — 15:00."
),
},

"check_out_time": {
"English": (
"What time is standard check-out?",
"Standard check-out time is 12:00 PM."
),
"Arabic": (
"ما هو وقت تسجيل المغادرة المعتاد؟",
"وقت تسجيل المغادرة المعتاد هو الساعة 12:00 ظهرًا."
),
"French": (
"À quelle heure est le départ standard ?",
"L'heure de départ standard est 12h00."
),
"Russian": (
"Во сколько происходит стандартная регистрация выезда?",
"Стандартное время выезда — 12:00."
),
},

"early_check_in": {
"English": (
"Can I check in early?",
"Early check-in is subject to room availability and hotel approval."
),
"Arabic": (
"هل يمكنني تسجيل الوصول مبكرًا؟",
"تسجيل الوصول المبكر يخضع لتوافر الغرفة وموافقة الفندق."
),
"French": (
"Puis-je m'enregistrer plus tôt ?",
"L'enregistrement anticipé dépend de la disponibilité de la chambre et de l'approbation de l'hôtel."
),
"Russian": (
"Можно ли заселиться раньше?",
"Ранний заезд зависит от наличия свободного номера и одобрения отеля."
),
},

"late_check_out": {
"English": (
"Can I check out late?",
"Late check-out is subject to availability and may incur an additional fee."
),
"Arabic": (
"هل يمكنني تسجيل المغادرة متأخرًا؟",
"تسجيل المغادرة المتأخر يخضع للتوافر وقد تترتب عليه رسوم إضافية."
),
"French": (
"Puis-je effectuer un départ tardif ?",
"Le départ tardif dépend des disponibilités et peut entraîner des frais supplémentaires."
),
"Russian": (
"Можно ли оформить поздний выезд?",
"Поздний выезд зависит от наличия мест и может потребовать дополнительной платы."
),
},

"identification_required": {
"English": (
"Do I need valid identification during check-in?",
"Yes. Guests are required to provide valid identification documents during check-in."
),
"Arabic": (
"هل أحتاج إلى إثبات هوية ساري عند تسجيل الوصول؟",
"نعم. يجب على النزلاء تقديم وثائق هوية سارية أثناء تسجيل الوصول."
),
"French": (
"Dois-je présenter une pièce d'identité valide lors de l'enregistrement ?",
"Oui. Les clients doivent présenter des documents d'identité valides lors de l'enregistrement."
),
"Russian": (
"Нужно ли предъявлять действительное удостоверение личности при регистрации заезда?",
"Да. Гости должны предоставить действительные документы, удостоверяющие личность, при регистрации заезда."
),
},
}

for idx, row in df.iterrows():

    intent = row["intent_name"]
    language = row["language"]

    if intent not in content:
        raise ValueError(f"Unknown intent: {intent}")

    if language not in content[intent]:
        raise ValueError(
            f"Unknown language {language} for {intent}"
        )

    question, answer = content[intent][language]

    df.at[idx, "question"] = question
    df.at[idx, "ground_truth"] = answer
    df.at[idx, "answer"] = answer

    source_map = {
        "hotel_location":
            "02_Hotel_Knowledge/Hotel_Information/hotel_information.txt",
        "hotel_category":
            "02_Hotel_Knowledge/Hotel_Information/hotel_information.txt",
        "reception_availability":
            "02_Hotel_Knowledge/Policies/check_in_check_out.txt",
        "check_in_time":
            "02_Hotel_Knowledge/Policies/check_in_check_out.txt",
        "check_out_time":
            "02_Hotel_Knowledge/Policies/check_in_check_out.txt",
        "early_check_in":
            "02_Hotel_Knowledge/Policies/check_in_check_out.txt",
        "late_check_out":
            "02_Hotel_Knowledge/Policies/check_in_check_out.txt",
        "identification_required":
            "02_Hotel_Knowledge/Policies/identification_policy.txt",
    }

    df.at[idx, "source"] = source_map[intent]
    df.at[idx, "attempts"] = "0"
    df.at[idx, "difficulty"] = "Easy"
    df.at[idx, "status"] = "generated"

df.to_csv(BATCH, index=False, encoding="utf-8-sig")

print("=== BATCH 24 GENERATED ===")
print("Rows:", len(df))
print("First ID:", df["faq_id"].iloc[0])
print("Last ID:", df["faq_id"].iloc[-1])
print("Questions filled:", int((df["question"].str.strip() != "").sum()))
print("Answers filled:", int((df["answer"].str.strip() != "").sum()))
print("Ground Truth filled:", int((df["ground_truth"].str.strip() != "").sum()))
print("Saved:", BATCH)
print("MASTER MODIFIED: NO")
