from flask import Flask, request
from flask import jsonify
import json
import os

app = Flask(__name__)
TASKS_FILE = 'tasks.json'

# Helper function to load tasks from JSON file
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

# Helper function to save tasks to JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Validation function
def validate_task(data):
    required_fields = ['id', 'title', 'description', 'status']
    valid_statuses = ['To Do', 'In Progress', 'Completed']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return f"'{field}' is required.", False
    if data['status'] not in valid_statuses:
        return f"Invalid status. Choose from {valid_statuses}.", False
    return "", True

# Get tasks (optional status filter)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = load_tasks()
    status = request.args.get('status')
    if status:
        tasks = [task for task in tasks if task['status'] == status]
    return jsonify(tasks), 200

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    tasks = load_tasks()
    data = request.get_json()
    
    message, valid = validate_task(data)
    if not valid:
        return jsonify({'error': message}), 400

    if any(task['id'] == data['id'] for task in tasks):
        return jsonify({'error': 'Task ID already exists.'}), 400

    tasks.append(data)
    save_tasks(tasks)
    return jsonify({'message': 'Task created successfully.'}), 201

# Update an existing task
@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    tasks = load_tasks()
    data = request.get_json()
    
    for task in tasks:
        if task['id'] == task_id:
            task.update(data)
            save_tasks(tasks)
            return jsonify({'message': 'Task updated successfully.'}), 200

    return jsonify({'error': 'Task not found.'}), 404

# Delete a task
@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = load_tasks()
    updated_tasks = [task for task in tasks if task['id'] != task_id]

    if len(updated_tasks) == len(tasks):
        return jsonify({'error': 'Task not found.'}), 404

    save_tasks(updated_tasks)
    return jsonify({'message': 'Task deleted successfully.'}), 200

if __name__ == '__main__':
    app.run(debug=True)
