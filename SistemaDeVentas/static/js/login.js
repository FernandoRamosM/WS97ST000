// Funcionalidad del modal recuperar contraseña
const recoverModal = document.getElementById('recover-modal');
const openRecoverModal = document.getElementById('recover-link');
const closeRecoverModal = document.getElementById('close-modal');

openRecoverModal.addEventListener('click', () => {
    recoverModal.style.display = 'flex';
}); // Abre modal de recuperación

closeRecoverModal.addEventListener('click', () => {
    recoverModal.style.display = 'none';
}); // Cierra modal de recuperación

window.addEventListener('click', (e) => {
    if (e.target === recoverModal) {
        recoverModal.style.display = 'none';
    }
}); // Cierra modal de recuperación al hacer clic fuera

// -------------------------------------------
// Funcionalidad del modal de nueva contraseña
// -------------------------------------------
const newPasswordModal      = document.querySelector('#new-password-modal');
const closeNewPasswordModal = document.querySelector('#close-modal-np');

closeNewPasswordModal.addEventListener("click",()=>{
    newPasswordModal.close();
})
