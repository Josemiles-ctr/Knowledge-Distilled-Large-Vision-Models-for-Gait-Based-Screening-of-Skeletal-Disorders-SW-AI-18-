#!/usr/bin/env python3
"""
Quick endpoint tester for GaitLab API.
Run against local development or remote Render deployment.
"""
import requests
import json
import sys
from pathlib import Path

# Configuration
BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
VIDEO_FILE = sys.argv[2] if len(sys.argv) > 2 else "RA1.mp4"

print(f"\n📋 Testing GaitLab API endpoints at: {BASE_URL}\n")

# Test 1: Health check
print("1️⃣  Testing /health...")
try:
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Ready check (should trigger model load)
print("\n2️⃣  Testing /ready (may take 30-60s on first call)...")
try:
    r = requests.get(f"{BASE_URL}/ready", timeout=90)
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: List conditions
print("\n3️⃣  Testing /conditions...")
try:
    r = requests.get(f"{BASE_URL}/conditions", timeout=5)
    print(f"   Status: {r.status_code}")
    data = r.json()
    if "conditions" in data:
        print(f"   Found {len(data['conditions'])} conditions:")
        for name, desc in list(data['conditions'].items())[:3]:
            print(f"      - {name}: {desc[:50]}...")
    else:
        print(f"   Response: {data}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Predict (optional, requires video file)
if Path(VIDEO_FILE).exists():
    print(f"\n4️⃣  Testing /predict with {VIDEO_FILE}...")
    try:
        with open(VIDEO_FILE, "rb") as f:
            files = {"video": f}
            data = {"clinical_condition": "Patient with knee pain and altered gait pattern"}
            r = requests.post(f"{BASE_URL}/predict", files=files, data=data, timeout=120)
            print(f"   Status: {r.status_code}")
            response = r.json()
            if "predicted_class" in response:
                print(f"   Predicted class: {response['predicted_class']}")
                print(f"   Top 3 probabilities:")
                sorted_probs = sorted(response['probabilities'].items(), key=lambda x: x[1], reverse=True)
                for cls, prob in sorted_probs[:3]:
                    print(f"      - {cls}: {prob:.4f}")
            else:
                print(f"   Response: {response}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
else:
    print(f"\n4️⃣  Skipping /predict test (video file '{VIDEO_FILE}' not found)")

print("\n✅ Test complete!\n")
