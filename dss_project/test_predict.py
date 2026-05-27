#!/usr/bin/env python
"""Test prediction endpoint."""

import sys
import json
sys.path.insert(0, '.')

try:
    print("Testing Flask app...")
    from app import app

    test_payload = {
        "stress_score": 65,
        "anxiety_score": 58,
        "exam_pressure": 7,
        "sleep_hours": 5.5,
        "social_support": 6,
        "heart_rate": 82,
        "physical_activity": 3,
        "assignment_load": 8,
        "study_hours": 4,
        "attendance": 85,
        "screen_time": 6.5,
        "facial_emotion": "Neutral",
        "mood_state": "Anxious",
        "intervention_response": "Positive",
        "reward_score": 45
    }

    print("\nTesting /predict endpoint...")
    with app.test_client() as client:
        response = client.post('/predict',
                              json=test_payload,
                              content_type='application/json')
        print(f"[OK] Status: {response.status_code}")
        result = response.json

        print(f"\n[OK] Response keys: {list(result.keys())}")
        print(f"[OK] Success: {result.get('success')}")
        print(f"[OK] Predictions: {result.get('predictions')}")
        print(f"[OK] Confidence: {result.get('confidence')}")
        print(f"[OK] Has preprocessing_steps: {'preprocessing_steps' in result}")
        print(f"[OK] Has prediction_probabilities: {'prediction_probabilities' in result}")
        print(f"[OK] Has decision_paths: {'decision_paths' in result}")

        if 'preprocessing_steps' in result:
            print(f"\n[OK] Preprocessing steps count: {len(result['preprocessing_steps'])}")
            for step in result['preprocessing_steps']:
                print(f"     - Step {step.get('step')}: {step.get('name')}")

        if 'prediction_probabilities' in result:
            print(f"\n[OK] Prediction probabilities targets: {list(result['prediction_probabilities'].keys())}")

        if 'decision_paths' in result:
            print(f"\n[OK] Decision paths targets: {list(result['decision_paths'].keys())}")
            for target, paths in result['decision_paths'].items():
                print(f"     - {target}: {len(paths)} steps")

    print("\n[SUCCESS] Prediction endpoint is working!")

except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
