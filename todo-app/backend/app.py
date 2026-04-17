from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# Enable CORS so frontend can call this backend from another origin.
CORS(app)

# Keep tasks.txt in the same folder as app.py.
TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.txt")


# Read all tasks from the text file and return a list.
def read_tasks():
    tasks = []

    if not os.path.exists(TASKS_FILE):
        return tasks

    file = open(TASKS_FILE, "r", encoding="utf-8")
    lines = file.readlines()
    file.close()

    for line in lines:
        task = line.strip()
        if task != "":
            tasks.append(task)

    return tasks


# Save the full task list to the text file.
def write_tasks(tasks):
    file = open(TASKS_FILE, "w", encoding="utf-8")

    for task in tasks:
        file.write(task + "\n")

    file.close()


# GET /tasks -> Return all tasks.
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = read_tasks()
    return jsonify({"tasks": tasks})


# POST /add -> Add a new task.
@app.route("/add", methods=["POST"])
def add_task():
    data = request.get_json(silent=True) or {}
    task = str(data.get("task", "")).strip()

    if task == "":
        return jsonify({"error": "Task cannot be empty."}), 400

    tasks = read_tasks()
    tasks.append(task)
    write_tasks(tasks)

    return jsonify({"message": "Task added.", "tasks": tasks}), 201


# DELETE /delete/<index> -> Delete task by index.
@app.route("/delete/<int:index>", methods=["DELETE"])
def delete_task(index):
    tasks = read_tasks()

    if index < 0 or index >= len(tasks):
        return jsonify({"error": "Invalid task index."}), 400

    deleted_task = tasks.pop(index)
    write_tasks(tasks)

    return jsonify({"message": "Task deleted.", "deleted": deleted_task, "tasks": tasks})


if __name__ == "__main__":
    # Use Render's PORT in deployment, or 5000 for local run.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
