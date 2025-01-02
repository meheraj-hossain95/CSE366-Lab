import pygame
import numpy as np

class Environment:
    def __init__(self, num_classes, num_students, num_time_slots):
        self.num_classes = num_classes
        self.num_students = num_students
        self.num_time_slots = num_time_slots

        self.class_durations = np.random.randint(1, 3, size=num_classes)
        self.class_priorities = np.random.randint(1, 6, size=num_classes)

        self.student_availability = np.random.choice([0, 1], size=(num_students, num_time_slots), p=[0.3, 0.7])
        self.student_preferences = np.random.randint(1, 6, size=(num_students, num_time_slots))

    def generate_initial_population(self, population_size):
        population = []
        for _ in range(population_size):
            schedule = [(np.random.randint(0, self.num_students), np.random.randint(0, self.num_time_slots))
                        for _ in range(self.num_classes)]
            population.append(schedule)
        return population

    def draw_schedule(self, screen, font, schedule):

        screen.fill((255, 255, 255))  # Clear screen

        cell_size = 60
        margin_left = 150
        margin_top = 100

        # Display class labels on the top (X-axis labels)
        for col in range(self.num_classes):
            class_text = font.render(f"Class {col + 1}", True, (0, 0, 0))
            screen.blit(class_text, (margin_left + col * cell_size + 5, margin_top - 30))

        # Display student labels and grid
        for row in range(self.num_students):
            student_text = font.render(f"Student {row + 1}", True, (0, 0, 0))
            screen.blit(student_text, (10, margin_top + row * cell_size + 15))

            for col in range(self.num_classes):
                assigned_student, assigned_slot = schedule[col]
                cell_rect = pygame.Rect(
                    margin_left + col * cell_size, 
                    margin_top + row * cell_size, 
                    cell_size, 
                    cell_size
                )
                if assigned_student == row:
                    # Highlight assigned slots
                    pygame.draw.rect(screen, (0, 0, 255), cell_rect)
                else:
                    # Unassigned slots
                    pygame.draw.rect(screen, (200, 200, 200), cell_rect)

                # Draw border
                pygame.draw.rect(screen, (0, 0, 0), cell_rect, 1)

                # Display priority in the cell if assigned
                if assigned_student == row:
                    priority_text = font.render(f"P{self.class_priorities[col]}", True, (0, 0, 0))
                    screen.blit(priority_text, (cell_rect.x + 5, cell_rect.y + 5))
                    priority_text = font.render(f"{self.class_durations[col]}h", True, (0, 0, 0))
                    screen.blit(priority_text, (cell_rect.x + 5, cell_rect.y + 30))

    def evaluate_schedule(self, schedule):
    
        conflict_penalty = 0
        preference_penalty = 0

        for class_id, (student_id, time_slot) in enumerate(schedule):
            if self.student_availability[student_id, time_slot] == 0:
                conflict_penalty += 1

            preference_penalty += (5 - self.student_preferences[student_id, time_slot])

        return conflict_penalty + preference_penalty
