import torch
import torch.nn.functional as F
import numpy as np
import pandas as pd
import pickle
from PIL import Image
from torchvision import transforms
import timm
from pathlib import Path

class EarDiseaseClassifier:
    """Main classifier combining ViT and Random Forest models"""
    
    def __init__(self, vit_model_path=None, rf_model_path=None, device='cpu'):
        """
        Initialize the classifier
        
        Args:
            vit_model_path: Path to saved ViT model
            rf_model_path: Path to saved Random Forest model
            device: torch device ('cpu' or 'cuda')
        """
        self.device = torch.device(device)
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        # Disease classes
        self.disease_classes = [
            'Acute Otitis Media',
            'Cerumen Impaction',
            'Chronic Otitis Media',
            'Myringosclerosis',
            'Normal'
        ]
        
        # Symptom features
        self.symptom_features = [
            'pain', 'discharge', 'hearing_loss', 'fever', 
            'blocked_ear', 'itching', 'dizziness', 'tinnitus', 
            'long_duration'
        ]
        
        # Load models if paths provided
        self.vit_model = self._load_vit_model(vit_model_path) if vit_model_path else None
        self.rf_model = self._load_rf_model(rf_model_path) if rf_model_path else None
    
    def _load_vit_model(self, path):
        """Load Vision Transformer model"""
        try:
            import torch.nn as nn
            model = timm.create_model('vit_base_patch16_224', pretrained=True)
            model.head = nn.Linear(model.head.in_features, len(self.disease_classes))
            
            if Path(path).exists():
                checkpoint = torch.load(path, map_location=self.device)
                if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
                    model.load_state_dict(checkpoint['model_state_dict'])
                else:
                    model.load_state_dict(checkpoint)
            
            model.to(self.device)
            model.eval()
            return model
        except Exception as e:
            print(f"Could not load ViT model: {e}")
            return None
    
    def _load_rf_model(self, path):
        """Load Random Forest model"""
        try:
            if Path(path).exists():
                with open(path, 'rb') as f:
                    return pickle.load(f)
            return None
        except Exception as e:
            print(f"Could not load RF model: {e}")
            return None
    
    def predict_image(self, image_path):
        """Predict from image using ViT"""
        if self.vit_model is None:
            return None
        
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            image_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Get prediction
            with torch.no_grad():
                outputs = self.vit_model(image_tensor)
                probabilities = F.softmax(outputs, dim=1).cpu().numpy()[0]
            
            predicted_idx = np.argmax(probabilities)
            predicted_class = self.disease_classes[predicted_idx]
            confidence = float(probabilities[predicted_idx])
            
            return {
                'class': predicted_class,
                'confidence': confidence,
                'probabilities': {
                    cls: float(prob) 
                    for cls, prob in zip(self.disease_classes, probabilities)
                }
            }
        except Exception as e:
            print(f"Error in image prediction: {e}")
            return None
    
    def predict_symptoms(self, symptoms):
        """Predict from symptoms using Random Forest"""
        if self.rf_model is None or not hasattr(self.rf_model, 'predict_proba'):
            return None
        
        try:
            # Create feature vector
            feature_vector = []
            for feature in self.symptom_features:
                feature_vector.append(symptoms.get(feature, 0))
            
            feature_vector = np.array(feature_vector).reshape(1, -1)
            
            # Get prediction
            probabilities = self.rf_model.predict_proba(feature_vector)[0]
            
            # Map to disease classes (adjust mapping as needed)
            symptom_classes = {
                0: 'Chronic Otitis Media',
                1: 'Cerumen Impaction',
                2: 'Myringosclerosis',
                3: 'Normal'
            }
            
            pred_idx = np.argmax(probabilities)
            predicted_class = symptom_classes.get(pred_idx, 'Normal')
            confidence = float(probabilities[pred_idx])
            
            return {
                'class': predicted_class,
                'confidence': confidence,
                'probabilities': {
                    'Normal': float(probabilities[3]) if len(probabilities) > 3 else 0,
                    'Chronic Otitis Media': float(probabilities[0]),
                    'Cerumen Impaction': float(probabilities[1]) if len(probabilities) > 1 else 0,
                    'Myringosclerosis': float(probabilities[2]) if len(probabilities) > 2 else 0,
                    'Acute Otitis Media': 0.0
                }
            }
        except Exception as e:
            print(f"Error in symptom prediction: {e}")
            return None
    
    def fuse_predictions(self, image_pred, symptom_pred, image_weight=0.8):
        """Fuse predictions using weighted averaging"""
        if image_pred is None or symptom_pred is None:
            # Return single prediction if one model is unavailable
            return image_pred or symptom_pred
        
        symptom_weight = 1.0 - image_weight
        
        # Get probabilities
        image_probs = image_pred.get('probabilities', {})
        symptom_probs = symptom_pred.get('probabilities', {})
        
        # Fuse probabilities for common classes
        fused_probs = {}
        for disease_class in self.disease_classes:
            image_p = image_probs.get(disease_class, 0.0)
            symptom_p = symptom_probs.get(disease_class, 0.0)
            fused_probs[disease_class] = (
                image_weight * image_p + 
                symptom_weight * symptom_p
            )
        
        # Normalize
        total = sum(fused_probs.values())
        if total > 0:
            fused_probs = {k: v/total for k, v in fused_probs.items()}
        
        # Get final prediction
        max_prob = max(fused_probs.values()) if fused_probs else 0
        predicted_class = max(fused_probs, key=fused_probs.get) if fused_probs else 'Normal'
        
        return {
            'class': predicted_class,
            'confidence': float(max_prob),
            'probabilities': fused_probs,
            'image_contribution': image_weight,
            'symptom_contribution': symptom_weight
        }
    
    def predict(self, image_path, symptoms=None):
        """Full prediction pipeline"""
        symptoms = symptoms or {}
        
        # Get individual predictions
        image_pred = self.predict_image(image_path)
        symptom_pred = self.predict_symptoms(symptoms) if symptoms else None
        
        # Fuse predictions
        if image_pred and symptom_pred:
            fused_pred = self.fuse_predictions(image_pred, symptom_pred)
        elif image_pred:
            fused_pred = image_pred
        else:
            fused_pred = {'class': 'Normal', 'confidence': 0.5, 'probabilities': {}}
        
        # Generate clinical explanation
        explanation = self._generate_explanation(
            image_pred, symptom_pred, fused_pred, symptoms
        )
        
        return {
            'image_prediction': image_pred,
            'symptom_prediction': symptom_pred,
            'fused_prediction': fused_pred,
            'explanation': explanation,
            'timestamp': None
        }
    
    def _generate_explanation(self, image_pred, symptom_pred, fused_pred, symptoms):
        """Generate clinical explanation"""
        if fused_pred is None:
            return "Unable to generate explanation."
        
        disease = fused_pred.get('class', 'Unknown')
        confidence = fused_pred.get('confidence', 0) * 100
        
        explanation = f"Based on the analysis, the predicted diagnosis is {disease} with {confidence:.1f}% confidence. "
        
        # Add symptom analysis
        if symptoms:
            active_symptoms = [k for k, v in symptoms.items() if v == 1]
            if active_symptoms:
                explanation += f"Reported symptoms include: {', '.join(active_symptoms)}. "
        
        # Add clinical notes based on disease
        clinical_notes = {
            'Acute Otitis Media': 'This condition requires prompt medical attention. Recommend consultation with an otolaryngologist.',
            'Chronic Otitis Media': 'This is a long-standing condition. Regular monitoring and follow-up care are recommended.',
            'Cerumen Impaction': 'This condition involves earwax buildup. Professional ear cleaning may be beneficial.',
            'Myringosclerosis': 'This condition affects the eardrum. Monitoring of hearing is recommended.',
            'Normal': 'No abnormalities detected. The ear appears healthy.'
        }
        
        explanation += clinical_notes.get(disease, 'Please consult a healthcare provider for guidance.')
        
        return explanation
