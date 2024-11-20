import pygame
import sys
from agent import Agent
from environment import Environment

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
GRID_SIZE = 40
STATUS_WIDTH = 600
BACKGROUND_COLOR = (255, 255, 255)
BARRIER_COLOR = (0, 0, 0)       # Barrier color is black
TASK_COLOR = (255, 0, 0)        # Task color is red
COMPLETED_TASK_COLOR = (0, 255, 0)  # Completed task color is green
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)
MOVEMENT_DELAY = 200  # Milliseconds between movements

def main():
    pygame.init()

    # Set up display with an additional status panel
    screen = pygame.display.set_mode((WINDOW_WIDTH + STATUS_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame AI Grid Simulation")

    # Clock to control frame rate
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Initialize environment and agent
    environment = Environment(WINDOW_WIDTH, WINDOW_HEIGHT, GRID_SIZE, num_tasks=5, num_barriers=15)
    agent = Agent(environment, GRID_SIZE)
    
    all_sprites = pygame.sprite.Group()
    all_sprites.add(agent)



    # Start button positioned on the right side (status panel)
    button_width, button_height = 100, 50

    # A* button
    button_Astar_x = WINDOW_WIDTH + 100
    button_Astar_y = 400
    button_Astar_rect = pygame.Rect(button_Astar_x, button_Astar_y, button_width, button_height)
    simulation1_started = False
    

    # UCS button
    button_UCS_x = WINDOW_WIDTH + 300
    button_UCS_y = 400
    button_UCS_rect = pygame.Rect(button_UCS_x, button_UCS_y, button_width, button_height)
    simulation2_started = False

    # Variables for movement delay
    last_move_time_Astar = pygame.time.get_ticks()
    last_move_time_UCS = pygame.time.get_ticks()

    # Track costs

    total_cost_Astar = 0
    total_cost_UCS = 0
    agent_path = []

    # Main loop
    running = True
    while running:
        clock.tick(60)  # Limit to 60 FPS

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # When A* button triggers
            if not simulation1_started and event.type == pygame.MOUSEBUTTONDOWN:
                if button_Astar_rect.collidepoint(event.pos):
                    simulation1_started = True
                    # Start moving towards the nearest task (A*)
                    if environment.task_locations_Astar:
                        agent_path = agent.find_nearest_task_Astar()
            # When UCS button triggers
            if not simulation2_started and event.type == pygame.MOUSEBUTTONDOWN:
                if button_UCS_rect.collidepoint(event.pos):
                    simulation2_started = True
                    # Start moving towards the nearest task (UCS)
                    if environment.task_locations_UCS:
                        agent_path = agent.find_nearest_task_UCS()

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw grid
        for x in range(environment.columns):
            for y in range(environment.rows):
                rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, (200, 200, 200), rect, 1)  # Draw grid lines

        # Draw barriers
        for (bx, by) in environment.barrier_locations:
            barrier_rect = pygame.Rect(bx * GRID_SIZE, by * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BARRIER_COLOR, barrier_rect)

        # Agent's optimal path using A*
        agent_path = agent.path_Astar
        if agent_path:  # Ensure agent_path is not None
            for px, py in agent_path:
                path_rect = pygame.Rect(px * GRID_SIZE, py * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, COMPLETED_TASK_COLOR, path_rect, 3)

        # Agent's optimal path using UCS
        agent_path = agent.path_UCS
        if agent_path:  # Ensure agent_path is not None
            for px, py in agent_path:
                path_rect = pygame.Rect(px * GRID_SIZE, py * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pygame.draw.rect(screen, (255, 165, 0), path_rect, 3)


        # Draw tasks with numbers for A*
        for (tx, ty), task_number in environment.task_locations_Astar.items():
            if (task_number, (tx, ty)) in agent.completed_tasks_Astar:
                task_color = (0, 255, 0)  # Green for completed tasks
            else:
                task_color = TASK_COLOR
            task_rect = pygame.Rect(tx * GRID_SIZE, ty * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, task_color, task_rect)
            # Draw task number
            task_num_surface = font.render(str(task_number), True, (255, 255, 255))
            task_num_rect = task_num_surface.get_rect(center=task_rect.center)
            screen.blit(task_num_surface, task_num_rect)

        # Draw tasks with numbers for UCS
        for (tx, ty), task_number in environment.task_locations_UCS.items():
            if (task_number, (tx, ty)) in agent.completed_tasks_UCS:
                task_color = (0, 255, 0)  # Green for completed tasks
            else:
                task_color = TASK_COLOR
            task_rect = pygame.Rect(int(tx) * GRID_SIZE, int(ty) * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, task_color, task_rect)
            # Draw task number
            task_num_surface = font.render(str(task_number), True, (255, 255, 255))
            task_num_rect = task_num_surface.get_rect(center=task_rect.center)
            screen.blit(task_num_surface, task_num_rect)
        
        # Draw agent
        all_sprites.draw(screen)

        # A* Status Bar creation
        status_x_Astar = WINDOW_WIDTH + 30
        task_status_text_Astar = f"Tasks Completed: {agent.task_completed_Astar}"
        position_text_Astar = f"Position: {agent.position_Astar}"
        completed_tasks_text_Astar = f"Completed Tasks: {', '.join(map(str, agent.completed_tasks_Astar))}"
        total_cost_text_Astar = f"Total Path Cost: {agent.total_cost_Astar}"
        status_surface_Astar = font.render(task_status_text_Astar, True, TEXT_COLOR)
        position_surface_Astar = font.render(position_text_Astar, True, TEXT_COLOR)
        completed_tasks_surface_Astar = font.render(completed_tasks_text_Astar, True, TEXT_COLOR)
        total_cost_surface_Astar = font.render(total_cost_text_Astar, True, TEXT_COLOR)

        screen.blit(font.render("A* Details:", True, TEXT_COLOR), (status_x_Astar, 10))
        screen.blit(status_surface_Astar, (status_x_Astar, 40))
        screen.blit(position_surface_Astar, (status_x_Astar, 70))
        screen.blit(completed_tasks_surface_Astar, (status_x_Astar, 100))
        screen.blit(total_cost_surface_Astar, (status_x_Astar, 130))

        # UCS Status Bar creation
        status_x_UCS = WINDOW_WIDTH + 30
        task_status_text_UCS = f"Tasks Completed: {agent.task_completed_UCS}"
        position_text_UCS = f"Position: {agent.position_UCS}"
        completed_tasks_text_UCS = f"Completed Tasks: {', '.join(map(str, agent.completed_tasks_UCS))}"
        total_cost_text_UCS = f"Total Path Cost: {agent.total_cost_UCS}"
        status_surface_UCS = font.render(task_status_text_UCS, True, TEXT_COLOR)
        position_surface_UCS = font.render(position_text_UCS, True, TEXT_COLOR)
        completed_tasks_surface_UCS = font.render(completed_tasks_text_UCS, True, TEXT_COLOR)
        total_cost_surface_UCS = font.render(total_cost_text_UCS, True, TEXT_COLOR)

        screen.blit(font.render("UCS Details:", True, TEXT_COLOR), (status_x_UCS, 220))
        screen.blit(status_surface_UCS, (status_x_UCS, 250))
        screen.blit(position_surface_UCS, (status_x_UCS, 280))
        screen.blit(completed_tasks_surface_UCS, (status_x_UCS, 310))
        screen.blit(total_cost_surface_UCS, (status_x_UCS, 340))

        # UCS Search button creation
        mouse_pos_UCS = pygame.mouse.get_pos()
        if button_UCS_rect.collidepoint(mouse_pos_UCS):
               button_color = BUTTON_HOVER_COLOR
        else:
           button_color = BUTTON_COLOR
        pygame.draw.rect(screen, button_color, button_UCS_rect)
        button_text_UCS = font.render("UCS Search", True, BUTTON_TEXT_COLOR)
        text_rect = button_text_UCS.get_rect(center=button_UCS_rect.center)
        screen.blit(button_text_UCS, text_rect)

        # A* Search button creation
        mouse_pos_Astar = pygame.mouse.get_pos()
        if button_Astar_rect.collidepoint(mouse_pos_Astar):
               button_color = BUTTON_HOVER_COLOR
        else:
           button_color = BUTTON_COLOR
        pygame.draw.rect(screen, button_color, button_Astar_rect)
        button_text_Astar = font.render("A* Search", True, BUTTON_TEXT_COLOR)
        text_rect = button_text_Astar.get_rect(center=button_Astar_rect.center)
        screen.blit(button_text_Astar, text_rect)

        cost = 0
        # Simulation for A* Search
        if simulation1_started:
            # Automatic movement with delay
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time_Astar > MOVEMENT_DELAY:
                if not agent.moving_Astar and environment.task_locations_Astar:
                    # Find the nearest task
                    agent_path = agent.find_nearest_task_Astar()
                elif agent.moving_Astar:
                    cost = agent.move_Astar()
                    if cost:  # Update the cost if a task is completed
                        total_cost_Astar += cost

                    if agent_path and agent.position_Astar == agent_path[0]:
                        agent_path.pop(0)
                last_move_time_Astar = current_time

        # Simulation for UCS Search
        cost = 0
        if simulation2_started:
            # Automatic movement with delay
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time_UCS > MOVEMENT_DELAY:
                if not agent.moving_UCS and environment.task_locations_UCS:
                    # Find the nearest task
                    agent_path = agent.find_nearest_task_UCS()
                elif agent.moving_UCS:
                    cost = agent.move_UCS()
                    if cost:  # Update the cost if a task is completed
                        total_cost_UCS += cost

                    if agent_path and agent.position_UCS == agent_path[0]:
                        agent_path.pop(0)
                last_move_time_UCS = current_time

        # Draw the status panel separator
        pygame.draw.line(screen, (0, 0, 0), (WINDOW_WIDTH, 0), (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Update the display
        pygame.display.flip()

    # Quit Pygame properly
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
