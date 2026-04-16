// api.js
const API_KEY  = CONFIG.API_KEY; // Definido en config.js (excluido del repo);
const API_BASE = 'https://api.restful-api.dev/collections/todos/objects';

const API_HEADERS = {
  'Content-Type': 'application/json',
  'x-api-key': API_KEY,
};

async function apiGetTodoById(id) {
  try {
    const response = await axios.get(`${API_BASE}/${id}`, { headers: API_HEADERS });
    return response.data;
  } catch (error) {
    if (error.response && error.response.status === 404) return null;
    console.warn(`No se pudo cargar tarea ${id}:`, error.message);
    return undefined;
  }
}

/**
 * Crea una tarea con título, userId, prioridad y fecha límite.
 * @param {string} title
 * @param {string} userId
 * @param {string} priority - 'alta' | 'media' | 'baja'
 * @param {string} dueDate  - 'YYYY-MM-DD' o '' si no se definió
 */
async function apiCreateTodo(title, userId, priority = 'media', dueDate = '') {
  const payload = {
    name: title,
    data: {
      userId:    userId,
      completed: false,
      priority:  priority,
      dueDate:   dueDate,
      createdAt: new Date().toISOString().split('T')[0],
    },
  };
  const response = await axios.post(API_BASE, payload, { headers: API_HEADERS });
  return response.data;
}

/**
 * Actualiza una tarea completa (PUT = reemplazo total).
 * @param {string}  id
 * @param {string}  title
 * @param {boolean} completed
 * @param {string}  userId
 * @param {string}  priority
 * @param {string}  dueDate
 */
async function apiUpdateTodo(id, title, completed, userId, priority = 'media', dueDate = '') {
  const payload = {
    name: title,
    data: {
      userId:    userId,
      completed: completed,
      priority:  priority,
      dueDate:   dueDate,
      createdAt: new Date().toISOString().split('T')[0],
    },
  };
  const response = await axios.put(`${API_BASE}/${id}`, payload, { headers: API_HEADERS });
  return response.data;
}

async function apiDeleteTodo(id) {
  const response = await axios.delete(`${API_BASE}/${id}`, { headers: API_HEADERS });
  return response.data;
}