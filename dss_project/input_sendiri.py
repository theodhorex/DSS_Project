"""Input manual interaktif untuk DSS prediction.
Jalankan: python input_sendiri.py
"""

import requests
import json

BASE = "http://localhost:5000"

# Cek koneksi dulu
try:
    r = requests.get(f"{BASE}/health", timeout=3)
    if not r.ok:
        print(f"Server error: {r.status_code}")
        exit(1)
except:
    print("Flask tidak terdeteksi. Jalankan 'python app.py' dulu.")
    exit(1)

print("=" * 55)
print("  INPUT SENDIRI — DSS Prediction")
print("=" * 55)

fields = [
    ("reward_score",     "Apresiasi Diri (0-10, step 0.5)",       "5"),
    ("mood_state",       "Kondisi Mood (Calm/Neutral/Tense/Fatigued)", "Neutral"),
    ("exam_pressure",    "Tekanan Ujian (0-10)",                   "5"),
    ("assignment_load",  "Beban Tugas (0-10)",                     "5"),
    ("study_hours",      "Jam Belajar (0-24, step 0.5)",           "4"),
    ("attendance",       "Kehadiran (0-100)",                      "80"),
    ("sleep_hours",      "Jam Tidur (0-24, step 0.5)",             "7"),
    ("heart_rate",       "Detak Jantung (40-200)",                 "80"),
    ("physical_activity","Aktivitas Fisik (0-10)",                 "5"),
    ("screen_time",      "Screen Time (0-24, step 0.5)",           "6"),
    ("social_support",   "Dukungan Sekitar (0-10)",                "5"),
    ("facial_emotion",   "Ekspresi Wajah (Neutral/Happy/Sad/Angry/Surprised)", "Neutral"),
    ("caffeine_intake",  "Konsumsi Kafein (0-10, step 0.5)",       "3"),
]

payload = {}
for key, label, default in fields:
    prompt = f"  {label} [{default}]: "
    val = input(prompt).strip()
    if val == "":
        val = default
    # Convert tipe data
    if key in ("mood_state", "facial_emotion"):
        payload[key] = val
    elif "." in val:
        payload[key] = float(val)
    else:
        try:
            payload[key] = int(val)
        except:
            payload[key] = float(val)

print("\nMengirim prediksi...")
r = requests.post(f"{BASE}/predict", json=payload, timeout=10)

if not r.ok:
    print(f"Error HTTP {r.status_code}: {r.text[:300]}")
    exit(1)

data = r.json()
if not data.get("success"):
    print(f"Error: {data.get('error', '?')}")
    exit(1)

preds = data["predictions"]
conf = data["confidence"]
paths = data.get("decision_paths", {})

print("\n" + "=" * 55)
print("  HASIL PREDIKSI")
print("=" * 55)
print(f"  Stress_Level:           {preds.get('stress_level', '?'):>8}")
print(f"  Anxiety_Level:          {preds.get('anxiety_level', '?'):>8}")
print(f"  Final_State:            {preds.get('final_state', '?'):>8}")
print(f"  Intervention_Response:  {preds.get('intervention_response', '?'):>8}")
print(f"  Confidence:             {conf * 100:.0f}%")
print()
print(f"  {data.get('explanation', '')}")

# Decision paths
for target in ["stress_level", "anxiety_level", "final_state", "intervention_response"]:
    steps = paths.get(target, [])
    if steps:
        label = {"stress_level":"Stres","anxiety_level":"Kecemasan","final_state":"Status Akhir","intervention_response":"Intervensi"}
        print(f"\n  Jalur keputusan — {label.get(target, target)}:")
        for i, step in enumerate(steps, 1):
            print(f"    {i}. {step}")

# Probabilities
probs = data.get("prediction_probabilities", {})
if probs:
    print(f"\n  Probabilitas per kelas:")
    for target, classes in probs.items():
        sorted_c = sorted(classes.items(), key=lambda x: x[1], reverse=True)
        top = sorted_c[0]
        print(f"    {target}: {top[0]} ({top[1]*100:.0f}%)")


# Loop untuk tes lagi
print()
while True:
        lagi = input("Input lagi? (y/n): ").strip().lower()
        if lagi == "y":
            payload = {}
            print()
            for key, label, default in fields:
                prompt = f"  {label} [{default}]: "
                val = input(prompt).strip()
                if val == "":
                    val = default
                if key in ("mood_state", "facial_emotion"):
                    payload[key] = val
                elif "." in val:
                    payload[key] = float(val)
                else:
                    try:
                        payload[key] = int(val)
                    except:
                        payload[key] = float(val)

            print("\nMengirim prediksi...")
            r = requests.post(f"{BASE}/predict", json=payload, timeout=10)
            if not r.ok:
                print(f"Error HTTP {r.status_code}: {r.text[:300]}")
                continue
            data = r.json()
            if not data.get("success"):
                print(f"Error: {data.get('error', '?')}")
                continue
            preds = data["predictions"]
            conf = data["confidence"]
            paths = data.get("decision_paths", {})
            print("\n" + "=" * 55)
            print("  HASIL PREDIKSI")
            print("=" * 55)
            print(f"  Stress_Level:           {preds.get('stress_level', '?'):>8}")
            print(f"  Anxiety_Level:          {preds.get('anxiety_level', '?'):>8}")
            print(f"  Final_State:            {preds.get('final_state', '?'):>8}")
            print(f"  Intervention_Response:  {preds.get('intervention_response', '?'):>8}")
            print(f"  Confidence:             {conf * 100:.0f}%")
            print(f"\n  {data.get('explanation', '')}")
            for target in ["stress_level", "anxiety_level", "final_state", "intervention_response"]:
                steps = paths.get(target, [])
                if steps:
                    label = {"stress_level":"Stres","anxiety_level":"Kecemasan","final_state":"Status Akhir","intervention_response":"Intervensi"}
                    print(f"\n  Jalur keputusan — {label.get(target, target)}:")
                    for i, step in enumerate(steps, 1):
                        print(f"    {i}. {step}")
            probs = data.get("prediction_probabilities", {})
            if probs:
                print(f"\n  Probabilitas per kelas:")
                for target, classes in probs.items():
                    sorted_c = sorted(classes.items(), key=lambda x: x[1], reverse=True)
                    top = sorted_c[0]
                    print(f"    {target}: {top[0]} ({top[1]*100:.0f}%)")
            print()
        elif lagi == "n":
            print("Selesai.")
            break
