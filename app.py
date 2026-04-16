import os
import sys
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import torch
import numpy as np
from PIL import Image
import io
import json
from datetime import datetime

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from models.inference import EarDiseaseClassifier

# Initialize Flask app
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'

# Initialize classifier
classifier = None

def init_classifier():
    """Initialize the disease classifier"""
    global classifier
    try:
        classifier = EarDiseaseClassifier(
            vit_model_path='models/vit_ear_model.pth',
            rf_model_path='models/symptom_rf_model.pkl',
            device='cuda' if torch.cuda.is_available() else 'cpu'
        )
        print("Classifier initialized successfully")
    except Exception as e:
        print(f"Warning: Could not load pretrained models. {str(e)}")
        print("The app will work in demo mode.")

@app.before_request
def setup():
    """Initialize classifier on first request"""
    global classifier
    if classifier is None:
        init_classifier()

@app.route('/')
def index():
    """Main page - input form"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for predictions"""
    try:
        # Get image file
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        # Get symptoms
        symptoms_data = request.form.get('symptoms', '{}')
        try:
            symptoms = json.loads(symptoms_data)
        except:
            symptoms = {}
        
        # Process image
        filename = secure_filename(image_file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Create upload folder if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        image_file.save(filepath)
        
        # Get predictions
        if classifier is not None:
            results = classifier.predict(
                image_path=filepath,
                symptoms=symptoms
            )
        else:
            # Demo mode - return mock results
            results = {
                'image_prediction': {
                    'class': 'Normal',
                    'confidence': 0.85,
                    'probabilities': {
                        'Normal': 0.85,
                        'Chronic Otitis Media': 0.10,
                        'Cerumen Impaction': 0.03,
                        'Acute Otitis Media': 0.01,
                        'Myringosclerosis': 0.01
                    }
                },
                'symptom_prediction': {
                    'class': 'Normal',
                    'confidence': 0.92,
                    'probabilities': {
                        'Normal': 0.92,
                        'Chronic Otitis Media': 0.05,
                        'Cerumen Impaction': 0.03
                    }
                },
                'fused_prediction': {
                    'class': 'Normal',
                    'confidence': 0.87,
                    'probabilities': {
                        'Normal': 0.87,
                        'Chronic Otitis Media': 0.08,
                        'Cerumen Impaction': 0.03,
                        'Acute Otitis Media': 0.01,
                        'Myringosclerosis': 0.01
                    }
                },
                'explanation': 'Based on image analysis and symptom evaluation, the patient appears to have normal ear condition. No abnormalities detected.',
                'image_path': filename,
                'timestamp': datetime.now().isoformat()
            }
        
        return jsonify(results)
    
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/results')
def results():
    """Results page"""
    return render_template('results.html')

@app.route('/help')
def help():
    """Help/About page"""
    return render_template('help.html')

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server error"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Run the app
    print("Starting Ear Disease Classification App...")
    print(f"Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    app.run(debug=True, host='127.0.0.1', port=5000)
