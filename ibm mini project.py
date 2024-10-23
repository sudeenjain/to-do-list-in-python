import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

TASKS_FILE = "tasks.json"

class Task:
    def __init__(self, title, due_date, priority):
        self.title = title
        self.due_date = due_date
        self.priority = priority

    def to_dict(self):
        return {
            'title': self.title,
            'due_date': self.due_date,
            'priority': self.priority,
        }

    @staticmethod
    def from_dict(data):
        return Task(data['title'], data['due_date'], data['priority'])

class ToDoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List Application")
        
        self.tasks = self.load_tasks()
        
        self.frame = tk.Frame(self.master)
        self.frame.pack(pady=10)
        
        self.task_listbox = tk.Listbox(self.frame, width=50, height=10)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.update_task_listbox()
        
        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.task_listbox.yview)

        self.add_task_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=5)

        self.delete_task_button = tk.Button(self.master, text="Delete Task", command=self.delete_task)
        self.delete_task_button.pack(pady=5)

        self.edit_task_button = tk.Button(self.master, text="Edit Task", command=self.edit_task)
        self.edit_task_button.pack(pady=5)

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as file:
                return [Task.from_dict(task) for task in json.load(file)]
        return []

    def save_tasks(self):
        with open(TASKS_FILE, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file)

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, f"{task.title} (Due: {task.due_date}, Priority: {task.priority})")

    def add_task(self):
        title = simpledialog.askstring("Task Title", "Enter task title:")
        if title:
            due_date = simpledialog.askstring("Due Date", "Enter due date (YYYY-MM-DD):")
            priority = simpledialog.askstring("Priority", "Enter priority (Low, Medium, High):")
            self.tasks.append(Task(title, due_date, priority))
            self.save_tasks()
            self.update_task_listbox()

    def delete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_task_index]
            self.save_tasks()
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to delete.")

    def edit_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            task = self.tasks[selected_task_index]
            new_title = simpledialog.askstring("Task Title", "Edit task title:", initialvalue=task.title)
            new_due_date = simpledialog.askstring("Due Date", "Edit due date (YYYY-MM-DD):", initialvalue=task.due_date)
            new_priority = simpledialog.askstring("Priority", "Edit priority (Low, Medium, High):", initialvalue=task.priority)
            if new_title and new_due_date and new_priority:
                task.title = new_title
                task.due_date = new_due_date
                task.priority = new_priority
                self.save_tasks()
                self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to edit.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()



