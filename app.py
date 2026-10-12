from flask import Flask, render_template_string, request, redirect, url_for
import json
import os

app = Flask(__name__)

DATA_FILE = '/tasks.json'

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f).get('tasks', [])
    return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump({'tasks': tasks}, f, ensure_ascii=False, indent=2)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Мои задачи</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; background: #f5f5f5; }
        h1 { color: #333; }
        .task { background: white; padding: 15px; margin: 10px 0; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .task a { color: #e74c3c; text-decoration: none; font-weight: bold; }
        form { margin-top: 20px; display: flex; }
        input[type=text] { flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 8px 0 0 8px; font-size: 16px; }
        button { padding: 12px 20px; background: #3498db; color: white; border: none; border-radius: 0 8px 8px 0; cursor: pointer; font-size: 16px; }
        button:hover { background: #2980b9; }
    </style>
</head>
<body>
    <h1>📝 Мои задачи</h1>
    {% for task in tasks %}
        <div class="task">
            <span>{{ task.text }}</span>
            <a href="/delete/{{ task.id }}">✖</a>
        </div>
    {% else %}
        <p>Список пуст. Добавьте первую задачу!</p>
    {% endfor %}
    <form action="/add" method="post">
        <input type="text" name="text" placeholder="Новая задача..." required>
        <button type="submit">Добавить</button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template_string(HTML_TEMPLATE, tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    text = request.form.get('text', '').strip()
    if text:
        tasks = load_tasks()
        new_id = max([t['id'] for t in tasks], default=0) + 1
        tasks.append({'id': new_id, 'text': text})
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
