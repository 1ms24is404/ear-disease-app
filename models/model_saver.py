"""
Helper script to export models from trained instances.
Run this in your Jupyter Notebook after training to save models for the web app.
"""

import torch
import pickle
import os

def save_vit_model(model, output_path='models/vit_ear_model.pth'):
    """
    Save trained Vision Transformer model to disk.
    
    Usage in Jupyter Notebook:
    >>> from models.model_saver import save_vit_model
    >>> save_vit_model(vit_model)
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save with metadata
    checkpoint = {
        'model_state_dict': model.state_dict(),
        'model_name': 'vit_base_patch16_224',
        'num_classes': 5,
    }
    
    torch.save(checkpoint, output_path)
    print(f"✓ ViT model saved to {output_path}")
    print(f"  File size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")

def save_rf_model(model, output_path='models/symptom_rf_model.pkl'):
    """
    Save trained Random Forest model to disk.
    
    Usage in Jupyter Notebook:
    >>> from models.model_saver import save_rf_model
    >>> save_rf_model(rf_model)
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"✓ Random Forest model saved to {output_path}")
    print(f"  File size: {os.path.getsize(output_path) / (1024*1024):.2f} MB")

def save_label_encoder(label_encoder, output_path='models/label_encoder.pkl'):
    """
    Save label encoder for symptom classification.
    
    Usage in Jupyter Notebook:
    >>> from models.model_saver import save_label_encoder
    >>> save_label_encoder(label_encoder)
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'wb') as f:
        pickle.dump(label_encoder, f)
    
    print(f"✓ Label encoder saved to {output_path}")

def save_all_models(vit_model, rf_model, label_encoder=None):
    """
    Save all models at once.
    
    Usage in Jupyter Notebook:
    >>> from models.model_saver import save_all_models
    >>> save_all_models(vit_model, rf_model, label_encoder)
    """
    print("Saving all models...")
    save_vit_model(vit_model)
    save_rf_model(rf_model)
    if label_encoder is not None:
        save_label_encoder(label_encoder)
    print("✓ All models saved successfully!")

# Instructions for Jupyter Notebook
NOTEBOOK_INSTRUCTIONS = """
# How to export models from Jupyter Notebook

## Step 1: After training your models, run this code:

```python
# Add this at the top of the notebook
import sys
sys.path.append('path/to/ear-disease-app')

# After training, save the models
from models.model_saver import save_all_models

save_all_models(vit_model, rf_model, label_encoder)
```

## Step 2: Verify the files were created:
- models/vit_ear_model.pth
- models/symptom_rf_model.pkl
- models/label_encoder.pkl

## Step 3: Start the web app:
```bash
python app.py
```
"""

if __name__ == '__main__':
    print(NOTEBOOK_INSTRUCTIONS)
