"""
Configuration file for the Ear Disease Classification System
"""

import os

# Application Settings
DEBUG = True
TESTING = False

# Server Settings
HOST = '127.0.0.1'
PORT = 5000
THREADED = True

# File Upload Settings
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# Model Settings
VIT_MODEL_PATH = 'models/vit_ear_model.pth'
RF_MODEL_PATH = 'models/symptom_rf_model.pkl'
LABEL_ENCODER_PATH = 'models/label_encoder.pkl'

# Device Settings (auto-detect GPU)
USE_GPU = True

# Model Weights for Fusion
IMAGE_WEIGHT = 0.8
SYMPTOM_WEIGHT = 0.2

# Disease Classes
DISEASE_CLASSES = [
    'Acute Otitis Media',
    'Cerumen Impaction',
    'Chronic Otitis Media',
    'Myringosclerosis',
    'Normal'
]

# Symptom Features
SYMPTOM_FEATURES = [
    'pain',
    'discharge',
    'hearing_loss',
    'fever',
    'blocked_ear',
    'itching',
    'dizziness',
    'tinnitus',
    'long_duration'
]

# Clinical Notes for Diseases
CLINICAL_NOTES = {
    'Acute Otitis Media': 'This condition requires prompt medical attention. Recommend consultation with an otolaryngologist.',
    'Chronic Otitis Media': 'This is a long-standing condition. Regular monitoring and follow-up care are recommended.',
    'Cerumen Impaction': 'This condition involves earwax buildup. Professional ear cleaning may be beneficial.',
    'Myringosclerosis': 'This condition affects the eardrum. Monitoring of hearing is recommended.',
    'Normal': 'No abnormalities detected. The ear appears healthy.'
}

# Image Processing Settings
IMAGE_SIZE = (224, 224)  # ViT input size
IMAGE_MEAN = [0.485, 0.456, 0.406]  # ImageNet normalization
IMAGE_STD = [0.229, 0.224, 0.225]

# Logging Settings
LOG_LEVEL = 'INFO'
LOG_FILE = 'app.log'

# CORS Settings (if needed)
CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']

# Session Settings
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
SESSION_COOKIE_SECURE = False  # Set to True in production

# Get environment-specific settings
def get_config():
    """Get configuration based on environment"""
    config = {
        'debug': DEBUG,
        'host': HOST,
        'port': PORT,
        'max_content_length': MAX_CONTENT_LENGTH,
        'upload_folder': UPLOAD_FOLDER,
        'vit_model_path': VIT_MODEL_PATH,
        'rf_model_path': RF_MODEL_PATH,
        'use_gpu': USE_GPU,
        'image_weight': IMAGE_WEIGHT,
        'symptom_weight': SYMPTOM_WEIGHT,
        'disease_classes': DISEASE_CLASSES,
        'symptom_features': SYMPTOM_FEATURES,
    }
    return config

if __name__ == '__main__':
    import json
    config = get_config()
    print(json.dumps(config, indent=2))
