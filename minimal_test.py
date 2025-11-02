#!/usr/bin/env python3
"""Minimal test of the gait prediction pipeline."""

import sys
import torch
import numpy as np

print("=" * 60)
print("Minimal Pipeline Test")
print("=" * 60)

# Test 1: Config
print("\n[1] Testing config...")
try:
    from app.config import DEVICE, NUM_FRAMES, FRAME_SIZE, CHUNK_SIZE, MODEL_PATH
    print(f"✓ Config loaded: DEVICE={DEVICE}, NUM_FRAMES={NUM_FRAMES}, FRAME_SIZE={FRAME_SIZE}")
except Exception as e:
    print(f"✗ Config failed: {e}")
    sys.exit(1)

# Test 2: Clinical embedder
print("\n[2] Testing clinical embedder...")
try:
    from utils.clinical_utils import ClinicalEmbedder
    embedder = ClinicalEmbedder()
    test_embed = embedder.get_embedding("test condition")
    print(f"✓ Embedder works. Shape: {test_embed.shape}")
except Exception as e:
    print(f"✗ Embedder failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Model loading
print("\n[3] Testing model loading...")
try:
    from models.load_model import load_student_model
    from models.class_mapping import class_mapping
    model = load_student_model(num_classes=len(class_mapping))
    print(f"✓ Model loaded successfully")
except Exception as e:
    print(f"✗ Model loading failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Dummy inference
print("\n[4] Testing dummy inference...")
try:
    # Create dummy video tensor (1, 3, 8, 224, 224) - batch, channels, frames, height, width
    dummy_video = torch.randn(1, 3, NUM_FRAMES, FRAME_SIZE, FRAME_SIZE).to(DEVICE)
    dummy_embed = embedder.get_embedding("dummy condition").to(DEVICE)
    
    print(f"  Video shape: {dummy_video.shape}")
    print(f"  Embed shape: {dummy_embed.shape}")
    
    with torch.no_grad():
        output = model(dummy_video, dummy_embed)
    
    print(f"✓ Inference works. Output shape: {output.shape}")
    
    # Test softmax
    probs = torch.softmax(output, dim=1)
    print(f"✓ Softmax works. Probabilities shape: {probs.shape}")
    print(f"  Sample probabilities: {probs[0, :3].tolist()}")
    
except Exception as e:
    print(f"✗ Inference failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ All tests passed!")
print("=" * 60)
