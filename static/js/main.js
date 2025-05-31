document.addEventListener('DOMContentLoaded', function() {
    // Form validation for marks input
    const marksInputs = document.querySelectorAll('.marks-input');
    marksInputs.forEach(input => {
        input.addEventListener('input', function() {
            let value = this.value;
            // Remove non-numeric characters
            value = value.replace(/[^0-9]/g, '');
            // Limit to 3 digits (0-100)
            if (value.length > 3) {
                value = value.slice(0, 3);
            }
            // Ensure value is within 0-100 range
            if (value && parseInt(value) > 100) {
                value = '100';
            }
            this.value = value;
        });
    });

    // Add loading spinner
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const spinner = document.createElement('div');
        spinner.className = 'spinner-border text-primary';
        spinner.style.display = 'none';
        spinner.style.margin = '20px auto';
        spinner.style.width = '3rem';
        spinner.style.height = '3rem';
        
        form.appendChild(spinner);
        
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            spinner.style.display = 'block';
            
            // Submit form after showing spinner
            setTimeout(() => {
                this.submit();
            }, 500);
        });
    });

    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add hover effects to cards
    const cards = document.querySelectorAll('.subject-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
            card.style.boxShadow = '0 8px 12px rgba(0,0,0,0.1)';
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
            card.style.boxShadow = '0 4px 6px rgba(0,0,0,0.05)';
        });
    });

    // Add print functionality
    const printBtn = document.querySelector('.print-btn');
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            window.print();
        });
    }
});
