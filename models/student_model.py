import torch
import torch.nn as nn
import torch.nn.functional as F

class ClinicalEnhancedStudent(nn.Module):
    def __init__(self, num_classes=9, clinical_dim=768):
        super().__init__()
        self.visual_encoder = nn.Sequential(
            nn.Conv3d(3, 16, kernel_size=(3,3,3), padding=1),
            nn.BatchNorm3d(16), nn.ReLU(), nn.MaxPool3d((1,2,2)),
            nn.Conv3d(16, 32, kernel_size=(3,3,3), padding=1),
            nn.BatchNorm3d(32), nn.ReLU(), nn.MaxPool3d((1,2,2)),
            nn.Conv3d(32, 64, kernel_size=(3,3,3), padding=1),
            nn.BatchNorm3d(64), nn.ReLU(), nn.MaxPool3d((1,2,2)),
            nn.AdaptiveAvgPool3d((None,7,7))
        )
        self.clinical_proj = nn.Linear(clinical_dim, 128)

        # Dummy forward to calculate feature size
        with torch.no_grad():
            dummy = torch.randn(1, 3, 16, 224, 224)
            visual_out = self.visual_encoder(dummy)
            visual_flat_size = visual_out.view(1, -1).shape[-1]

        self.classifier = nn.Sequential(
            nn.Linear(visual_flat_size + 128, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes)
        )

    def forward(self, x, clinical_embeds=None):
        visual_features = self.visual_encoder(x)
        batch_size = visual_features.size(0)
        visual_flat = visual_features.view(batch_size, -1)

        if clinical_embeds is not None:
            clinical_proj = self.clinical_proj(clinical_embeds)
            fused = torch.cat([visual_flat, clinical_proj], dim=1)
        else:
            fused = visual_flat

        return self.classifier(fused)
