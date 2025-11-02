#!/usr/bin/env python3
"""Test script for GaitLab prediction endpoint."""

import requests
import sys
from pathlib import Path

BASE_URL = "https://knowledge-distilled-large-vision-models-f53p.onrender.com"
VIDEO_PATH = Path("/home/otaijoseph/Downloads/RA1.mp4")


def test_endpoints():
    """Test basic endpoints."""
    print("\n=== Testing Basic Endpoints ===\n")
    
    # Test root
    print("[1] GET / (root)")
    try:
        resp = requests.get(f"{BASE_URL}/", timeout=10)
        print(f"  Status: {resp.status_code}")
        print(f"  Response: {resp.json()}\n")
    except Exception as e:
        print(f"  Error: {e}\n")
    
    # Test health
    print("[2] GET /health")
    try:
        resp = requests.get(f"{BASE_URL}/health", timeout=10)
        print(f"  Status: {resp.status_code}")
        print(f"  Response: {resp.json()}\n")
    except Exception as e:
        print(f"  Error: {e}\n")
    
    # Test readiness
    print("[3] GET /ready")
    try:
        resp = requests.get(f"{BASE_URL}/ready", timeout=10)
        print(f"  Status: {resp.status_code}")
        print(f"  Response: {resp.json()}\n")
    except Exception as e:
        print(f"  Error: {e}\n")


def test_conditions():
    """Test get conditions endpoint."""
    print("\n=== Testing Conditions Endpoint ===\n")
    try:
        resp = requests.get(f"{BASE_URL}/conditions", timeout=10)
        print(f"Status: {resp.status_code}")
        data = resp.json()
        print(f"Available conditions: {list(data.get('conditions', {}).keys())}\n")
    except Exception as e:
        print(f"Error: {e}\n")


def test_predict():
    """Test prediction endpoint with video."""
    if not VIDEO_PATH.exists():
        print(f"\n✗ Video file not found: {VIDEO_PATH}")
        return
    
    print(f"\n=== Testing Prediction Endpoint ===\n")
    print(f"Video: {VIDEO_PATH} ({VIDEO_PATH.stat().st_size / 1024 / 1024:.2f} MB)")
    print("Uploading and processing... (this may take 1-2 minutes on first run)")
    print()
    
    try:
        with open(VIDEO_PATH, "rb") as f:
            files = {
                "video": ("RA1.mp4", f, "video/mp4"),
            }
            data = {
                "clinical_condition": "Mild knee osteoarthritis showing gait asymmetry",
            }
            
            # Allow 5 minutes for model initialization + inference
            resp = requests.post(
                f"{BASE_URL}/predict",
                files=files,
                data=data,
                timeout=300
            )
        
        print(f"Status: {resp.status_code}\n")
        
        if resp.status_code == 200:
            result = resp.json()
            print("✓ Prediction successful!\n")
            print(f"Predicted class: {result.get('predicted_class', 'N/A')}")
            print(f"\nProbabilities:")
            for class_name, prob in result.get("probabilities", {}).items():
                print(f"  {class_name}: {prob:.4f}")
        else:
            print(f"✗ Error: {resp.status_code}")
            print(f"Response: {resp.text[:500]}")
    
    except requests.exceptions.Timeout:
        print("✗ Request timeout (model initialization took too long)")
    except requests.exceptions.ConnectionError as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("GaitLab API Test Suite")
    print("="*60)
    
    test_endpoints()
    test_conditions()
    test_predict()
    
    print("\n" + "="*60)
    print("Testing complete")
    print("="*60 + "\n")
