const form = document.getElementById('change-password-form');
const errorMessage = document.getElementById('error-message');
const successMessage = document.getElementById('success-message');

form.addEventListener('submit', async function(event) {
  event.preventDefault();

  const userId = document.getElementById('userId').value;
  const oldPassword = document.getElementById('oldPassword').value;
  const newPassword = document.getElementById('newPassword').value;
  const confirmPassword = document.getElementById('confirmPassword').value;

  // Función helper para mostrar errores
  function showError(message) {
    errorMessage.style.display = 'block';
    errorMessage.textContent = message;
    successMessage.style.display = 'none';
  }

  try {
    // Validación 1: Que el usuario exista
    const URL = `https://corsproxy.io/?https://api.restful-api.dev/objects/${userId}`;
    const response = await axios.get(URL);
    const user = response.data;

    // Validación 2: Que la contraseña anterior sea correcta
    if (user.data.password !== oldPassword) {
      showError('La contraseña anterior es incorrecta.');
      return;
    }

    // Validación 3: Que nueva contraseña y confirmación coincidan
    if (newPassword !== confirmPassword) {
      showError('La nueva contraseña y la confirmación no coinciden.');
      return;
    }

    // Si todo pasó, hacemos el PUT con la nueva contraseña
    const updatedUser = {
      name: user.name,
      data: {
        email: user.data.email,
        password: newPassword,
        address: user.data.address
      }
    };

    await axios.put(URL, updatedUser);

    // Mostramos mensaje de éxito
    errorMessage.style.display = 'none';
    successMessage.style.display = 'block';
    successMessage.textContent = 'Contraseña cambiada correctamente.';
    form.reset();

  } catch (error) {
    showError('El usuario no existe. Verifica tu ID.');
  }
});