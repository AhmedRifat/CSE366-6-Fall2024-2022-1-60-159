import pygame
import numpy as np

class Environment:
    def __init__(self, num_classes, num_students):
        self.num_classes = num_classes
        self.num_students = num_students
        self.slot_durations = np.random.randint(1, 3, size=num_classes)
        self.class_priorities = np.random.randint(1, 6, size=num_classes)
        self.student_preferences = np.random.uniform(0.5, 1.5, size=num_students)

        self.student_class_preferences = np.random.uniform(0.5, 1.5, size=(self.num_students, self.num_classes))
        self.student_availability = np.random.randint(0, 2, size=(num_students, num_classes))

    def generate_assignments(self):
        """
        Randomly assign class to students for initial population in the genetic algorithm.
        """
        return [np.random.randint(0, self.num_students, size=self.num_classes) for _ in range(50)]

    def draw_grid(self, screen, font, class_assignments):
        """
        Draw a grid representing the slot durations on the Pygame screen.
        Each row is a student, each column is a class, colors are based on slot durations, and annotations
        show class priorities and durations inside the grid.
        """
        screen.fill((255, 255, 255))  # Background color
        
        color_map = [(0, 0, 255 - i * 150) for i in range(3)]  # Color gradient for durations
        
        # Set spacing and margins
        cell_size = 60
        margin_left = 150
        margin_top = 100

        # Display class names on the top (X-axis labels)
        for col in range(self.num_classes):
            task_text = font.render(f"Slot {col + 1}", True, (0, 0, 0))
            screen.blit(task_text, (margin_left + col * cell_size + cell_size // 3, margin_top - 30))

        # Draw each student row with class assigned
        for row in range(self.num_students):
            # Display student preference on the left of each row
            preference_text = font.render(f"Preference: {self.student_preferences[row]:.2f}", True, (0, 0, 0))
            screen.blit(preference_text, (10, margin_top + row * cell_size + cell_size // 3))

            for col in range(self.num_classes):
                # Determine if this class is assigned to the current student
                assigned_student = class_assignments[col]
                
                # Set color based on task duration
                color = color_map[self.slot_durations[col] - 1] if assigned_student == row else (200, 200, 200)
                
                # Draw the cell
                cell_rect = pygame.Rect(
                    margin_left + col * cell_size,
                    margin_top + row * cell_size,
                    cell_size,
                    cell_size
                )
                pygame.draw.rect(screen, color, cell_rect)
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)  # Draw cell border

                # Display task priority and duration within the cell
                priority_text = font.render(f"P{self.class_priorities[col]}", True, (255, 255, 255) if assigned_student == row else (0, 0, 0))
                duration_text = font.render(f"{self.slot_durations[col]}h", True, (255, 255, 255) if assigned_student == row else (0, 0, 0))
                screen.blit(priority_text, (cell_rect.x + 5, cell_rect.y + 5))
                screen.blit(duration_text, (cell_rect.x + 5, cell_rect.y + 25))

