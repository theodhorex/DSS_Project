"""End-to-end QA test runner for DSS Flask application."""
import json
import os
import subprocess
import sys
import time
import traceback
from datetime import datetime

import joblib
import pandas as pd
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_PYTHON = os.path.join(BASE_DIR, "venv", "Scripts", "python.exe")
FLASK_URL = "http://localhost:5000"
RESULTS_FILE = os.path.join(
    os.environ.get("TEMP", "C:\\Users\\Nino\\AppData\\Local\\Temp"),
    "opencode",
    "qa_report.md",
)

results = []
server_proc = None


def report(tc_id, name, status, http_code=None, output_summary="", notes=""):
    results.append({
        "tc_id": tc_id,
        "name": name,
        "status": status,
        "http_code": http_code,
        "output_summary": output_summary,
        "notes": notes,
    })


def start_server():
    global server_proc
    server_proc = subprocess.Popen(
        [VENV_PYTHON, "app.py"],
        cwd=BASE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    for i in range(30):
        try:
            r = requests.get(f"{FLASK_URL}/", timeout=2)
            if r.status_code == 200:
                print(f"[SETUP] Server started (attempt {i+1})")
                return True
        except requests.ConnectionError:
            pass
        time.sleep(1)
    return False


def stop_server():
    global server_proc
    if server_proc:
        server_proc.terminate()
        server_proc.wait(timeout=5)
        server_proc = None


def do_get(path):
    try:
        r = requests.get(f"{FLASK_URL}{path}", timeout=10)
        return r.status_code, r.text[:200]
    except Exception as e:
        return 0, str(e)


def do_post(payload):
    try:
        r = requests.post(
            f"{FLASK_URL}/predict",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        data = None
        try:
            data = r.json()
        except Exception:
            data = r.text[:200]
        return r.status_code, data
    except Exception as e:
        return 0, str(e)


# ------------------------------------------------------------------ #
#  TEST GROUP 1 — API Health Check
# ------------------------------------------------------------------ #
def test_tc01():
    code, body = do_get("/")
    ok = code == 200
    report("TC-01", "GET /", "PASS" if ok else "FAIL", code, f"Body length={len(body)}", "" if ok else f"Expected 200, got {code}")


def test_tc02():
    code, data = do_post({})
    ok = code in (400, 422)
    report("TC-02", "POST /predict with {}", "PASS" if ok else "FAIL", code, str(data)[:100], "" if ok else f"Expected 400/422, got {code}")


def test_tc03():
    results_tmp = []
    for path, label in [("/static/css/style.css", "style.css"), ("/static/js/script.js", "script.js")]:
        code, body = do_get(path)
        ok = code == 200
        results_tmp.append(("PASS" if ok else "FAIL", code, label))
    status = "PASS" if all(r[0] == "PASS" for r in results_tmp) else "FAIL"
    summary = "; ".join(f"{r[2]}: HTTP {r[1]}" for r in results_tmp)
    report("TC-03", "Static files", status, code, summary, "" if status == "PASS" else "Some static files not found")


# ------------------------------------------------------------------ #
#  TEST GROUP 2 — Input Validation
# ------------------------------------------------------------------ #
def test_tc04():
    code, data = do_post({})
    ok = code == 400 and ("Missing" in str(data) or "missing" in str(data).lower())
    report("TC-04", "Missing fields", "PASS" if ok else "FAIL", code, str(data)[:150], "" if ok else f"Expected 400 with missing field error")


def test_tc05():
    payload = {"exam_pressure":7,"sleep_hours":6,"social_support":5,"heart_rate":80,"physical_activity":5,"assignment_load":7,"study_hours":8,"attendance":75,"screen_time":6,"facial_emotion":"Neutral","mood_state":"Neutral","reward_score":5}
    code, data = do_post(payload)
    ok = code == 400 and "caffeine_intake" in str(data)
    report("TC-05", "Missing caffeine_intake", "PASS" if ok else "FAIL", code, str(data)[:150], "" if ok else f"Expected 400 mentioning caffeine_intake")


def test_tc06():
    payload = {"exam_pressure":5,"sleep_hours":6,"social_support":5,"heart_rate":80,"physical_activity":5,"assignment_load":5,"study_hours":7,"attendance":70,"screen_time":5,"caffeine_intake":5,"facial_emotion":"Neutral","mood_state":"Neutral","reward_score":15}
    code, data = do_post(payload)
    ok = code in (400, 422)
    report("TC-06", "reward_score out of range", "PASS" if ok else "FAIL", code, str(data)[:150], "" if ok else f"Expected 400/422, got {code}")


def test_tc07():
    payload = {"exam_pressure":5,"sleep_hours":6,"social_support":5,"heart_rate":80,"physical_activity":5,"assignment_load":5,"study_hours":7,"attendance":70,"screen_time":5,"caffeine_intake":5,"facial_emotion":"Neutral","mood_state":"Excited","reward_score":5}
    code, data = do_post(payload)
    ok = code != 500
    report("TC-07", "Invalid mood_state 'Excited'", "PASS" if ok else "FAIL", code, str(data)[:150], "" if ok else f"Got 500 (server error)")


def test_tc08():
    payload = {"exam_pressure":5,"sleep_hours":6,"social_support":5,"heart_rate":80,"physical_activity":5,"assignment_load":5,"study_hours":7,"attendance":70,"screen_time":5,"caffeine_intake":5,"facial_emotion":"Neutral","mood_state":"Neutral","reward_score":5,"stress_score":50}
    code, data = do_post(payload)
    ok = code == 200 or code == 400
    report("TC-08", "Extra field stress_score:50", "PASS" if ok else "FAIL", code, str(data)[:150], f"Got {code} (allowed: 200 or 400)")


# ------------------------------------------------------------------ #
#  TEST GROUP 3 — Prediction Output Validation
# ------------------------------------------------------------------ #
def test_tc09():
    payload = {"exam_pressure":10,"sleep_hours":3,"social_support":1,"heart_rate":120,"physical_activity":1,"assignment_load":10,"study_hours":14,"attendance":40,"screen_time":12,"caffeine_intake":9,"facial_emotion":"Angry","mood_state":"Tense","reward_score":1}
    code, data = do_post(payload)
    notes = []
    if code != 200:
        notes.append(f"Expected 200 got {code}")
    else:
        d = data if isinstance(data, dict) else {}
        if d.get("predictions", {}).get("stress_level") != "High":
            notes.append("stress_level not High")
        if d.get("predictions", {}).get("anxiety_level") != "High":
            notes.append("anxiety_level not High (may be ok)")
        conf = d.get("confidence", 0)
        if conf <= 0.0:
            notes.append("confidence <= 0")
        expl = d.get("explanation", "")
        if not expl:
            notes.append("explanation empty")
    status = "PASS" if not notes else ("FAIL" if "Expected 200 got" in notes[0] else "WARN")
    report("TC-09", "High stress prediction", status, code, json.dumps(data if isinstance(data, dict) else {})[:200], "; ".join(notes))


def test_tc10():
    payload = {"exam_pressure":1,"sleep_hours":8,"social_support":9,"heart_rate":65,"physical_activity":8,"assignment_load":2,"study_hours":4,"attendance":95,"screen_time":2,"caffeine_intake":1,"facial_emotion":"Happy","mood_state":"Calm","reward_score":9}
    code, data = do_post(payload)
    notes = []
    if code != 200:
        notes.append(f"Expected 200 got {code}")
    else:
        d = data if isinstance(data, dict) else {}
        if d.get("predictions", {}).get("stress_level") != "Low":
            notes.append("stress_level not Low (may be ok)")
    status = "PASS" if not notes else "WARN"
    report("TC-10", "Low stress prediction", status, code, json.dumps(data if isinstance(data, dict) else {})[:200], "; ".join(notes))


def test_tc11():
    payload = {"exam_pressure":5,"sleep_hours":6,"social_support":5,"heart_rate":85,"physical_activity":5,"assignment_load":5,"study_hours":7,"attendance":70,"screen_time":5,"caffeine_intake":5,"facial_emotion":"Neutral","mood_state":"Neutral","reward_score":5}
    code, data = do_post(payload)
    notes = []
    if code != 200:
        notes.append(f"Expected 200 got {code}")
    else:
        d = data if isinstance(data, dict) else {}
        preds = d.get("predictions", {})
        for t in ["stress_level", "anxiety_level", "final_state", "intervention_response"]:
            if t not in preds:
                notes.append(f"Missing prediction: {t}")
    status = "PASS" if not notes else "FAIL"
    report("TC-11", "Medium/borderline prediction", status, code, json.dumps(data if isinstance(data, dict) else {})[:200], "; ".join(notes))


def test_tc12():
    payload = {"exam_pressure":0,"sleep_hours":0,"social_support":0,"heart_rate":40,"physical_activity":0,"assignment_load":0,"study_hours":0,"attendance":0,"screen_time":0,"caffeine_intake":0,"facial_emotion":"Sad","mood_state":"Fatigued","reward_score":0}
    code, data = do_post(payload)
    ok = code == 200
    report("TC-12", "All minimum values", "PASS" if ok else "FAIL", code, str(data)[:150], "" if ok else f"Server crashed? Got {code}")


def test_tc13():
    payload = {"exam_pressure":10,"sleep_hours":24,"social_support":10,"heart_rate":200,"physical_activity":10,"assignment_load":10,"study_hours":24,"attendance":100,"screen_time":24,"caffeine_intake":10,"facial_emotion":"Surprised","mood_state":"Tense","reward_score":10}
    code, data = do_post(payload)
    ok = code == 200
    report("TC-13", "All maximum values", "PASS" if ok else "FAIL", code, str(data)[:150], "" if ok else f"Server crashed? Got {code}")


# ------------------------------------------------------------------ #
#  TEST GROUP 4 — Explanation Text Validation
# ------------------------------------------------------------------ #
def test_tc14():
    payload = {"exam_pressure":10,"sleep_hours":3,"social_support":1,"heart_rate":120,"physical_activity":1,"assignment_load":10,"study_hours":14,"attendance":40,"screen_time":12,"caffeine_intake":9,"facial_emotion":"Angry","mood_state":"Tense","reward_score":1}
    code, data = do_post(payload)
    notes = []
    if code != 200:
        notes.append(f"Expected 200 got {code}")
    else:
        d = data if isinstance(data, dict) else {}
        expl = d.get("explanation", "")
        if not expl:
            notes.append("Explanation is empty")
        elif "stres tinggi" not in expl.lower() and "tingkat stres tinggi" not in expl.lower() and "terdeteksi tingkat stres tinggi" not in expl.lower():
            notes.append(f"Explanation doesn't contain Indonesian stress text: {expl[:100]}")
    status = "PASS" if not notes else "FAIL"
    report("TC-14", "Explanation for high stress - Bahasa", status, code, (data.get("explanation", "") if isinstance(data, dict) else "")[:150], "; ".join(notes))


def test_tc15():
    payload = {"exam_pressure":1,"sleep_hours":8,"social_support":9,"heart_rate":65,"physical_activity":8,"assignment_load":2,"study_hours":4,"attendance":95,"screen_time":2,"caffeine_intake":1,"facial_emotion":"Happy","mood_state":"Calm","reward_score":9}
    code, data = do_post(payload)
    notes = []
    if code != 200:
        notes.append(f"Expected 200 got {code}")
    else:
        d = data if isinstance(data, dict) else {}
        expl = d.get("explanation", "")
        if not expl:
            notes.append("Explanation is empty")
        elif "stres" not in expl.lower() and "rendah" not in expl.lower() and "rileks" not in expl.lower():
            notes.append(f"Explanation lacks expected Indonesian keywords: {expl[:100]}")
    status = "PASS" if not notes else "FAIL"
    report("TC-15", "Explanation for low stress - Bahasa", status, code, (data.get("explanation", "") if isinstance(data, dict) else "")[:150], "; ".join(notes))


# ------------------------------------------------------------------ #
#  TEST GROUP 5 — Model File Integrity
# ------------------------------------------------------------------ #
def test_tc16():
    try:
        model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
        model_type = type(model).__name__
        report("TC-16", "Load model.pkl type check", "PASS", None, f"Type: {model_type}", "")
    except Exception as e:
        report("TC-16", "Load model.pkl type check", "FAIL", None, str(e), traceback.format_exc())


def test_tc17():
    try:
        model = joblib.load(os.path.join(BASE_DIR, "model.pkl"))
        dummy = pd.DataFrame([{
            "Exam_Pressure": 5, "Sleep_Hours": 6, "Social_Support": 5,
            "Heart_Rate": 80, "Physical_Activity": 5, "Assignment_Load": 5,
            "Study_Hours": 7, "Attendance": 70, "Screen_Time": 5,
            "Caffeine_Intake": 5, "Facial_Emotion": "Neutral",
            "Mood_State": "Neutral", "Reward_Score": 5,
        }])
        pred = model.predict(dummy)
        shape_ok = pred.shape == (1, 4)
        report("TC-17", "Predict with model.pkl", "PASS" if shape_ok else "WARN", None, f"Shape: {pred.shape}", "" if shape_ok else f"Expected (1,4), got {pred.shape}")
    except Exception as e:
        report("TC-17", "Predict with model.pkl", "FAIL", None, str(e), traceback.format_exc())


# ------------------------------------------------------------------ #
#  MAIN
# ------------------------------------------------------------------ #
def main():
    print("=" * 60)
    print("DSS PROJECT - END-TO-END QA TEST RUNNER")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 60)

    # Start server
    print("\n[SETUP] Starting Flask server...")
    if not start_server():
        print("[SETUP] FAILED to start server. Some tests will be skipped.")
    else:
        print("[SETUP] Server is running.")

    # Run tests
    test_tc01()
    test_tc02()
    test_tc03()
    test_tc04()
    test_tc05()
    test_tc06()
    test_tc07()
    test_tc08()
    test_tc09()
    test_tc10()
    test_tc11()
    test_tc12()
    test_tc13()
    test_tc14()
    test_tc15()
    test_tc16()
    test_tc17()

    # Stop server
    stop_server()

    # Generate report
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    warned = sum(1 for r in results if r["status"] == "WARN")

    report_lines = []
    report_lines.append("# QA Test Report — DSS Prediction API")
    report_lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"**Server URL:** {FLASK_URL}")
    report_lines.append(f"**Model file:** model.pkl")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## Test Results")
    report_lines.append("")
    report_lines.append("| TC ID | Test Name | Status | HTTP | Output Summary | Notes |")
    report_lines.append("|-------|-----------|--------|------|----------------|-------|")

    for r in results:
        tc_id = r["tc_id"]
        name = r["name"]
        status = r["status"]
        http = str(r["http_code"]) if r["http_code"] else "N/A"
        out = (r["output_summary"] or "").replace("\n", " ").replace("|", "/")[:120]
        notes = (r["notes"] or "-").replace("\n", " ").replace("|", "/")[:120]
        report_lines.append(f"| {tc_id} | {name} | {status} | {http} | {out} | {notes} |")

    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## Summary")
    report_lines.append("")
    report_lines.append(f"- **Total:** {len(results)}")
    report_lines.append(f"- **Passed:** {passed}")
    report_lines.append(f"- **Failed:** {failed}")
    report_lines.append(f"- **Warnings:** {warned}")
    report_lines.append(f"- **Pass Rate:** {passed/len(results)*100:.1f}%")
    report_lines.append("")

    if failed > 0 or warned > 0:
        report_lines.append("## Issues Found")
        report_lines.append("")
        for r in results:
            if r["status"] in ("FAIL", "WARN"):
                report_lines.append(f"- **{r['tc_id']}** ({r['name']}): {r['notes']}")
        report_lines.append("")

    report_text = "\n".join(report_lines)

    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    with open(RESULTS_FILE, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"\n[REPORT] Written to {RESULTS_FILE}")
    print(report_text)


if __name__ == "__main__":
    main()
