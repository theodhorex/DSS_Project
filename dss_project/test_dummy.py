"""Dummy test untuk validasi model setelah retraining."""
import json
import requests

BASE = "http://localhost:5000"

# Low stress dummy
low = {
    "exam_pressure": 2, "sleep_hours": 8, "social_support": 8, "heart_rate": 70,
    "physical_activity": 7, "assignment_load": 2, "study_hours": 3, "attendance": 90,
    "screen_time": 3, "caffeine_intake": 1, "facial_emotion": "Happy",
    "mood_state": "Calm", "reward_score": 8,
}

# High stress dummy
high = {
    "exam_pressure": 9, "sleep_hours": 4, "social_support": 2, "heart_rate": 110,
    "physical_activity": 1, "assignment_load": 9, "study_hours": 8, "attendance": 50,
    "screen_time": 10, "caffeine_intake": 8, "facial_emotion": "Sad",
    "mood_state": "Tense", "reward_score": 2,
}

for label, payload in [("LOW", low), ("HIGH", high)]:
    r = requests.post(f"{BASE}/predict", json=payload)
    if r.ok:
        data = r.json()
        print(f"\n=== {label} STRESS DUMMY ===")
        print(f"stress_level={data['predictions']['stress_level']}")
        print(f"anxiety_level={data['predictions']['anxiety_level']}")
        print(f"final_state={data['predictions']['final_state']}")
        print(f"intervention_response={data['predictions']['intervention_response']}")
        print(f"confidence={data['confidence']}")
        print(f"Decision path (stress):")
        for step in data['decision_paths'].get('stress_level', []):
            print(f"  - {step}")
    else:
        print(f"\n=== {label} ERROR ===")
        print(r.text)

# Also fetch feature importances
print("\n\n=== FEATURE IMPORTANCES ===")
r2 = requests.get(f"{BASE}/feature-importance")
if r2.ok:
    fi = r2.json().get("feature_importances", {})
    for target, imps in fi.items():
        print(f"\n{target}:")
        for name, imp in list(imps.items())[:8]:
            print(f"  {name}: {imp:.4f}")
