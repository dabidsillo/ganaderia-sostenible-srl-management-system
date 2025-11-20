// Verificar si ya se aceptaron las políticas de privacidad
document.addEventListener('DOMContentLoaded', function () {
    if (!localStorage.getItem('privacyAccepted')) {
        const privacyBanner = document.getElementById('privacy-banner');
        privacyBanner.classList.remove('hidden');
    }
});

// Guardar la aceptación en el localStorage
function acceptPrivacyPolicy() {
    localStorage.setItem('privacyAccepted', true);
    document.getElementById('privacy-banner').classList.add('hidden');
}
