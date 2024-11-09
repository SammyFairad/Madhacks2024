from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory task storage with completion status
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task').strip()  # Trim spaces here
    if task_text:
        tasks.append({"text": task_text, "completed": False})
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['completed'] = not tasks[task_id]['completed']
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('index'))

@app.route('/toggle_edit/<int:task_id>', methods=['POST'])
def toggle_edit(task_id):
    if 0 <= task_id < len(tasks):
        # Toggle the editing state
        tasks[task_id]['editing'] = not tasks[task_id].get('editing', False)
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    if 0 <= task_id < len(tasks):
        new_text = request.form.get('edited_text')
        tasks[task_id]['text'] = new_text
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
