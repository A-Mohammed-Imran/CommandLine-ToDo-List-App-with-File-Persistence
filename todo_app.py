# Simple Command-Line To-Do List App with File Persistence
# This program lets users add, view, and delete tasks saved in a text file.

FILE_NAME = "tasks.txt"


# Read all tasks from the file and return them as a list.
def load_tasks():
    try:
        file = open(FILE_NAME, "r")
        lines = file.readlines()
        file.close()

        tasks = []
        for line in lines:
            task = line.strip()
            if task != "":
                tasks.append(task)
        return tasks
    except FileNotFoundError:
        # If the file does not exist yet, return an empty list.
        return []


# Save the full list of tasks back to the file.
def save_tasks(tasks):
    file = open(FILE_NAME, "w")
    for task in tasks:
        file.write(task + "\n")
    file.close()


# Ask the user for a new task and save it.
def add_task():
    task = input("Enter a new task: ").strip()

    if task == "":
        print("Task cannot be empty.")
        return

    tasks = load_tasks()
    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully.")


# Display all tasks with numbers.
def view_tasks():
    tasks = load_tasks()

    if len(tasks) == 0:
        print("No tasks found.")
        return

    print("\nYour Tasks:")
    for i in range(len(tasks)):
        print(str(i + 1) + ". " + tasks[i])


# Delete a task by number.
def delete_task():
    tasks = load_tasks()

    if len(tasks) == 0:
        print("No tasks to delete.")
        return

    print("\nTasks:")
    for i in range(len(tasks)):
        print(str(i + 1) + ". " + tasks[i])

    choice = input("Enter task number to delete: ").strip()

    if not choice.isdigit():
        print("Invalid input. Please enter a number.")
        return

    task_number = int(choice)

    if task_number < 1 or task_number > len(tasks):
        print("Invalid task number.")
        return

    removed_task = tasks.pop(task_number - 1)
    save_tasks(tasks)
    print("Deleted task: " + removed_task)


# Show the main menu and run the app until user exits.
def main():
    while True:
        print("\n--- To-Do List Menu ---")
        print("1. Add task")
        print("2. View tasks")
        print("3. Delete task")
        print("4. Exit")

        option = input("Choose an option (1-4): ").strip()

        if option == "1":
            add_task()
        elif option == "2":
            view_tasks()
        elif option == "3":
            delete_task()
        elif option == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")


# Start the program.
main()
