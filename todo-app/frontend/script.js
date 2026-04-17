// For local run, keep localhost. For deployment, change to your Render URL.
const API_BASE_URL = "http://127.0.0.1:5000";

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
    try {
        const response = await fetch(API_BASE_URL + "/tasks");
        const data = await response.json();

        renderTasks(data.tasks || []);
        showMessage("");
    } catch (error) {
        showMessage("Could not connect to backend.");
    }
}


// Send a new task to backend.
async function addTask() {
    const task = taskInput.value.trim();

    if (task === "") {
        showMessage("Task cannot be empty.");
        return;
    }

    try {
        const response = await fetch(API_BASE_URL + "/add", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ task: task })
        });

        const data = await response.json();

        if (!response.ok) {
            showMessage(data.error || "Could not add task.");
            return;
        }

        taskInput.value = "";
        showMessage(data.message);
        loadTasks();
    } catch (error) {
        showMessage("Could not connect to backend.");
    }
}


// Delete one task using its index.
async function deleteTask(index) {
    try {
        const response = await fetch(API_BASE_URL + "/delete/" + index, {
            method: "DELETE"
        });

        const data = await response.json();

        if (!response.ok) {
            showMessage(data.error || "Could not delete task.");
            return;
        }

        showMessage(data.message);
        loadTasks();
    } catch (error) {
        showMessage("Could not connect to backend.");
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
