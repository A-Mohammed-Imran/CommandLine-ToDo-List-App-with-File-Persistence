// Render backend URL (deployed Flask API).
const API_BASE_URL = "https://commandline-todo-list-app-with-file.onrender.com";

const taskInput = document.getElementById("taskInput");
const addButton = document.getElementById("addBtn");
const taskList = document.getElementById("taskList");
const message = document.getElementById("message");


// Show simple text messages to the user.
function showMessage(text) {
    message.textContent = text;
}


// Draw tasks in the list with a delete button for each task.
function renderTasks(tasks) {
    taskList.innerHTML = "";

    if (tasks.length === 0) {
        const emptyItem = document.createElement("li");
        emptyItem.textContent = "No tasks yet.";
        taskList.appendChild(emptyItem);
        return;
    }

    tasks.forEach(function (task, index) {
        const item = document.createElement("li");

        const text = document.createElement("span");
        text.textContent = (index + 1) + ". " + task;

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.className = "delete-btn";
        deleteButton.addEventListener("click", function () {
            deleteTask(index);
        });

        item.appendChild(text);
        item.appendChild(deleteButton);
        taskList.appendChild(item);
    });
}


// Load all tasks from backend.
async function loadTasks() {
    showMessage("Loading...");

    try {
        const response = await fetch(API_BASE_URL + "/tasks", {
            method: "GET",
            mode: "cors"
        });

        let data = {};
        try {
            data = await response.json();
        } catch (error) {
            data = {};
        }

        if (!response.ok) {
            showMessage(data.error || "Server waking up, please wait...");
            return;
        }

        renderTasks(data.tasks || []);
        showMessage("Tasks loaded.");
    } catch (error) {
        showMessage("Server waking up, please wait...");
    }
}


// Send a new task to backend.
async function addTask() {
    const task = taskInput.value.trim();

    if (task === "") {
        showMessage("Task cannot be empty.");
        return;
    }

    showMessage("Loading...");

    try {
        const response = await fetch(API_BASE_URL + "/add", {
            method: "POST",
            mode: "cors",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ task: task })
        });

        let data = {};
        try {
            data = await response.json();
        } catch (error) {
            data = {};
        }

        if (!response.ok) {
            showMessage(data.error || "Could not add task.");
            return;
        }

        taskInput.value = "";
        showMessage(data.message);
        loadTasks();
    } catch (error) {
        showMessage("Server waking up, please wait...");
    }
}


// Delete one task using its index.
async function deleteTask(index) {
    showMessage("Loading...");

    try {
        const response = await fetch(API_BASE_URL + "/delete/" + index, {
            method: "DELETE",
            mode: "cors"
        });

        let data = {};
        try {
            data = await response.json();
        } catch (error) {
            data = {};
        }

        if (!response.ok) {
            showMessage(data.error || "Could not delete task.");
            return;
        }

        showMessage(data.message);
        loadTasks();
    } catch (error) {
        showMessage("Server waking up, please wait...");
    }
}


// Button click and Enter key both add a task.
addButton.addEventListener("click", addTask);

taskInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        addTask();
    }
});


// Load tasks when page opens.
loadTasks();
