// Contact form handling
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contact-form');
    const formMessage = document.getElementById('form-message');

    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const formData = new FormData(contactForm);
            const data = {
                name: formData.get('name'),
                email: formData.get('email'),
                subject: formData.get('subject'),
                message: formData.get('message')
            };

            try {
                const response = await fetch('/api/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (result.success) {
                    formMessage.innerHTML = `
                        <div class="success-message">
                            <i class="fas fa-check-circle"></i>
                            ${result.message}
                        </div>
                    `;
                    contactForm.reset();
                } else {
                    formMessage.innerHTML = `
                        <div class="error-message">
                            <i class="fas fa-exclamation-circle"></i>
                            ${result.error}
                        </div>
                    `;
                }
            } catch (error) {
                formMessage.innerHTML = `
                    <div class="error-message">
                        <i class="fas fa-exclamation-circle"></i>
                        Something went wrong. Please try again.
                    </div>
                `;
            }
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

// API functions for potential use
async function getPortfolioData() {
    try {
        const response = await fetch('/api/portfolio');
        return await response.json();
    } catch (error) {
        console.error('Error fetching portfolio data:', error);
        return null;
    }
}

async function getSkills() {
    try {
        const response = await fetch('/api/skills');
        return await response.json();
    } catch (error) {
        console.error('Error fetching skills:', error);
        return null;
    }
}
// Mobile Menu Toggle Functions
function toggleMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    
    hamburger.classList.toggle('active');
    mobileMenu.classList.toggle('active');
}

function closeMobileMenu() {
    const hamburger = document.querySelector('.hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    
    hamburger.classList.remove('active');
    mobileMenu.classList.remove('active');
}

// Close menu when clicking outside
document.addEventListener('click', function(event) {
    const mobileNav = document.querySelector('.mobile-nav');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (!mobileNav.contains(event.target) && mobileMenu.classList.contains('active')) {
        closeMobileMenu();
    }
});