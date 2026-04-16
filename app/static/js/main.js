// ==================== DOM Elements ====================

const uploadArea = document.getElementById('uploadArea');
const imageInput = document.getElementById('imageInput');
const browseBtn = document.getElementById('browseBtn');
const previewContainer = document.getElementById('previewContainer');
const imagePreview = document.getElementById('imagePreview');
const changeImageBtn = document.getElementById('changeImageBtn');
const predictionForm = document.getElementById('predictionForm');
const submitBtn = document.getElementById('submitBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const resultsSection = document.getElementById('resultsSection');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');

// ==================== Event Listeners ====================

// Browse button click
browseBtn.addEventListener('click', () => {
    imageInput.click();
});

// Image input change
imageInput.addEventListener('change', handleImageSelect);

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        imageInput.files = files;
        handleImageSelect();
    }
});

// Change image button
changeImageBtn.addEventListener('click', () => {
    imageInput.click();
});

// Form submission
predictionForm.addEventListener('submit', handleFormSubmit);

// New analysis button
newAnalysisBtn.addEventListener('click', resetForm);

// ==================== Functions ====================

function handleImageSelect() {
    const file = imageInput.files[0];
    if (!file) return;
    
    // Validate file type
    if (!file.type.startsWith('image/')) {
        showError('Please select a valid image file');
        return;
    }
    
    // Validate file size (16MB)
    const maxSize = 16 * 1024 * 1024;
    if (file.size > maxSize) {
        showError('File size exceeds 16MB limit');
        return;
    }
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        uploadArea.style.display = 'none';
        previewContainer.style.display = 'flex';
    };
    reader.readAsDataURL(file);
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    // Validate image selection
    if (!imageInput.files[0]) {
        showError('Please select an image');
        return;
    }
    
    // Get symptoms
    const symptoms = {};
    document.querySelectorAll('.symptom-checkbox input').forEach(checkbox => {
        symptoms[checkbox.name] = checkbox.checked ? 1 : 0;
    });
    
    // Prepare form data
    const formData = new FormData();
    formData.append('image', imageInput.files[0]);
    formData.append('symptoms', JSON.stringify(symptoms));
    
    // Show loading spinner
    showLoadingSpinner();
    
    try {
        // Send prediction request
        const response = await fetch('/api/predict', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Prediction failed');
        }
        
        const results = await response.json();
        displayResults(results);
        
    } catch (error) {
        hideLoadingSpinner();
        showError('Error: ' + error.message);
    }
}

function displayResults(results) {
    hideLoadingSpinner();
    
    // Display image prediction
    if (results.image_prediction) {
        displayPrediction('image', results.image_prediction);
    }
    
    // Display symptom prediction
    if (results.symptom_prediction) {
        displayPrediction('symptom', results.symptom_prediction);
    } else {
        document.querySelector('[data-type="symptom"]').style.display = 'none';
    }
    
    // Display fused prediction
    if (results.fused_prediction) {
        displayPrediction('fused', results.fused_prediction);
    }
    
    // Display explanation
    if (results.explanation) {
        document.getElementById('explanationBox').textContent = results.explanation;
    }
    
    // Show results section
    resultsSection.style.display = 'block';
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

function displayPrediction(type, prediction) {
    const diseaseLabel = document.getElementById(`${type}DiseaseLabel`);
    const confidenceFill = document.getElementById(`${type}ConfidenceFill`);
    const confidenceText = document.getElementById(`${type}ConfidenceText`);
    const probsList = document.getElementById(`${type}Probs`);
    
    // Update disease label
    diseaseLabel.textContent = prediction.class || 'Unknown';
    
    // Update confidence
    const confidence = (prediction.confidence || 0) * 100;
    confidenceFill.style.width = confidence + '%';
    confidenceText.textContent = confidence.toFixed(1) + '%';
    
    // Update probabilities
    probsList.innerHTML = '';
    const probs = prediction.probabilities || {};
    
    Object.entries(probs)
        .sort((a, b) => b[1] - a[1])
        .forEach(([disease, prob]) => {
            const probItem = document.createElement('div');
            probItem.className = 'prob-item';
            probItem.innerHTML = `
                <span class="prob-name">${disease}</span>
                <span class="prob-value">${(prob * 100).toFixed(1)}%</span>
            `;
            probsList.appendChild(probItem);
        });
}

function resetForm() {
    // Reset form
    predictionForm.reset();
    imageInput.value = '';
    
    // Reset preview
    previewContainer.style.display = 'none';
    uploadArea.style.display = 'block';
    
    // Hide results
    resultsSection.style.display = 'none';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function showLoadingSpinner() {
    predictionForm.style.display = 'none';
    resultsSection.style.display = 'none';
    loadingSpinner.style.display = 'flex';
}

function hideLoadingSpinner() {
    loadingSpinner.style.display = 'none';
    predictionForm.style.display = 'block';
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    const formContainer = document.querySelector('.form-container');
    formContainer.insertBefore(errorDiv, formContainer.firstChild);
    
    // Remove error after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// ==================== Initialization ====================

// Set up symptom checkboxes with data attributes
document.querySelectorAll('.symptom-checkbox input').forEach(checkbox => {
    const card = checkbox.closest('[data-type]');
    if (!card) {
        checkbox.closest('.symptom-checkbox').dataset.symptom = checkbox.name;
    }
});

// Ensure results section has proper data attributes
const resultCards = document.querySelectorAll('.result-card');
resultCards.forEach((card, index) => {
    if (index === 0) card.dataset.type = 'image';
    if (index === 1) card.dataset.type = 'symptom';
    if (index === 2) card.dataset.type = 'fused';
});
