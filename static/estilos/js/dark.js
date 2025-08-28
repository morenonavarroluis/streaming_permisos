// Espera a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', () => {

    // Selecciona el botón y el ícono
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const htmlElement = document.documentElement;

    // Función para cambiar el tema
    function toggleTheme() {
        if (htmlElement.getAttribute('data-bs-theme') === 'dark') {
            // Si el tema actual es oscuro, lo cambia a claro
            htmlElement.setAttribute('data-bs-theme', 'light');
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
            themeIcon.style.color = 'yellow'; // Cambia el color del ícono para el tema claro
        } else {
            // Si el tema actual es claro, lo cambia a oscuro
            htmlElement.setAttribute('data-bs-theme', 'dark');
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
            themeIcon.style.color = 'black'; // Cambia el color del ícono para el tema oscuro
        }
    }

    // Agrega un "event listener" al botón
    themeToggle.addEventListener('click', toggleTheme);
});