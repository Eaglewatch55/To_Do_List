task_list = ["Do yoga",
             "Make a breakfast",
             "Learn the basics of SQL",
             "Learn about ORM"]

print("Today:")
for i, task in enumerate(task_list):
    print(f"{i + 1}) {task}")
