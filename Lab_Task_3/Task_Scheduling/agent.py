import numpy as np

class Agent:
    def __init__(self, id, preference):
        self.id = id  # Unique identifier for each student
        self.preference = preference  # Preference factor of the student
        self.slots = []  # List of slots assigned to this student

    def assign_class(self, class_duration, class_priority):
        """
        Assign a class to the student and calculate effective class time
        considering student preference and class priority.
        """
        effective_time = class_duration / self.preference * class_priority
        self.slots.append(effective_time)

    def total_time(self):
        """Calculate the total time required by this student to complete all class."""
        return sum(self.slots)

    def reset_classes(self):
        """Clear the classes assigned to the agent."""
        self.slots = []


