from datetime import datetime

# TODO add more to this class
class Task:
    def __init__(self, name: str, priority: int, duration: int, due: datetime):
        self.name: str = name
        self.priority: int = priority
        self.duration: int = duration
        self.due: datetime = due
    
    def __str__(self):
        return f"name: {self.name}; priority: {self.priority}; duration: {self.duration}; due: {self.due}"
    
tasks_to_allocate = []
