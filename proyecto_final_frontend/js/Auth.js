// auth.js
// Maneja login, register, logout y el "guard" de rutas protegidas.
// Analogía Flask: combina tu blueprint de auth + el decorador @login_required.

/**
 * Protege páginas que requieren sesión activa.
 * Si no hay sesión, redirige al login.
 * 
 *  * 
 * Uso: llamar requireAuth() al inicio del script de cada página protegida.
 */
function requireAuth() {
  const user = getSession();
  if (!user) {
    window.location.href = 'index.html';
  }
  return user;
}

/**
 * Redirige al app si ya hay sesión activa (evita ver el login estando logueado).
 * Uso: llamar redirectIfLoggedIn() en index.html
 */
function redirectIfLoggedIn() {
  const user = getSession();
  if (user) {
    window.location.href = 'app.html';
  }
}

// ─── HANDLERS DE FORMULARIOS ──────────────────────────────────────────────────

/**
 * Maneja el submit del form de login.
 
 */
function handleLogin(email, password) {
  if (!email || !password) {
    return { success: false, message: 'Por favor completa todos los campos.' };
  }

  const user = loginUser(email, password);
  if (!user) {
    return { success: false, message: 'Correo o contraseña incorrectos.' };
  }

  setSession(user);
  return { success: true, message: 'Bienvenido!' };
}

/**
 * Maneja el submit del form de registro.
 * 
 */
function handleRegister(name, email, password, confirmPassword) {
  if (!name || !email || !password || !confirmPassword) {
    return { success: false, message: 'Por favor completa todos los campos.' };
  }

  if (password !== confirmPassword) {
    return { success: false, message: 'Las contraseñas no coinciden.' };
  }

  if (password.length < 6) {
    return { success: false, message: 'La contraseña debe tener al menos 6 caracteres.' };
  }

  const success = registerUser(name, email, password);
  if (!success) {
    return { success: false, message: 'Este correo ya está registrado.' };
  }

  // Auto-login después del registro
  const user = loginUser(email, password);
  setSession(user);
  return { success: true, message: 'Cuenta creada exitosamente.' };
}

/**
 * Cierra la sesión del usuario y redirige al login.
 */
function handleLogout() {
  clearSession();
  window.location.href = 'index.html';
}