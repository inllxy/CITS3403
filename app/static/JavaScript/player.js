// Preview uploaded player photo
function previewImage(event) {
    const preview = document.getElementById('previewImage');
    const file = event.target.files[0];
    if (file) {
      preview.src = URL.createObjectURL(file);
      preview.style.display = 'block';
    } else {
      preview.src = '';
      preview.style.display = 'none';
    }
  }
  
  // Attach handler once DOM is ready
  document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.querySelector('#addPlayerModal input[type="file"]');
    if (fileInput) fileInput.addEventListener('change', previewImage);
  });
  