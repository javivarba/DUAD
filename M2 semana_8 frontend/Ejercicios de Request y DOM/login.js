const form = document.getElementById('login-form');
const errorMessage = document.getElementById('error-message');

form.addEventListener('submit', async function(event) {
  event.preventDefault();

  const userId = document.getElementById('userId').value;
  const password = document.getElementById('password').value;

  try {
    // Hacemos GET con el ID ingresado por el usuario
    const URL = `https://corsproxy.io/?https://api.restful-api.dev/objects/${userId}`;
    const response = await axios.get(URL);
    const user = response.data;

    // Comparamos la contraseña localmente
    if (user.data.password !== password) {
      errorMessage.style.display = 'block';
      errorMessage.textContent = 'Contraseña incorrecta.';
      return;
    }

    // Si la contraseña es correcta, guardamos la sesión
    localStorage.setItem('currentUser', JSON.stringify(user));

    // Redirigimos a Mi Perfil
    window.location.href = 'profile.html';

  } catch (error) {
    errorMessage.style.display = 'block';
    errorMessage.textContent = 'El usuario no existe. Verifica tu ID.';
  }
});