// Agarramos el formulario y el párrafo de error del DOM
const form = document.getElementById('register-form');
const errorMessage = document.getElementById('error-message');
const BASE_URL = 'https://corsproxy.io/?https://api.restful-api.dev/objects';

// Escuchamos el evento submit del formulario
form.addEventListener('submit', async function(event) {
  // Prevenimos que la página se recargue
  event.preventDefault();

  // Leemos los valores de cada campo
  const name = document.getElementById('name').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const address = document.getElementById('address').value;

  // Armamos el objeto que espera la API
  const newUser = {
    name: name,
    data: {
      email: email,
      password: password,
      address: address
    }
  };

  try {
    // Hacemos el POST a la API
    const response = await axios.post(BASE_URL, newUser);
    const user = response.data;

    // Guardamos el usuario completo en localStorage para mantener la sesión
    localStorage.setItem('currentUser', JSON.stringify(user));

    // Mostramos el alert con el ID generado
    alert(`Usuario creado correctamente! Tu id es ${user.id}`);

    // Redirigimos a Mi Perfil
    window.location.href = 'profile.html';

  } catch (error) {
    errorMessage.style.display = 'block';
    errorMessage.textContent = 'Hubo un error al crear el usuario. Intenta de nuevo.';
  }
});