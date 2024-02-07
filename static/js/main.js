let button = document.querySelector('[data-mobile-menu]');
let mobileMenu = document.getElementById('mobile-menu');

button.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden')
});


//Alert
let alertButton = document.querySelector('[close]');
let alerta = document.getElementById('alerta');

if (alertButton) {
alertButton.addEventListener('click', () => {
    alerta.classList.toggle('hidden')
    setTimeout(() => {
alerta.classList.add('hidden');
    }, 50000)
});
}