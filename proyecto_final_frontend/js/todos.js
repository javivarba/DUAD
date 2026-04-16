// todos.js

async function loadTodos(userId, filter = 'all') {
  try {
    showLoading(true);
    const ids = getTodoIds(userId);

    if (ids.length === 0) {
      renderTodos([]);
      updateStats([]);
      return;
    }

    const results = await Promise.all(ids.map(id => apiGetTodoById(id)));

    const validTodos = [];
    const notFoundIds = [];

    results.forEach((todo, index) => {
      if (todo === null)            notFoundIds.push(ids[index]);
      else if (todo !== undefined)  validTodos.push(todo);
    });

    notFoundIds.forEach(id => removeTodoId(userId, id));

    let filtered = validTodos;
    if (filter === 'active')    filtered = validTodos.filter(t => t.data && !t.data.completed);
    if (filter === 'completed') filtered = validTodos.filter(t => t.data && t.data.completed);

    renderTodos(filtered);
    updateStats(validTodos);

  } catch (error) {
    showError('No se pudieron cargar las tareas.');
    console.error('[loadTodos]', error);
  } finally {
    showLoading(false);
  }
}

/**
 * Crea una tarea con prioridad y fecha límite.
 */
async function createTodo(title, userId, priority = 'media', dueDate = '') {
  if (!title.trim()) return;
  try {
    showLoading(true);
    const created = await apiCreateTodo(title.trim(), userId, priority, dueDate);
    if (!created || !created.id) { showError('Error al crear la tarea.'); return; }
    addTodoId(userId, created.id);
    await loadTodos(userId, getCurrentFilter());
  } catch (error) {
    showError('No se pudo crear la tarea.');
    console.error('[createTodo]', error.response?.data || error.message);
  } finally {
    showLoading(false);
  }
}

/**
 * Toggle completed — preserva prioridad y fecha del objeto original.
 */
async function toggleTodo(todo, userId) {
  try {
    showLoading(true);
    const newCompleted = !todo.data.completed;
    const priority = todo.data.priority || 'media';
    const dueDate  = todo.data.dueDate  || '';
    await apiUpdateTodo(todo.id, todo.name, newCompleted, userId, priority, dueDate);
    await loadTodos(userId, getCurrentFilter());
  } catch (error) {
    showError('No se pudo actualizar la tarea.');
    console.error('[toggleTodo]', error.response?.data || error.message);
  } finally {
    showLoading(false);
  }
}

/**
 * Edita una tarea — acepta todos los campos editables.
 */
async function editTodo(todo, newTitle, userId, priority, dueDate) {
  if (!newTitle.trim()) return;
  try {
    await apiUpdateTodo(
      todo.id,
      newTitle.trim(),
      todo.data.completed,
      userId,
      priority || todo.data.priority || 'media',
      dueDate  !== undefined ? dueDate : (todo.data.dueDate || '')
    );
    await loadTodos(userId, getCurrentFilter());
  } catch (error) {
    showError('No se pudo editar la tarea.');
    console.error('[editTodo]', error.response?.data || error.message);
  }
}

async function deleteTodo(id, userId) {
  try {
    showLoading(true);
    await apiDeleteTodo(id);
    removeTodoId(userId, id);
    await loadTodos(userId, getCurrentFilter());
  } catch (error) {
    showError('No se pudo eliminar la tarea.');
    console.error('[deleteTodo]', error.response?.data || error.message);
  } finally {
    showLoading(false);
  }
}

function getCurrentFilter() {
  const active = document.querySelector('.filter-btn.active');
  return active ? active.dataset.filter : 'all';
}