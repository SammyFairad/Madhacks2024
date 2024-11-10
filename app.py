from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# In-memory task storage with completion status and descriptions
tasks = []
task_descriptions = {}

@app.route('/')
def index():
    """Render the main page with the list of tasks."""
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    """Add a new task."""
    task_text = request.form.get('task').strip()
    if task_text:
        new_task_id = len(tasks)
        tasks.append({"text": task_text, "completed": False})
        task_descriptions[new_task_id] = {"text": ""}
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    """Toggle the completion status of a task."""
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = not tasks[task_id]['completed']
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    """Edit a task's text."""
    if 0 <= task_id < len(tasks):
        new_text = request.form.get('edited_text', '').strip()
        if new_text:
            tasks[task_id]['text'] = new_text
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """Delete a task and its description."""
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        task_descriptions.pop(task_id, None)
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>')
def view_task(task_id):
    """View a specific task's details."""
    if 0 <= task_id < len(tasks):
        return render_template(
            'task.html',
            task_name=tasks[task_id]['text'],
            task_description=task_descriptions.get(task_id, {}).get('text', ''),
            task_id=task_id
        )
    return redirect(url_for('index'))

@app.route('/save_task/<int:task_id>', methods=['POST'])
def save_task(task_id):
    """Save the description of a task via AJAX."""
    if task_id in task_descriptions:
        new_text = request.json.get('text', '').strip()
        if new_text:
            task_descriptions[task_id]['text'] = new_text
            return jsonify({"status": "success"}), 200
    return jsonify({"status": "error"}), 400

@app.route('/theme/<string:theme>', methods=['POST'])
def save_theme(theme):
    """Save the selected theme for persistence."""
    if theme in ['default', 'pink-lofi', 'brown-library', 'green-cottagecore', 'purple-cosmos']:
        return jsonify({"status": "success", "theme": theme}), 200
    return jsonify({"status": "error"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
