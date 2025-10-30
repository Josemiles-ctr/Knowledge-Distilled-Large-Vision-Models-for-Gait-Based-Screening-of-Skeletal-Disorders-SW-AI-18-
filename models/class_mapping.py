# model/class_mapping.py

"""
This module defines the clinical descriptions for each gait condition
and provides a consistent mapping from class names to integer indices.
"""

# Clinical descriptions for each gait condition
clinical_descriptions = {
    "Normal": "Normal symmetrical gait pattern with balanced stride length and cadence",
    "KOA_Early": "Early knee osteoarthritis with mild gait modifications and reduced knee flexion",
    "KOA_Mild": "Mild knee osteoarthritis showing limping gait and asymmetric weight bearing",
    "KOA_Severe": "Severe knee osteoarthritis with significant antalgic gait and reduced mobility",
    "PD_Early": "Early Parkinson's disease showing slight shuffling gait and reduced arm swing",
    "PD_Mild": "Mild Parkinson's disease with festinating gait and postural instability",
    "PD_Severe": "Severe Parkinson's disease showing freezing of gait and significant bradykinesia",
    "Disabled_Assistive": "Disabled gait using assistive devices with modified weight distribution",
    "Disabled_NonAssistive": "Disabled gait without assistive devices showing compensatory movements"
}

# Mapping class names to integer indices
# Ensures consistency between training and inference
class_mapping = {name: idx for idx, name in enumerate(clinical_descriptions.keys())}

# Reverse mapping for convenience (index -> class name)
idx_to_class = {idx: name for name, idx in class_mapping.items()}
