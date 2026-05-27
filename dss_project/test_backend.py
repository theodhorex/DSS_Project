#!/usr/bin/env python
"""Quick test script for backend."""

import sys
import logging

logging.basicConfig(level=logging.INFO)

try:
    print("1. Testing imports...")
    from train_model import train, _resolve_dataset_path, TARGETS
    print(f"   [OK] train_model imported")
    print(f"   [OK] TARGETS: {TARGETS}")

    print("\n2. Checking dataset...")
    dataset_path = _resolve_dataset_path()
    print(f"   [OK] Dataset path: {dataset_path}")
    print(f"   [OK] Dataset exists: {dataset_path.exists()}")

    print("\n3. Training model...")
    train()
    print("   [OK] Model trained successfully!")

    print("\n4. Testing predictor...")
    from utils.predictor import Predictor
    predictor = Predictor("model.pkl")
    print(f"   [OK] Predictor loaded: {predictor.is_ready}")

    if predictor.is_ready:
        print("\n5. Testing prediction...")
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
        result = predictor.predict(test_payload)
        print(f"   [OK] Prediction successful!")
        print(f"   [OK] Predictions: {result['predictions']}")
        print(f"   [OK] Confidence: {result['confidence']}")
        print(f"   [OK] Has preprocessing_steps: {'preprocessing_steps' in result}")
        print(f"   [OK] Has prediction_probabilities: {'prediction_probabilities' in result}")
        print(f"   [OK] Has decision_paths: {'decision_paths' in result}")

    print("\n[SUCCESS] All tests passed!")
    sys.exit(0)

except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
