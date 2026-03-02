// Leemos la sesión del localStorage
const user = JSON.parse(localStorage.getItem('currentUser'));

// Si no hay sesión, redirigimos al login
if (!user) {
  window.location.href = 'login.html';
}

const container = document.getElementById('profile-container');
const logoutBtn = document.getElementById('logout-btn');

// Construimos las cards con los datos del usuario
container.innerHTML = `
  <div>
    <h2>Información del usuario</h2>
    <p><strong>ID:</strong> ${user.id}</p>
    <p><strong>Nombre:</strong> ${user.name}</p>
    <p><strong>Email:</strong> ${user.data.email}</p>
    <p><strong>Dirección:</strong> ${user.data.address}</p>
    
  </div>
`;

// Botón de cerrar sesión
logoutBtn.addEventListener('click', function() {
  localStorage.removeItem('currentUser');
  window.location.href = 'login.html';
});