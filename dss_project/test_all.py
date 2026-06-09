"""Test case otomatis untuk DSS prediction form.
Jalankan dengan: python test_all.py
Pastikan Flask sudah running (python app.py) di terminal lain.
"""

import requests
import json
import sys

BASE = "http://localhost:5000"
PASS = 0
FAIL = 0
ERRORS = []

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

NORMAL = dict(
    reward_score=5, mood_state="Neutral", exam_pressure=5,
    assignment_load=5, study_hours=4, attendance=80, sleep_hours=7,
    heart_rate=80, physical_activity=5, screen_time=6, social_support=5,
    facial_emotion="Neutral", caffeine_intake=3,
)


def test(no, name, payload, expect_success=True, expected=None):
    global PASS, FAIL
    try:
        r = requests.post(f"{BASE}/predict", json=payload, timeout=10)
        ok = r.ok and r.json().get("success") is expect_success
        label = f"{GREEN}PASS{RESET}" if ok else f"{RED}FAIL{RESET}"
        detail = ""
        if r.ok:
            data = r.json()
            preds = data.get("predictions", {})
            conf = data.get("confidence", 0)
            detail = f" | stress={preds.get('stress_level','?')} anxiety={preds.get('anxiety_level','?')} final={preds.get('final_state','?')} conf={conf}"
            if expected and ok:
                for k, v in expected.items():
                    if preds.get(k) != v:
                        ok = False
                        label = f"{RED}FAIL{RESET}"
                        detail += f" | EXPECTED {k}={v} GOT {preds.get(k)}"
        else:
            detail = f" | HTTP {r.status_code}: {r.text[:120]}"
        if ok:
            PASS += 1
        else:
            FAIL += 1
            ERRORS.append(f"TC{no:02d}: {name} -> {detail.strip()}")
        print(f"  {label} TC{no:02d} {name}{detail}")
    except requests.exceptions.ConnectionError:
        FAIL += 1
        ERRORS.append(f"TC{no:02d}: {name} -> CONNECTION REFUSED (Flask running?)")
        print(f"  {RED}FAIL{RESET} TC{no:02d} {name} | {RED}Connection refused{RESET}")


def test_invalid(no, name, payload, expect_field=None):
    global PASS, FAIL
    try:
        r = requests.post(f"{BASE}/predict", json=payload, timeout=10)
        got_error = not r.ok or not r.json().get("success")
        ok = got_error
        label = f"{GREEN}PASS{RESET}" if ok else f"{RED}FAIL{RESET}"
        detail = ""
        if r.ok:
            data = r.json()
            detail = f" | success={data.get('success')}"
            if not data.get("success"):
                detail += f" error={data.get('error','?')}"
        else:
            detail = f" | HTTP {r.status_code}: {r.text[:120]}"
        if ok:
            PASS += 1
        else:
            FAIL += 1
            ERRORS.append(f"TC{no:02d}: {name} -> expected rejection but got success")
        print(f"  {label} TC{no:02d} {name}{detail}")
    except requests.exceptions.ConnectionError:
        FAIL += 1
        ERRORS.append(f"TC{no:02d}: {name} -> CONNECTION REFUSED")
        print(f"  {RED}FAIL{RESET} TC{no:02d} {name} | {RED}Connection refused{RESET}")


print(f"{BOLD}{CYAN}{'='*60}{RESET}")
print(f"{BOLD}{CYAN}   DSS TEST SUITE — 25 Test Cases{RESET}")
print(f"{BOLD}{CYAN}{'='*60}{RESET}")

# ─── HEALTH CHECK ───
try:
    r = requests.get(f"{BASE}/health", timeout=5)
    if r.ok:
        print(f"\n{YELLOW}[INFO]{RESET} Server: {r.json()}")
    else:
        print(f"\n{RED}[ERROR]{RESET} Health check failed: {r.status_code}")
        sys.exit(1)
except requests.exceptions.ConnectionError:
    print(f"\n{RED}[ERROR]{RESET} Cannot connect to Flask at {BASE}")
    print("  Jalankan 'python app.py' di terminal lain dulu.")
    sys.exit(1)


print(f"\n{BOLD}─── HAPPY PATH ───{RESET}")

# TC01 - Low stress (validated)
test(1, "Low Stress Profile", dict(NORMAL,
    reward_score=8, mood_state="Calm", exam_pressure=2, assignment_load=2,
    study_hours=3, attendance=90, sleep_hours=8, heart_rate=70,
    physical_activity=7, screen_time=3, social_support=8,
    facial_emotion="Happy", caffeine_intake=1,
), expected={"stress_level": "Low", "anxiety_level": "Low", "final_state": "Relaxed"})

# TC02 - High stress (validated)
test(2, "High Stress Profile", dict(NORMAL,
    reward_score=2, mood_state="Tense", exam_pressure=9, assignment_load=9,
    study_hours=8, attendance=50, sleep_hours=4, heart_rate=110,
    physical_activity=1, screen_time=10, social_support=2,
    facial_emotion="Sad", caffeine_intake=8,
), expected={"stress_level": "High", "anxiety_level": "High", "final_state": "Stress"})

# TC03 - Medium / borderline
test(3, "Medium Borderline", NORMAL)  # all middle values

# TC04 - All minimum
test(4, "All Minimums", dict(NORMAL,
    reward_score=0, mood_state="Calm", exam_pressure=0, assignment_load=0,
    study_hours=0, attendance=0, sleep_hours=0, heart_rate=40,
    physical_activity=0, screen_time=0, social_support=0,
    facial_emotion="Neutral", caffeine_intake=0,
))

# TC05 - All maximum
test(5, "All Maximums", dict(NORMAL,
    reward_score=10, mood_state="Fatigued", exam_pressure=10, assignment_load=10,
    study_hours=24, attendance=100, sleep_hours=24, heart_rate=200,
    physical_activity=10, screen_time=24, social_support=10,
    facial_emotion="Surprised", caffeine_intake=10,
))


print(f"\n{BOLD}─── BOUNDARY VALUE ANALYSIS ───{RESET}")

# TC06 - Each at minimum (batched)
for field, val in [("reward_score", 0), ("exam_pressure", 0), ("assignment_load", 0),
                   ("study_hours", 0), ("attendance", 0), ("sleep_hours", 0),
                   ("heart_rate", 40), ("physical_activity", 0), ("screen_time", 0),
                   ("social_support", 0), ("caffeine_intake", 0)]:
    p = dict(NORMAL)
    p[field] = val
    test(6, f"Min {field}={val}", p)

# TC07 - Each at maximum (batched)
for field, val in [("reward_score", 10), ("exam_pressure", 10), ("assignment_load", 10),
                   ("study_hours", 24), ("attendance", 100), ("sleep_hours", 24),
                   ("heart_rate", 200), ("physical_activity", 10), ("screen_time", 24),
                   ("social_support", 10), ("caffeine_intake", 10)]:
    p = dict(NORMAL)
    p[field] = val
    test(7, f"Max {field}={val}", p)

# TC08 - Below minimum (should be rejected)
for field, val in [("reward_score", -0.5), ("exam_pressure", -1), ("assignment_load", -1),
                   ("study_hours", -0.5), ("attendance", -1), ("sleep_hours", -0.5),
                   ("heart_rate", 39), ("physical_activity", -1), ("screen_time", -0.5),
                   ("social_support", -1), ("caffeine_intake", -0.5)]:
    p = dict(NORMAL)
    p[field] = val
    test_invalid(8, f"Below min {field}={val}", p)

# TC09 - Above maximum (should be rejected)
for field, val in [("reward_score", 10.5), ("exam_pressure", 11), ("assignment_load", 11),
                   ("study_hours", 24.5), ("attendance", 101), ("sleep_hours", 24.5),
                   ("heart_rate", 201), ("physical_activity", 11), ("screen_time", 24.5),
                   ("social_support", 11), ("caffeine_intake", 10.5)]:
    p = dict(NORMAL)
    p[field] = val
    test_invalid(9, f"Above max {field}={val}", p)


print(f"\n{BOLD}─── NEGATIVE CASES ───{RESET}")

# TC10 - Missing required field
test_invalid(10, "Missing exam_pressure",
    {k: v for k, v in NORMAL.items() if k != "exam_pressure"})

# TC11 - Extra unknown field
test(11, "Has extra unknown field", dict(NORMAL, unknown_field=999))

# TC12 - Invalid mood_state value
test_invalid(12, "Invalid mood_state", dict(NORMAL, mood_state="Anxious"))

# TC13 - Invalid facial_emotion value
test_invalid(13, "Invalid facial_emotion", dict(NORMAL, facial_emotion="Confused"))

# TC14 - Wrong type: string in numeric field
test_invalid(14, "String in exam_pressure", dict(NORMAL, exam_pressure="abc"))


print(f"\n{BOLD}─── EDGE CASES ───{RESET}")

# TC15 - Extreme stress
test(15, "Extreme Stress", dict(NORMAL,
    reward_score=0, mood_state="Tense", exam_pressure=10, assignment_load=10,
    study_hours=10, attendance=20, sleep_hours=2, heart_rate=130,
    physical_activity=0, screen_time=16, social_support=0,
    facial_emotion="Angry", caffeine_intake=10,
), expected={"stress_level": "High", "final_state": "Stress"})

# TC16 - Extreme relaxed
test(16, "Extreme Relaxed", dict(NORMAL,
    reward_score=10, mood_state="Calm", exam_pressure=0, assignment_load=0,
    study_hours=2, attendance=100, sleep_hours=9, heart_rate=55,
    physical_activity=10, screen_time=1, social_support=10,
    facial_emotion="Happy", caffeine_intake=0,
), expected={"stress_level": "Low", "final_state": "Relaxed"})

# TC17 - Heart rate boundaries
test(17, "Heart Rate=40", dict(NORMAL, heart_rate=40))
test(17, "Heart Rate=200", dict(NORMAL, heart_rate=200))

# TC18 - Attendance=0 + high pressure
test(18, "Att=0 + High Pressure", dict(NORMAL,
    attendance=0, exam_pressure=9, assignment_load=8, reward_score=1,
    mood_state="Tense",
))

# TC19 - Sleep=0
test(19, "Sleep Deprivation (0h)", dict(NORMAL,
    sleep_hours=0, exam_pressure=7, assignment_load=7, heart_rate=100,
    reward_score=3, mood_state="Fatigued",
))

# TC20 - All categorical combos (sampling 4 key combos)
for mood in ["Calm", "Neutral", "Tense", "Fatigued"]:
    for face in ["Neutral", "Happy"]:
        test(20, f"Mood={mood} Face={face}", dict(NORMAL, mood_state=mood, facial_emotion=face))

# TC21 - Screen max + activity min
test(21, "Sedentary (screen=24, activity=0)", dict(NORMAL,
    screen_time=24, physical_activity=0, exam_pressure=6, sleep_hours=5,
    reward_score=3, mood_state="Neutral",
))

# TC22 - High caffeine + low sleep
test(22, "High Caffeine + Low Sleep", dict(NORMAL,
    caffeine_intake=10, sleep_hours=2, exam_pressure=8, heart_rate=120,
    mood_state="Tense", reward_score=2,
))

# TC23 - All middle values
test(23, "All Middle Values", dict(NORMAL,
    reward_score=5, mood_state="Neutral", exam_pressure=5, assignment_load=5,
    study_hours=12, attendance=50, sleep_hours=12, heart_rate=120,
    physical_activity=5, screen_time=12, social_support=5,
    facial_emotion="Neutral", caffeine_intake=5,
))

# TC24 - Step 0.5 valid
test(24, "Step 0.5 Values", dict(NORMAL,
    reward_score=3.5, sleep_hours=6.5, study_hours=5.5,
    screen_time=4.5, caffeine_intake=2.5,
))


print(f"\n{BOLD}─── FEATURE IMPORTANCES ───{RESET}")
try:
    r = requests.get(f"{BASE}/feature-importance", timeout=10)
    if r.ok:
        fi = r.json().get("feature_importances", {})
        for target, imps in fi.items():
            print(f"\n  {CYAN}{target}:{RESET}")
            for name, imp in list(imps.items())[:6]:
                print(f"    {name}: {imp:.4f}")
    else:
        print(f"  {RED}Failed to load feature importances{RESET}")
except Exception as e:
    print(f"  {RED}Error: {e}{RESET}")


print(f"\n{BOLD}{'='*60}{RESET}")
print(f"{BOLD}RESULTS:  {GREEN}{PASS} PASS{RESET}  {RED}{FAIL} FAIL{RESET}  out of {PASS+FAIL} tests{RESET}")
if ERRORS:
    print(f"\n{YELLOW}Failed tests:{RESET}")
    for e in ERRORS:
        print(f"  {RED}- {e}{RESET}")
print(f"{BOLD}{'='*60}{RESET}")
