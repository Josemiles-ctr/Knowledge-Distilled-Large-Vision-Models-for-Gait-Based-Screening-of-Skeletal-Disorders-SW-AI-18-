import torch
import cv2
import numpy as np
from decord import VideoReader, cpu

def process_video(video_path, num_frames=16, frame_size=224):
    vr = VideoReader(video_path, ctx=cpu(0))
    total_frames = len(vr)
    
    if total_frames <= num_frames:
        frame_indices = list(range(total_frames))
        while len(frame_indices) < num_frames:
            frame_indices.append(frame_indices[-1])
    else:
        frame_indices = np.linspace(0, total_frames-1, num_frames, dtype=int)

    frames = vr.get_batch(frame_indices).asnumpy()
    resized_frames = [cv2.resize(f, (frame_size, frame_size)) for f in frames]
    frames = np.array(resized_frames)

    tensor = torch.from_numpy(frames).permute(3,0,1,2).float()
    if tensor.max() > 1.0:
        tensor = tensor / 255.0

    mean = torch.tensor([0.485,0.456,0.406]).view(3,1,1,1)
    std = torch.tensor([0.229,0.224,0.225]).view(3,1,1,1)
    tensor = (tensor - mean) / std
    return tensor.unsqueeze(0) # Add batch dimension
