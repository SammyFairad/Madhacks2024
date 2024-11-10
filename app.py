from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# In-memory task storage with completion status and descriptions
tasks = []
task_descriptions = {}

# Hugging Face API settings
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-j-6B"
HUGGING_FACE_API_TOKEN = "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"

def get_ai_tips(task_name):
    """Fetch tips and tricks from Hugging Face's GPT-J model for a given task name."""
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_TOKEN}"}
    prompt = f"Provide tips and tricks for the following task: {task_name}"

    response = requests.post(
        HUGGING_FACE_API_URL,
        headers=headers,
        json={"inputs": prompt, "parameters": {"max_new_tokens": 100}}
    )
    
    # Handle response
    if response.status_code == 200:
        data = response.json()
        return data[0]['generated_text']
    else:
        return "Could not retrieve tips. Please try again later."

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_text = request.form.get('task').strip()
    if task_text:
        new_task_id = len(tasks)
        tasks.append({"text": task_text, "completed": False})
        task_descriptions[new_task_id] = {"text": task_text}
    return redirect(url_for('index'))

@app.route('/task/<int:task_id>')
def view_task(task_id):
    if 0 <= task_id < len(tasks):
        task = task_descriptions[task_id]
        
        # Get tips using AI model for this task
        ai_tips = get_ai_tips(task['text'])
        
        # Render the details page, passing the task and the generated tips
        return render_template('task.html', task=task, task_id=task_id, ai_tips=ai_tips)
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
        task_descriptions.pop(task_id, None)
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    if task_id in task_descriptions:
        new_text = request.form.get('task-input').strip()
        if new_text:
            tasks[task_id]['text'] = new_text
            task_descriptions[task_id]['text'] = new_text
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090, debug=True)
