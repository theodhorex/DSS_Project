#!/usr/bin/env python
"""Test Flask app startup."""

import sys
sys.path.insert(0, '.')

try:
    print("Testing Flask app import...")
    from app import app, PREDICTOR
    print(f"[OK] Flask app imported")
    print(f"[OK] Predictor ready: {PREDICTOR.is_ready}")

    print("\nTesting /health endpoint...")
    with app.test_client() as client:
        response = client.get('/health')
        print(f"[OK] Status: {response.status_code}")
        print(f"[OK] Response: {response.json}")

    print("\n[SUCCESS] Flask app is working!")

except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
