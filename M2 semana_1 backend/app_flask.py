from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
TASKS_FILE = 'tasks.json'

# ---------------------- Helper Functions ----------------------

def load_tasks():
    """Load tasks from JSON file with error handling."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        app.logger.error(f"[ERROR] Failed to load tasks: {e}")
        raise Exception("Could not read tasks from storage.")

def save_tasks(tasks):
    """Save tasks to JSON file with error handling."""
    try:
        with open(TASKS_FILE, 'w') as file:
            json.dump(tasks, file, indent=4)
    except IOError as e:
        app.logger.error(f"[ERROR] Failed to save tasks: {e}")
        raise Exception("Could not save task to storage.")

def validate_task(data):
    """Validate required fields and normalize the input."""
    required_fields = ['id', 'title', 'description', 'status']
    valid_statuses = ['To Do', 'In Progress', 'Completed']

    data['id'] = str(data.get('id', '')).strip()
    data['status'] = str(data.get('status', '')).strip().title()

    for field in required_fields:
        if not data.get(field):
            return f"'{field}' is required.", False

    if data['status'] not in valid_statuses:
        return f"Invalid status. Must be one of: {valid_statuses}.", False

    return "", True

# ---------------------- Routes ----------------------

@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        tasks = load_tasks()
        status_filter = request.args.get('status')

        if status_filter:
            status_filter = status_filter.strip().lower()
            tasks = [task for task in tasks if task['status'].lower() == status_filter]

        return jsonify(tasks), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        tasks = load_tasks()
        data = request.get_json()

        message, valid = validate_task(data)
        if not valid:
            return jsonify({'error': message}), 400

        if any(str(task['id']) == str(data['id']) for task in tasks):
            return jsonify({'error': 'Task ID already exists.'}), 400

        tasks.append(data)
        save_tasks(tasks)
        return jsonify({'message': 'Task created successfully.'}), 201
    except Exception:
        return jsonify({'error': 'Task could not be created due to an internal error.'}), 500

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        tasks = load_tasks()
        data = request.get_json()

        for task in tasks:
            if str(task['id']) == str(task_id):
                updated_task = {**task, **data}
                message, valid = validate_task(updated_task)
                if not valid:
                    return jsonify({'error': message}), 400

                task.update(updated_task)
                save_tasks(tasks)
                return jsonify({'message': 'Task updated successfully.'}), 200

        return jsonify({'error': 'Task not found.'}), 404
    except Exception:
        return jsonify({'error': 'Task could not be updated due to an internal error.'}), 500

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        tasks = load_tasks()
        updated_tasks = [task for task in tasks if str(task['id']) != str(task_id)]

        if len(updated_tasks) == len(tasks):
            return jsonify({'error': 'Task not found.'}), 404

        save_tasks(updated_tasks)
        return jsonify({'message': 'Task deleted successfully.'}), 200
    except Exception:
        return jsonify({'error': 'Task could not be deleted due to an internal error.'}), 500

# ---------------------- Main App ----------------------

if __name__ == '__main__':
    app.run(debug=True)
