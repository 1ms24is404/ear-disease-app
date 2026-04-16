# 🏥 Ear Disease Classification System - Frontend

A comprehensive web application for AI-powered ear disease diagnosis using otoscopic images and symptom analysis.

## 🎯 Overview

This frontend application provides an intuitive interface for the multimodal ear disease classification system that combines:

- **Vision Transformer (ViT)**: Deep learning model trained on otoscopic images
- **Random Forest**: Machine learning classifier for symptom-based diagnosis
- **Decision-Level Late Fusion**: Combines predictions from both models (80% image + 20% symptoms)

## 🌟 Features

### User Interface
- 📷 **Image Upload**: Drag-and-drop or browse file selection for otoscopic images
- 🩺 **Symptom Selection**: Easy-to-use checkboxes for symptom input (9 symptoms)
- 📊 **Real-time Results**: Instant analysis and diagnosis display
- 📈 **Confidence Metrics**: Probability distributions for all disease categories
- 📋 **Clinical Summaries**: AI-generated explanations and recommendations

### Technical Features
- Responsive design for desktop and mobile devices
- Real-time form validation
- Asynchronous prediction processing
- Error handling and user feedback
- Loading indicators and progress tracking

## 📋 Project Structure

```
ear-disease-app/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── app/
│   ├── templates/              # HTML templates
│   │   ├── index.html          # Main prediction interface
│   │   ├── results.html        # Results display page
│   │   └── help.html           # Help and documentation
│   │
│   └── static/                 # Static assets
│       ├── css/
│       │   └── style.css       # Styling (gradient theme, responsive)
│       ├── js/
│       │   └── main.js         # Client-side logic
│       └── uploads/            # Temporary image storage
│
├── models/                     # ML model integration
│   ├── inference.py            # Main classifier class
│   ├── vit_ear_model.pth       # ViT model weights (download from notebook)
│   └── symptom_rf_model.pkl    # Random Forest model (export from notebook)
```

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.8+
- CUDA (optional, for GPU acceleration)

### 2. Clone and Navigate
```bash
cd c:\Users\sheru\ear-disease-app
```

### 3. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Prepare Models

The application requires two trained models:

**From your Jupyter Notebook:**
1. Save the ViT model after training:
   ```python
   torch.save({'model_state_dict': vit_model.state_dict()}, 'vit_ear_model.pth')
   ```

2. Save the Random Forest model:
   ```python
   import pickle
   with open('symptom_rf_model.pkl', 'wb') as f:
       pickle.dump(rf_model, f)
   ```

3. Move both files to the `models/` directory

**Note:** If models are not available, the app runs in **demo mode** with mock predictions.

### 6. Run the Application
```bash
python app.py
```

The application will start at `http://127.0.0.1:5000`

## 💻 Usage

### Step 1: Upload Image
- Click the upload area or drag-drop an otoscopic image
- Supported formats: JPG, PNG, GIF
- Maximum size: 16MB

### Step 2: Select Symptoms
Choose all applicable symptoms:
- Pain
- Discharge
- Hearing Loss
- Fever
- Blocked Ear
- Itching
- Dizziness
- Tinnitus
- Long Duration

### Step 3: Get Diagnosis
Click "Get Diagnosis" button to:
- Analyze the uploaded image using Vision Transformer
- Evaluate selected symptoms using Random Forest
- Combine predictions using decision-level fusion
- Generate clinical summary

### Step 4: Review Results
The results display includes:
- **Image Analysis**: ViT-based diagnosis
- **Symptom Analysis**: Random Forest-based diagnosis
- **Final Diagnosis**: Fused prediction
- **Probabilities**: Confidence scores for all diseases
- **Clinical Summary**: AI-generated explanation

## 🏥 Supported Diseases

1. **Acute Otitis Media** - Sudden middle ear infection
2. **Chronic Otitis Media** - Long-term ear inflammation
3. **Cerumen Impaction** - Earwax buildup
4. **Myringosclerosis** - Eardrum hardening/scarring
5. **Normal** - Healthy ear condition

## 🎨 User Interface Design

### Color Scheme
- **Primary**: #667eea (Purple-Blue)
- **Secondary**: #764ba2 (Deep Purple)
- **Background**: Gradient (135deg from #667eea to #764ba2)
- **Accent**: White backgrounds with gradient overlays

### Responsive Breakpoints
- Desktop: Full layout with 3-column grid
- Tablet: 2-column layout
- Mobile: 1-column stacked layout

## 🔧 Customization

### Modify Disease Classes
Edit `models/inference.py`:
```python
self.disease_classes = [
    'Your Disease 1',
    'Your Disease 2',
    # ... add more
]
```

### Adjust Fusion Weights
Edit `models/inference.py` in `fuse_predictions()`:
```python
image_weight = 0.8  # Change as needed
symptom_weight = 0.2
```

### Change Styling
Edit `app/static/css/style.css` to customize colors, fonts, and layout.

## ⚠️ Important Disclaimers

- **Educational Purpose Only**: This system is NOT a medical device
- **Not a Replacement**: Always consult qualified healthcare providers
- **Accuracy Limitations**: AI models can make mistakes
- **Privacy**: Images uploaded locally; consult your privacy policy

## 🐛 Troubleshooting

### Issue: "Model not found" warnings
**Solution**: Models are optional. App runs in demo mode. Place trained models in `models/` directory.

### Issue: Port 5000 already in use
**Solution**: Change port in `app.py`:
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

### Issue: Slow predictions
**Solution**: 
- Install CUDA/cuDNN for GPU acceleration
- Reduce image resolution
- Use GPU device in `models/inference.py`

### Issue: Image upload fails
**Solution**: 
- Check file format (JPG, PNG, GIF)
- Verify file size < 16MB
- Ensure `app/static/uploads/` directory has write permissions

## 📚 API Endpoints

### POST `/api/predict`
Performs prediction on provided image and symptoms.

**Request:**
```
FormData:
- image: File (required)
- symptoms: JSON string of symptom flags
```

**Response:**
```json
{
  "image_prediction": {
    "class": "Disease Name",
    "confidence": 0.95,
    "probabilities": {...}
  },
  "symptom_prediction": {...},
  "fused_prediction": {...},
  "explanation": "Clinical summary",
  "timestamp": "ISO timestamp"
}
```

## 📈 Performance Metrics

Expected performance on typical hardware:
- Image preprocessing: ~50ms
- ViT inference: ~200-500ms (CPU), ~50-100ms (GPU)
- RF inference: ~10ms
- Total response time: ~300-700ms (CPU), ~150-200ms (GPU)

## 🔐 Security Considerations

- File size limit: 16MB
- Allowed formats: JPG, PNG, GIF (MIME type validation)
- Temporary file cleanup recommended
- CSRF protection available (add if needed)

## 🤝 Contributing

To extend the system:
1. Modify `models/inference.py` for new models
2. Update HTML templates for new UI elements
3. Extend CSS for new styling
4. Add API endpoints in `app.py`

## 📞 Support

For issues or questions:
1. Check the Help page in the application
2. Review documentation in `README.md`
3. Check console for error messages
4. Consult the Jupyter Notebook for model details

## 📄 License

This project is for educational purposes. Use at your own risk.

## 🎓 References

- Vision Transformer: https://arxiv.org/abs/2010.11929
- Flask Documentation: https://flask.palletsprojects.com/
- PyTorch: https://pytorch.org/
- scikit-learn: https://scikit-learn.org/

---

**Version**: 1.0.0  
**Last Updated**: April 2024  
**Status**: Ready for Educational Use
