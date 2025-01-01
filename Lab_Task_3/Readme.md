# Class Scheduling Optimization using Genetic Algorithms

This project implements a **class scheduling system** using a genetic algorithm for optimization and Pygame for visualization. It assigns classes to students based on preferences, availability, and class priorities, aiming to minimize conflicts and maximize efficiency.

## 🎯 Project Overview

- **Genetic Algorithm Optimization**: Efficiently schedules classes to students by minimizing conflicts and considering student preferences.
- **Pygame Visualization**: Provides a real-time, interactive visualization of the scheduling process.
- **Dynamic Scheduling**: Assigns classes based on individual student preferences, availability, and class priorities.
## 🖼️ Preview
![Task Scheduling Visualization](preview.gif)
## 🚀 Features

### 1. Genetic Algorithm for Optimization
- **Fitness Function**: Designed to penalize schedules based on the number of conflicting classes and the inverse of student preferences.
  - **Conflict Penalty**: Increments for each class where the student is unavailable.
  - **Preference Penalty**: Adds the inverse of the student's preference for the assigned class.
- **Selection**: Retains the best-performing solutions based on fitness.
- **Crossover**: Combines parent schedules to create new offspring schedules.
- **Mutation**: Introduces random changes to offspring schedules to maintain diversity.

### 2. Pygame-Based Visualization
- **Grid Display**: Represents class assignments in a grid format.
  - **Rows**: Represent students.
  - **Columns**: Represent class slots.
- **Color-Coding**: Cells are color-coded based on slot durations and assignment status.
- **Real-Time Updates**: Displays the current generation, fitness values, and updates below the grid.

### 3. Dynamic Scheduling
- **Student Preferences**: Each student has a unique preference factor for classes.
- **Student Availability**: Randomly initialized availability for each class (1 = available, 0 = unavailable).
- **Class Priorities and Durations**: Each class has its own priority and duration.

## 🛠️ Installation

### Requirements
- Python 3.x
- Pip (Python package installer)

### Clone the Repository
```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```
### Install Dependencies
To install the necessary dependencies, run the following command:

```bash
pip install numpy pygame
```
## 🎮 Usage
Run the main script to start the scheduling visualization:

```bash
python run.py
```

---

## 📁 Project Structure

```plaintext
├── agent.py             # Defines the Agent class for students
├── environment.py       # Manages classes, preferences, availability, and grid visualization
├── run.py               # Main script running the genetic algorithm and visualization
```

### `agent.py`
Defines the Agent class representing students.

**Attributes:**
- `id`: Unique identifier for each student.
- `preference`: Preference factor of the student.
- `slots`: List of slots (classes) assigned to the student.

**Methods:**
- `assign_class()`: Assigns a class to the student.
- `total_time()`: Calculates total time required to complete all classes.
- `reset_classes()`: Clears assigned classes.

---

### `environment.py`
Manages the scheduling environment and visualization.

**Attributes:**
- `num_classes`: Number of classes.
- `num_students`: Number of students.
- `slot_durations`: Durations for each class slot.
- `class_priorities`: Priority levels for each class.
- `student_preferences`: Preference factors for each student.
- `student_class_preferences`: Preference matrix of students for classes.
- `student_availability`: Availability matrix (0 or 1) of students for classes.

**Methods:**
- `generate_assignments()`: Generates initial class assignments.
- `draw_grid()`: Visualizes the class assignments using Pygame.

---

### `run.py`
Main script executing the genetic algorithm and visualization.

**Initializes:**
- Pygame window.
- Environment and agents.

**Genetic Algorithm:**
- **Fitness Function**: Calculates penalties based on conflicts and preferences.
- **Selection**: Selects top individuals based on fitness.
- **Crossover**: Combines parents to produce offspring.
- **Mutation**: Introduces random mutations.

**Visualization:**
- Shows grid of class assignments.
- Displays generation and fitness information.
- Updates list of recent changes.

---
**Genetic Algorithm:**
- **Fitness Function**: Calculates penalties based on conflicts and preferences.
  ```python
  def fitness(individual):
      conflict_penalty = 0
      preference_penalty = 0.0

      for class_index, student_index in enumerate(individual):
          # Conflict Penalty
          if environment.student_availability[student_index, class_index] == 0:
              conflict_penalty += 1

          # Preference Penalty
          preference = environment.student_class_preferences[student_index, class_index]
          if preference == 0:
              preference_penalty += 1.0  # Maximum penalty
          else:
              preference_penalty += 1.0 / preference  # Inverse preference

      total_fitness = conflict_penalty + preference_penalty
      return total_fitness
  ```
  - **Conflict Penalty**: Counts the number of classes where the assigned student is unavailable.
  - **Preference Penalty**: Sum of the inverse of student preferences for the assigned classes.
- **Selection**: Selects top individuals based on fitness.
- **Crossover**: Combines parents to produce offspring.
- **Mutation**: Introduces random mutations.

**Genetic Algorithm Parameters:**
- **Population Size**: 50
- **Mutation Rate**: 0.1
- **Number of Generations**: 100
- **Generation Delay**: 500 milliseconds (for visualization).

**Visualization:**
- Shows grid of class assignments.
- Displays generation and fitness information.
- Updates list of recent changes.

---

## ⚙️ Genetic Algorithm Details

### 📊 Visualization Details

**Grid Layout:**
- **Columns**: Represent class slots.
- **Rows**: Represent students.

**Cell Details:**
- **Color**: Indicates whether the class is assigned to the student and the duration.
- **Annotations**: Show class priority and duration.

**Sidebar Information:**
- Current generation.
- Current fitness of the best individual.
- Best fitness found so far.

**Updates List:**
- Displays recent updates and fitness values below the grid.

### Controls
- **Exit**: Close the Pygame window to exit the program.

---

## ⚠️ Important Notes

- **Student Availability**: Randomly initialized in `environment.py` using 0/1, where:
  - `1 = Available`
  - `0 = Unavailable`
- **Student Preferences**: Each student has a preference factor influencing their satisfaction with a class assignment.
- **Class Priorities**: Classes have priorities that can affect scheduling decisions.

---

## 🔄 Customization

You can modify the scheduling parameters in `run.py`:

```python
# Environment setup
num_classes = 10      # Number of classes
num_students = 5      # Number of students

# Genetic Algorithm parameters
population_size = 50  # Size of the population
mutation_rate = 0.1   # Mutation rate
n_generations = 100   # Number of generations to run
generation_delay = 500  # Delay between generations in milliseconds
```

