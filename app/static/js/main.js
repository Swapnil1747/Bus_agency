// Form validation
document.addEventListener('DOMContentLoaded', function() {
    // Password validation
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    
    if (passwordInput && confirmPasswordInput) {
        function validatePassword() {
            if (passwordInput.value !== confirmPasswordInput.value) {
                confirmPasswordInput.setCustomValidity('Passwords do not match');
            } else {
                confirmPasswordInput.setCustomValidity('');
            }
        }
        
        passwordInput.addEventListener('change', validatePassword);
        confirmPasswordInput.addEventListener('keyup', validatePassword);
    }
    
    // Date validation for search
    const dateInput = document.getElementById('date');
    if (dateInput) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
    }
    
    // Auto-dismiss alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });
});

// Seat selection
function updateSeatSelection(seatNumber) {
    const selectedSeatSpan = document.getElementById('selected-seat');
    if (selectedSeatSpan) {
        selectedSeatSpan.textContent = seatNumber;
    }
}

// Booking confirmation
function confirmBooking() {
    return confirm('Are you sure you want to proceed with this booking?');
}

// Cancel booking confirmation
function confirmCancellation() {
    return confirm('Are you sure you want to cancel this booking? This action cannot be undone.');
}

// Add smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
}); 