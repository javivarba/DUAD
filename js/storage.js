// storage.js
// Analogía Flask: este archivo es como tu "models.py" pero para el browser.
// En lugar de PostgreSQL, usamos localStorage del navegador.

const KEYS = {
  USERS:           'duad_users',
  SESSION:         'duad_session',
  TODO_IDS_PREFIX: 'duad_todos_', // + email del usuario = clave única por usuario
};

// ─── USUARIOS ─────────────────────────────────────────────────────────────────

function getUsers() {
  const raw = localStorage.getItem(KEYS.USERS);
  return raw ? JSON.parse(raw) : [];
}

function saveUsers(users) {
  localStorage.setItem(KEYS.USERS, JSON.stringify(users));
}

function registerUser(name, email, password) {
  const users = getUsers();
  if (users.find(u => u.email === email)) return false;
  users.push({ name, email, password });
  saveUsers(users);
  return true;
}

function loginUser(email, password) {
  const users = getUsers();
  return users.find(u => u.email === email && u.password === password) || null;
}

// ─── SESIÓN ───────────────────────────────────────────────────────────────────

function setSession(user) {
  localStorage.setItem(KEYS.SESSION, JSON.stringify(user));
}

function getSession() {
  const raw = localStorage.getItem(KEYS.SESSION);
  return raw ? JSON.parse(raw) : null;
}

function clearSession() {
  localStorage.removeItem(KEYS.SESSION);
}

// ─── IDs DE TAREAS POR USUARIO ────────────────────────────────────────────────
// Guardamos los IDs de las tareas de cada usuario en localStorage.
// Así podemos buscarlas individualmente en la API sin traer todos los objetos.
// Analogía SQL: es como tener una tabla "user_todo_ids" con foreign keys.

/**
 * Retorna el arreglo de IDs de tareas de un usuario.
 */
function getTodoIds(userId) {
  const key = KEYS.TODO_IDS_PREFIX + userId;
  const raw = localStorage.getItem(key);
  return raw ? JSON.parse(raw) : [];
}

/**
 * Agrega un ID al arreglo de tareas del usuario.
 */
function addTodoId(userId, id) {
  const key  = KEYS.TODO_IDS_PREFIX + userId;
  const ids  = getTodoIds(userId);
  if (!ids.includes(id)) {
    ids.push(id);
    localStorage.setItem(key, JSON.stringify(ids));
  }
}

/**
 * Elimina un ID del arreglo de tareas del usuario.
 */
function removeTodoId(userId, id) {
  const key = KEYS.TODO_IDS_PREFIX + userId;
  const ids = getTodoIds(userId).filter(i => i !== id);
  localStorage.setItem(key, JSON.stringify(ids));
}