import torch
import cv2
import numpy as np
from decord import VideoReader, cpu
import gc
import logging

logger = logging.getLogger(__name__)

def process_video(video_path, num_frames=16, frame_size=224, chunk_size=4):
    """
    Process video with memory optimization.
    Streams frames in chunks instead of loading all at once.
    
    Args:
        video_path: Path to video file
        num_frames: Number of frames to extract
        frame_size: Size to resize frames to
        chunk_size: Process frames in batches of this size
    
    Returns:
        torch.Tensor: Normalized video tensor (1, C, T, H, W)
    """
    vr = VideoReader(video_path, ctx=cpu(0))
    total_frames = len(vr)
    
    if total_frames <= num_frames:
        frame_indices = list(range(total_frames))
        while len(frame_indices) < num_frames:
            frame_indices.append(frame_indices[-1])
    else:
        frame_indices = np.linspace(0, total_frames-1, num_frames, dtype=int)

    # Process frames in chunks to minimize memory usage
    frames_list = []
    for i in range(0, len(frame_indices), chunk_size):
        batch_indices = frame_indices[i:i+chunk_size]
        frames = vr.get_batch(batch_indices).asnumpy()
        
        resized_frames = [cv2.resize(f, (frame_size, frame_size)) for f in frames]
        frames_list.extend(resized_frames)
        
        # Clear intermediate data
        del frames
        gc.collect()
    
    frames = np.array(frames_list)
    
    # Normalize to float in range [0, 1]
    tensor = torch.from_numpy(frames).permute(3,0,1,2).float()
    if tensor.max() > 1.0:
        tensor = tensor / 255.0

    # Apply ImageNet normalization
    mean = torch.tensor([0.485,0.456,0.406]).view(3,1,1,1)
    std = torch.tensor([0.229,0.224,0.225]).view(3,1,1,1)
    tensor = (tensor - mean) / std
    
    # Cleanup
    del frames
    gc.collect()
    
    return tensor.unsqueeze(0)  # Add batch dimension
