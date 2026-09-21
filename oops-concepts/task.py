class Task:
    # Class attribute (shared by all instances)
    category = "General"

    def __init__(self, task_id: int, title: str):
        # Instance attributes (unique to each instance)
        self.task_id = task_id
        self.title = title
        self.is_completed = False

    def mark_complete(self):
        self.is_completed = True

# Creating an object
t1 = Task(1, "Parse Log File")
t1.mark_complete()