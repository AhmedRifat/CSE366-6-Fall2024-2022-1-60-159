# Task Scheduling Visualization and Optimization

This project implements a **task scheduling system** using a **genetic algorithm** for optimization and **Pygame** for visualization. It assigns classes to students based on preferences, availability, and class priorities, aiming to minimize conflicts and maximize efficiency.

---

## Features

### 1. **Genetic Algorithm for Optimization**
- **Selection**: Chooses the top-performing solutions for reproduction.
- **Crossover**: Combines parents to create new solutions.
- **Mutation**: Introduces random changes to maintain diversity.
- **Fitness Function**: Penalizes conflicts and low-preference assignments.

### 2. **Pygame-Based Visualization**
- Grid-based visualization of task assignments.
- Color-coded cells represent task durations.
- Real-time updates of generations and fitness values.

### 3. **Dynamic Scheduling**
- Each student is assigned classes based on:
  - **Preferences**: How much they prefer specific classes.
  - **Availability**: Whether they are available for a class time slot.
  - **Class Priorities**: Importance of the class.

---

## Project Structure

```plaintext
├── agent.py             # Defines the Agent class for students.
├── environment.py       # Manages classes, preferences, and grid visualization.
├── run.py               # Main script running the genetic algorithm and visualization.
└── README.md            # Project documentation.
