// ui.js — Todas las funciones que tocan el DOM

const PRIORITY_CONFIG = {
  alta:  { label: 'Alta',  cls: 'priority-alta' },
  media: { label: 'Media', cls: 'priority-media' },
  baja:  { label: 'Baja',  cls: 'priority-baja' },
};

/**
 * Formatea una fecha YYYY-MM-DD para mostrarla al usuario.
 * Marca como vencida si es anterior a hoy.
 */
function formatDueDate(dueDate) {
  if (!dueDate) return '';
  const [year, month, day] = dueDate.split('-');
  const due   = new Date(year, month - 1, day);
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const isOverdue = due < today;
  const label = due.toLocaleDateString('es-CR', { day: 'numeric', month: 'short' });
  return `<span class="due-date ${isOverdue ? 'overdue' : ''}">${isOverdue ? '⚠ ' : '📅 '}${label}</span>`;
}

/**
 * Renderiza la lista de tareas en el DOM.
 */
function renderTodos(todos) {
  const list = document.getElementById('todo-list');

  if (todos.length === 0) {
    list.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">✓</div>
        <p>No hay tareas aquí.</p>
        <span>¡Agrega una nueva tarea para comenzar!</span>
      </div>`;
    return;
  }

  // Ordenar: Alta primero, luego Media, luego Baja
  const order = { alta: 0, media: 1, baja: 2 };
  const sorted = [...todos].sort((a, b) => {
    const pa = order[a.data?.priority] ?? 1;
    const pb = order[b.data?.priority] ?? 1;
    return pa - pb;
  });

  list.innerHTML = sorted.map(todo => {
    const priority = todo.data?.priority || 'media';
    const pConfig  = PRIORITY_CONFIG[priority] || PRIORITY_CONFIG.media;
    const dateHtml = formatDueDate(todo.data?.dueDate);

    return `
    <li class="todo-item ${todo.data?.completed ? 'completed' : ''}" data-id="${todo.id}"
        data-priority="${priority}" data-due="${todo.data?.dueDate || ''}">

      <button class="toggle-btn" onclick="handleToggle('${todo.id}')" title="Cambiar estado">
        <span class="check-icon">${todo.data?.completed ? '✓' : ''}</span>
      </button>

      <div class="todo-content">
        <span class="todo-text">${escapeHtml(todo.name)}</span>
        <div class="todo-meta">
          <span class="priority-badge ${pConfig.cls}">${pConfig.label}</span>
          ${dateHtml}
        </div>
      </div>

      <div class="todo-actions">
        <button class="edit-btn" onclick="openEditPanel('${todo.id}')" title="Editar">✏️</button>
        <button class="delete-btn" onclick="handleDelete('${todo.id}')" title="Eliminar">🗑️</button>
      </div>
    </li>`;
  }).join('');
}

/**
 * Abre el panel de edición inline debajo de una tarea.
 * Muestra campos para título, prioridad y fecha.
 */
function openEditPanel(todoId) {
  // Cerrar cualquier panel abierto previamente
  document.querySelectorAll('.edit-panel').forEach(p => p.remove());

  const todoEl   = document.querySelector(`[data-id="${todoId}"]`);
  const title    = todoEl.querySelector('.todo-text').textContent;
  const priority = todoEl.dataset.priority || 'media';
  const dueDate  = todoEl.dataset.due || '';

  const panel = document.createElement('div');
  panel.className = 'edit-panel';
  panel.innerHTML = `
    <input  type="text"  class="ep-title"    value="${escapeHtml(title)}" maxlength="200" placeholder="Título" />
    <div class="ep-row">
      <select class="ep-priority">
        <option value="alta"  ${priority === 'alta'  ? 'selected' : ''}>Alta</option>
        <option value="media" ${priority === 'media' ? 'selected' : ''}>Media</option>
        <option value="baja"  ${priority === 'baja'  ? 'selected' : ''}>Baja</option>
      </select>
      <input type="date" class="ep-date" value="${dueDate}" />
    </div>
    <div class="ep-actions">
      <button class="btn btn-primary ep-save">Guardar</button>
      <button class="btn btn-ghost ep-cancel">Cancelar</button>
    </div>`;

  todoEl.insertAdjacentElement('afterend', panel);
  panel.querySelector('.ep-title').focus();

  panel.querySelector('.ep-save').addEventListener('click', async () => {
    const user        = getSession();
    const newTitle    = panel.querySelector('.ep-title').value.trim();
    const newPriority = panel.querySelector('.ep-priority').value;
    const newDueDate  = panel.querySelector('.ep-date').value;
    const completed   = todoEl.classList.contains('completed');
    const todoObj     = { id: todoId, name: title, data: { completed, userId: user.email } };

    panel.remove();
    await editTodo(todoObj, newTitle || title, user.email, newPriority, newDueDate);
  });

  panel.querySelector('.ep-cancel').addEventListener('click', () => panel.remove());

  panel.querySelector('.ep-title').addEventListener('keydown', (e) => {
    if (e.key === 'Escape') panel.remove();
  });
}

async function handleToggle(todoId) {
  const user    = getSession();
  const todoEl  = document.querySelector(`[data-id="${todoId}"]`);
  const textEl  = todoEl.querySelector('.todo-text');
  const text    = textEl.textContent;
  const completed  = todoEl.classList.contains('completed');
  const priority   = todoEl.dataset.priority || 'media';
  const dueDate    = todoEl.dataset.due || '';
  const todoObj = { id: todoId, name: text, data: { completed, userId: user.email, priority, dueDate } };
  await toggleTodo(todoObj, user.email);
}

async function handleDelete(todoId) {
  const user = getSession();
  if (confirm('¿Eliminar esta tarea?')) {
    await deleteTodo(todoId, user.email);
  }
}

function showLoading(visible) {
  const spinner = document.getElementById('loading-spinner');
  if (spinner) spinner.style.display = visible ? 'flex' : 'none';
}

function showError(message) {
  const toast = document.getElementById('error-toast');
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
}

function showSuccess(message) {
  const toast = document.getElementById('success-toast');
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3000);
}

function updateStats(allTodos) {
  const total     = allTodos.length;
  const completed = allTodos.filter(t => t.data?.completed).length;
  const active    = total - completed;
  const el = document.getElementById('stats-text');
  if (el) el.textContent = `${active} pendiente${active !== 1 ? 's' : ''} · ${completed} completada${completed !== 1 ? 's' : ''}`;
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(text));
  return div.innerHTML;
}

function showFormError(formId, message) {
  const el = document.getElementById(`${formId}-error`);
  if (el) { el.textContent = message; el.style.display = 'block'; }
}

function clearFormError(formId) {
  const el = document.getElementById(`${formId}-error`);
  if (el) { el.textContent = ''; el.style.display = 'none'; }
}