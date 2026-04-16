// storage.js
// Analogía Flask: Este archivo es como tu "models.py" pero para el browser.
// En lugar de PostgreSQL, usamos localStorage del navegador.
// localStorage = diccionario persistente que sobrevive recargas de página.

const KEYS = {
  USERS: 'duad_users',
  SESSION: 'duad_session',
  TODO_IDS_PREFIX: 'duad_todos_', // + email del usuario = clave única por usuario
};

// ─── USUARIOS ────────────────────────────────────────────────────────────────

/**
 * Retorna el arreglo completo de usuarios registrados.
 * Si no existe aún, retorna arreglo vacío.
 */
function getUsers() {
  const raw = localStorage.getItem(KEYS.USERS);
  return raw ? JSON.parse(raw) : [];
}

/**
 * Guarda el arreglo completo de usuarios.
 * JSON.stringify convierte objeto JS → string (localStorage solo guarda strings).
 */
function saveUsers(users) {
  localStorage.setItem(KEYS.USERS, JSON.stringify(users));
}

/**
 * Agrega un nuevo usuario al arreglo.
 * Retorna false si el email ya existe (validación de unicidad).
 */
function registerUser(name, email, password) {
  const users = getUsers();
  const exists = users.find(u => u.email === email);
  if (exists) return false;

  users.push({ name, email, password });
  saveUsers(users);
  return true;
}

/**
 * Valida credenciales. Retorna el objeto usuario si son correctas, null si no.
 *
 */
function loginUser(email, password) {
  const users = getUsers();
  const user = users.find(u => u.email === email && u.password === password);
  return user || null;
}

// ─── SESIÓN ───────────────────────────────────────────────────────────────────

/**
 * Guarda la sesión activa del usuario.
 
 * Esto es lo que permite que el login persista entre recargas.
 */
function setSession(user) {
  localStorage.setItem(KEYS.SESSION, JSON.stringify(user));
}

/**
 * Retorna el usuario actualmente logueado, o null si no hay sesión.
 */
function getSession() {
  const raw = localStorage.getItem(KEYS.SESSION);
  return raw ? JSON.parse(raw) : null;
}

/**
 * Elimina la sesión (logout).
 * Analogía Flask: equivalente a session.clear()
 */
function clearSession() {
  localStorage.removeItem(KEYS.SESSION);
}

// ─── IDs DE TAREAS POR USUARIO ────────────────────────────────────────────────
// Por qué guardamos IDs: la API pública devuelve miles de objetos de todos los
// usuarios del mundo. En lugar de filtrar esa lista enorme, guardamos solo los
// IDs de las tareas de cada usuario aquí en localStorage.


/**
 * Retorna el arreglo de IDs de tareas de un usuario.
 * La clave en localStorage es única por usuario: "duad_todos_email@ejemplo.com"
 */
function getTodoIds(userId) {
  const key = KEYS.TODO_IDS_PREFIX + userId;
  const raw = localStorage.getItem(key);
  return raw ? JSON.parse(raw) : [];
}

/**
 * Agrega un ID al arreglo de tareas del usuario.
 * Se llama justo después de hacer POST a la API y recibir el ID generado.
 */
function addTodoId(userId, id) {
  const key = KEYS.TODO_IDS_PREFIX + userId;
  const ids = getTodoIds(userId);
  if (!ids.includes(id)) {
    ids.push(id);
    localStorage.setItem(key, JSON.stringify(ids));
  }
}

/**
 * Elimina un ID del arreglo de tareas del usuario.
 * Se llama después de hacer DELETE exitoso en la API.
 */
function removeTodoId(userId, id) {
  const key = KEYS.TODO_IDS_PREFIX + userId;
  const ids = getTodoIds(userId).filter(i => i !== id);
  localStorage.setItem(key, JSON.stringify(ids));
}