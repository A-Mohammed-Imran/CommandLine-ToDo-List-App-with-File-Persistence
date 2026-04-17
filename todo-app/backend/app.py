from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# Enable CORS so frontend can call this backend from another origin.
CORS(app)

# Keep tasks.txt in the same folder as app.py.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TASKS_FILE = os.path.join(BASE_DIR, "tasks.txt")


# Create tasks.txt if it does not exist.
def ensure_tasks_file():
    if not os.path.exists(TASKS_FILE):
        try:
            file = open(TASKS_FILE, "w", encoding="utf-8")
            file.close()
        except OSError:
            return False
    return True


# Read all tasks from the text file and return a list.
def read_tasks():
    tasks = []

    if not ensure_tasks_file():
        return tasks

    try:
        file = open(TASKS_FILE, "r", encoding="utf-8")
        lines = file.readlines()
        file.close()

        for line in lines:
            task = line.strip()
            if task != "":
                tasks.append(task)
    except OSError:
        return []

    return tasks


# Save the full task list to the text file.
def write_tasks(tasks):
    if not ensure_tasks_file():
        return False

    try:
        file = open(TASKS_FILE, "w", encoding="utf-8")

        for task in tasks:
            file.write(task + "\n")

        file.close()
        return True
    except OSError:
        return False


# GET /tasks -> Return all tasks.
@app.route("/tasks", methods=["GET"])
def get_tasks():
    try:
        tasks = read_tasks()
        return jsonify({"tasks": tasks}), 200
    except Exception:
        return jsonify({"error": "Could not load tasks."}), 500


# POST /add -> Add a new task.
@app.route("/add", methods=["POST"])
def add_task():
    try:
        data = request.get_json(silent=True) or {}
        task = str(data.get("task", "")).strip()

        if task == "":
            return jsonify({"error": "Task cannot be empty."}), 400

        tasks = read_tasks()
        tasks.append(task)

        if not write_tasks(tasks):
            return jsonify({"error": "Could not save task."}), 500

        return jsonify({"message": "Task added.", "tasks": tasks}), 201
    except Exception:
        return jsonify({"error": "Could not add task."}), 500


# DELETE /delete/<index> -> Delete task by index.
@app.route("/delete/<int:index>", methods=["DELETE"])
def delete_task(index):
    try:
        tasks = read_tasks()

        if index < 0 or index >= len(tasks):
            return jsonify({"error": "Invalid task index."}), 400

        deleted_task = tasks.pop(index)

        if not write_tasks(tasks):
            return jsonify({"error": "Could not delete task."}), 500

        return jsonify({"message": "Task deleted.", "deleted": deleted_task, "tasks": tasks}), 200
    except Exception:
        return jsonify({"error": "Could not delete task."}), 500


# Create the tasks file on startup so file operations are ready.
ensure_tasks_file()


if __name__ == "__main__":
    # Render gives a PORT environment variable. Local default is 5000.
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
