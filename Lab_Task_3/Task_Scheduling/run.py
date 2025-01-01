import pygame
from agent import Agent
from environment import Environment
import numpy as np
import random

# Initialize Pygame
pygame.init()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600  # Increased height to accommodate updates below the grid
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Class Scheduling Visualization")
font = pygame.font.Font(None, 24)

# Environment setup
num_classes = 10
num_students = 5
environment = Environment(num_classes, num_students)
task_assignments = environment.generate_assignments()

# Initialize agents
agents = [Agent(id=i, preference=environment.student_preferences[i]) for i in range(num_students)]

# Genetic Algorithm parameters
population_size = 50
mutation_rate = 0.1
n_generations = 100
generation_delay = 500  # Delay (milliseconds) between each generation for visualization

# Updates list to display below the grid
updates = []
max_updates = 5  # Max number of updates to display at once

def fitness(individual):
    conflict_penalty = 0
    preference_penalty = 0.0

    for class_index, student_index in enumerate(individual):
        # Check for conflicts (student is unavailable for the class time slot)
        if environment.student_availability[student_index, class_index] == 0:
            conflict_penalty += 1  # Increment conflict penalty

        # Compute preference penalty
        preference = environment.student_class_preferences[student_index, class_index]
        if preference == 0:
            # If no preference, apply maximum penalty (adjust value as needed)
            preference_penalty += 1.0
        else:
            # Apply penalty inversely proportional to the student's preference
            preference_penalty += 1.0 / preference
        

    # Total fitness is the sum of conflict and preference penalties
    total_fitness = conflict_penalty + preference_penalty
    # print(f"{total_fitness}")
    return total_fitness

def selection(population):
    return sorted(population, key=fitness)[:population_size // 2]

def crossover(parent1, parent2):
    point = random.randint(1, num_classes - 1)
    return np.concatenate([parent1[:point], parent2[point:]])

def mutate(individual):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = random.randint(0, num_students - 1)
    return individual

# Initialize population
population = environment.generate_assignments()

# Visualization loop
running = True
best_solution = None
best_fitness = float('inf')
generation_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Genetic Algorithm step-by-step per generation
    selected = selection(population)
    next_generation = []
    while len(next_generation) < population_size:
        parent1, parent2 = random.sample(selected, 2)
        child = crossover(parent1, parent2)
        next_generation.append(mutate(child))
    
    # Update population with next generation
    population = next_generation

    # Find the best solution in the current generation
    current_best = min(population, key=fitness)
    current_fitness = fitness(current_best)
    if current_fitness < best_fitness:
        best_fitness = current_fitness
        best_solution = current_best

    # Draw current generation's best solution on the grid
    environment.draw_grid(screen, font, current_best)

    # Display generation and fitness info on the right panel
    generation_text = font.render(f"Generation: {generation_count + 1}", True, (0, 0, 0))
    fitness_text = font.render(f"Current Fitness: {current_fitness:.2f}", True, (0, 0, 0))
    best_fitness_text = font.render(f"Best Fitness: {best_fitness:.2f}", True, (0, 0, 0))
    screen.blit(generation_text, (SCREEN_WIDTH - 200, 50))
    screen.blit(fitness_text, (SCREEN_WIDTH - 200, 80))
    screen.blit(best_fitness_text, (SCREEN_WIDTH - 200, 110))

    # Add update for the current generation to the updates list
    update_text = f"Generation {generation_count + 1}: Total Fitness = {current_fitness:.2f}"
    updates.append(update_text)
    if len(updates) > max_updates:
        updates.pop(0)  # Remove the oldest update if we exceed the display limit

    # Display the list of updates below the grid
    update_start_y = 450 # Starting Y position below the grid
    for i, update in enumerate(updates):
        update_surface = font.render(update, True, (0, 0, 0))
        screen.blit(update_surface, (50, update_start_y + i * 25))

    pygame.display.flip()
    pygame.time.delay(generation_delay)

    generation_count += 1
    if generation_count >= n_generations:
        break

# Keep window open after completion
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()


