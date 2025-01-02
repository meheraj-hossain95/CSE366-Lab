import pygame
import random
from environment import Environment
from agent import Student


pygame.init()
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Class Scheduling Visualization")
font = pygame.font.Font(None, 24)


NUM_CLASSES = 10
NUM_STUDENTS = 5
NUM_TIME_SLOTS = 8
POPULATION_SIZE = 50
MUTATION_RATE = 0.1
NUM_GENERATIONS = 100
GENERATION_DELAY = 1000  # milliseconds

# Initialize Environment
environment = Environment(NUM_CLASSES, NUM_STUDENTS, NUM_TIME_SLOTS)
students = [Student(student_id=i, 
                    availability=environment.student_availability[i], 
                    preferences=environment.student_preferences[i]) 
            for i in range(NUM_STUDENTS)]


def fitness(schedule):
    total_fitness = 0
    for student_id, student in enumerate(students):
        student.clear_schedule()
        for class_id, (assigned_student, time_slot) in enumerate(schedule):
            if assigned_student == student_id:
                student.assign_class(class_id, time_slot)
        total_fitness += student.calculate_fitness(environment.class_priorities) 
    return total_fitness

def selection(population):
    return sorted(population, key=fitness)[:POPULATION_SIZE // 2]

def crossover(parent1, parent2):
    point = random.randint(1, NUM_CLASSES - 1)
    return parent1[:point] + parent2[point:]

def mutate(schedule):
    for i in range(len(schedule)):
        if random.random() < MUTATION_RATE:
            schedule[i] = (random.randint(0, NUM_STUDENTS - 1), random.randint(0, NUM_TIME_SLOTS - 1))
    return schedule

# Initialize Population
population = environment.generate_initial_population(POPULATION_SIZE)

# Visualization Loop
running = True
best_schedule = None
best_fitness = float('inf')
generation_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Genetic Algorithm Step
    selected = selection(population)
    next_generation = []
    while len(next_generation) < POPULATION_SIZE:
        parent1, parent2 = random.sample(selected, 2)
        child = crossover(parent1, parent2)
        next_generation.append(mutate(child))

    population = next_generation

    # Evaluate Best Schedule
    
    current_best = min(population, key=fitness)
    current_fitness = fitness(current_best)
    #max_fit = (-1, current_fitness)
    if current_fitness < best_fitness:
        best_fitness = current_fitness
        best_schedule = current_best

    # Visualization
    environment.draw_schedule(screen, font, best_schedule)

    # Display Fitness and Generation Info
    generation_text = font.render(f"Generation: {generation_count + 1}", True, (0, 0, 0))
    fitness_text = font.render(f"Best Fitness: {best_fitness:.2f}", True, (0, 0, 0))
    #max_fit_text = font.render(f"Max Fitness Achievend: {max_fit:.2f}", True, (0, 0, 0))
    screen.blit(generation_text, (SCREEN_WIDTH - 250, 50))
    screen.blit(fitness_text, (SCREEN_WIDTH - 250, 80))
    #screen.blit(max_fit_text, (SCREEN_WIDTH - 250, 110))

    pygame.display.flip()
    pygame.time.delay(GENERATION_DELAY)

    generation_count += 1
    if generation_count >= NUM_GENERATIONS:
        break


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
