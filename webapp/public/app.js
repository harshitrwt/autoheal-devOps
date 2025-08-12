const API_URL = '/api/todos';

async function fetchTodos() {
  const res = await fetch(API_URL);
  const todos = await res.json();
  const list = document.getElementById('todoList');
  list.innerHTML = '';
  todos.forEach(todo => {
    const li = document.createElement('li');
    li.className = todo.done ? 'done' : '';
    li.innerHTML = `
      <span onclick="toggleDone(${todo.id}, ${!todo.done})">${todo.text}</span>
      <button onclick="deleteTodo(${todo.id})">❌</button>
    `;
    list.appendChild(li);
  });
}

async function addTodo() {
  const text = document.getElementById('todoText').value.trim();
  if (!text) return;
  await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  document.getElementById('todoText').value = '';
  fetchTodos();
}

async function toggleDone(id, done) {
  await fetch(`${API_URL}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ done })
  });
  fetchTodos();
}

async function deleteTodo(id) {
  await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
  fetchTodos();
}

fetchTodos();
