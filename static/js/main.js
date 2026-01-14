// ===================================
// BIBLIOTECA DJANGO - JAVASCRIPT PERSONALIZADO
// ===================================

// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializar popovers de Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Añadir animación de fade-in a las tarjetas
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animation = `fadeIn 0.5s ease ${index * 0.1}s both`;
    });

    // Confirmación antes de eliminar (si se implementa)
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que deseas eliminar este elemento?')) {
                e.preventDefault();
            }
        });
    });

    // Búsqueda en tiempo real (opcional)
    const searchInput = document.querySelector('#search');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Aquí se podría implementar búsqueda AJAX
                console.log('Buscando:', this.value);
            }, 500);
        });
    }

    // Validación de formularios
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // Scroll suave para enlaces internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Botón de volver arriba
    const backToTopButton = createBackToTopButton();
    document.body.appendChild(backToTopButton);
    
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });

    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Contador animado para estadísticas
    animateCounters();

    // Lazy loading para imágenes
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img.lazy').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Highlight active nav link
    highlightActiveNavLink();
});

// Función para crear botón de volver arriba
function createBackToTopButton() {
    const button = document.createElement('button');
    button.innerHTML = '<i class="fas fa-arrow-up"></i>';
    button.className = 'btn btn-primary';
    button.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        display: none;
        z-index: 1000;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    `;
    button.setAttribute('title', 'Volver arriba');
    return button;
}

// Función para animar contadores
function animateCounters() {
    const counters = document.querySelectorAll('.card-body h2');
    const speed = 200;

    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.innerText;
            const count = +counter.getAttribute('data-count') || 0;
            const increment = target / speed;

            if (count < target) {
                counter.setAttribute('data-count', Math.ceil(count + increment));
                counter.innerText = Math.ceil(count + increment);
                setTimeout(updateCount, 1);
            } else {
                counter.innerText = target;
            }
        };

        // Solo animar si es un número
        if (!isNaN(counter.innerText)) {
            const originalValue = counter.innerText;
            counter.innerText = '0';
            counter.setAttribute('data-count', '0');
            
            // Usar Intersection Observer para animar cuando sea visible
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        counter.innerText = originalValue;
                        observer.unobserve(counter);
                    }
                });
            });
            
            observer.observe(counter);
        }
    });
}

// Función para resaltar el enlace activo en la navegación
function highlightActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// Función de utilidad para mostrar mensajes toast
function showToast(message, type = 'info') {
    const toastHTML = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    // Crear contenedor de toasts si no existe
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastElement = toastContainer.lastElementChild;
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Eliminar el toast después de que se oculte
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

// Función para formatear números con separadores de miles
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Exportar funciones para uso global
window.bibliotecaApp = {
    showToast,
    formatNumber
};

console.log('Biblioteca Django - Sistema cargado correctamente ✓');
