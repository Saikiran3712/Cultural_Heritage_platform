// Main JavaScript for Indian Cultural Heritage Platform

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });

    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // Language selector functionality
    const languageSelectors = document.querySelectorAll('select[id="language"]');
    languageSelectors.forEach(selector => {
        selector.addEventListener('change', function() {
            const selectedLang = this.value;
            updateUILanguage(selectedLang);
        });
    });

    // Character counter for text fields
    const textInputs = document.querySelectorAll('input[type="text"], textarea');
    textInputs.forEach(input => {
        if (input.hasAttribute('maxlength')) {
            addCharacterCounter(input);
        }
    });
});

function updateUILanguage(language) {
    // This function would update UI elements based on selected language
    // For now, it's a placeholder for future multilingual support
    console.log('Language changed to:', language);
}

function addCharacterCounter(input) {
    const maxLength = input.getAttribute('maxlength');
    const counter = document.createElement('small');
    counter.className = 'form-text text-muted character-counter';
    counter.textContent = `0/${maxLength} characters`;
    
    input.parentNode.appendChild(counter);
    
    input.addEventListener('input', function() {
        const currentLength = this.value.length;
        counter.textContent = `${currentLength}/${maxLength} characters`;
        
        if (currentLength > maxLength * 0.9) {
            counter.classList.add('text-warning');
        } else {
            counter.classList.remove('text-warning');
        }
    });
}

// API helper functions
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(endpoint, options);
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Show loading spinner
function showLoading(element) {
    const originalText = element.innerHTML;
    element.innerHTML = '<span class="spinner"></span> Loading...';
    element.disabled = true;
    return originalText;
}

function hideLoading(element, originalText) {
    element.innerHTML = originalText;
    element.disabled = false;
}

// Form submission helpers
async function submitForm(formId, endpoint) {
    const form = document.getElementById(formId);
    const formData = new FormData(form);
    const jsonData = {};
    
    for (let [key, value] of formData.entries()) {
        jsonData[key] = value;
    }

    try {
        const response = await apiCall(endpoint, 'POST', jsonData);
        if (response.success) {
            showAlert('Success!', 'Your submission was successful.', 'success');
            form.reset();
        } else {
            showAlert('Error', response.message || 'Something went wrong.', 'error');
        }
    } catch (error) {
        showAlert('Error', 'Failed to submit. Please try again.', 'error');
    }
}

// Alert system
function showAlert(title, message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.innerHTML = `
        <strong>${title}</strong> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertContainer, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}

// File upload helpers
function setupFileUpload(inputId) {
    const input = document.getElementById(inputId);
    if (!input) return;

    input.addEventListener('change', function(e) {
        const files = e.target.files;
        const fileInfo = document.createElement('div');
        fileInfo.className = 'file-info mt-2';
        
        let infoText = '';
        for (let file of files) {
            const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
            infoText += `<small class="text-muted d-block">${file.name} (${sizeMB} MB)</small>`;
        }
        
        fileInfo.innerHTML = infoText;
        
        // Remove existing file info
        const existingInfo = input.parentNode.querySelector('.file-info');
        if (existingInfo) {
            existingInfo.remove();
        }
        
        input.parentNode.appendChild(fileInfo);
    });
}

// Audio recording functionality (placeholder)
function initializeAudioRecording() {
    const recordButtons = document.querySelectorAll('#recordBtn');
    recordButtons.forEach(button => {
        button.addEventListener('click', function() {
            // This would implement actual audio recording functionality
            console.log('Audio recording not yet implemented');
            showAlert('Info', 'Audio recording feature coming soon!', 'info');
        });
    });
}

// Initialize file upload handlers when page loads
document.addEventListener('DOMContentLoaded', function() {
    setupFileUpload('audio');
    setupFileUpload('photo');
    setupFileUpload('photos');
    initializeAudioRecording();
});

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Export functions for use in other scripts
window.CHPlatform = {
    apiCall,
    showLoading,
    hideLoading,
    submitForm,
    showAlert,
    setupFileUpload
};