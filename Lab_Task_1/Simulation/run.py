import pygame
from agent import Agent
from environment import Environment

pygame.init()

# Total height and width of the screen
WIDTH = 800
HEIGHT = 600

# Colors
BACKGROUND_COLOR = (186, 238, 255)
AGENT_COLOR = (8, 101, 189) 
TEXT_COLOR = (0, 0, 0)

# Agent size, speed and text height
AGENT_SIZE = 30
AGENT_SPEED = 1
TEXT_HEIGHT = 40

# Environment and Agent type objects
#env object will store the width and height of the environment
env = Environment(WIDTH, HEIGHT)
#agent object will store the position of the agent, the speed of the agent and the Environment class object. Initialized the position of the agent is [WIDTH // 4, HEIGHT // 4]
agent = Agent([WIDTH // 4, HEIGHT // 4], AGENT_SPEED, env)

# Setting up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Title of the window
pygame.display.set_caption("Pygame Based Agent-Environment Simulation")

# Setting up the font size
font = pygame.font.Font(None, 25)

# Clock object is used to control the frame rate(updates the frame per second)
clock = pygame.time.Clock()
FPS = 60

running = True
while running:
    # Event loop. It will run until the user closes the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 'keys' stores the pressed keys. In each key press, the speed of the agent will increase by 0.1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        # The move function of agent object will move the agent in the specified direction. It takes the direction, the size of the agent and the height of the text to be calculated properly.
        agent.move("up", AGENT_SIZE, TEXT_HEIGHT)
        agent.speed += 0.1
    elif keys[pygame.K_DOWN]:
        agent.move("down", AGENT_SIZE, TEXT_HEIGHT)
        agent.speed += 0.1
    elif keys[pygame.K_LEFT]:
        agent.move("left", AGENT_SIZE, TEXT_HEIGHT)
        agent.speed += 0.1
    elif keys[pygame.K_RIGHT]:
        agent.move("right", AGENT_SIZE, TEXT_HEIGHT)
        agent.speed += 0.1     

    # Fill the screen with the background color so that the background is always visible, to ignore the trail of the agent
    screen.fill(BACKGROUND_COLOR)

    # Rendering the text that will be displayed. Here in positin=on_text, the position of the text will be seen on the screen 20 height above the agents actual position because we have set the text height to 40. As the top-left corner of the agent is (0, 0), but the top section is booked for the text, that's why we are subtracting 20 to view the agent position as (0, 0) when the actual position of the agent is (0, 20).
    position_text = font.render(f"Position: ({int(agent.position[0])}, {int(agent.position[1])})", True, TEXT_COLOR)
    speed_text = font.render(f"Speed: {agent.speed:.1f}", True, TEXT_COLOR)
    
    # Blit the text on the screen. It takes the text object and the position (x and y coordinates) of the text that will be displayed
    screen.blit(position_text, (10, 10))
    screen.blit(speed_text, (660, 10))

    # Drawing the line to differentiate the blit objects and the agents movement
    pygame.draw.line(screen, TEXT_COLOR, (0, 40), (800, 40))
    # Drawing the agent by using rectangle. It takes the main screen, the color of the agent, and the position and size of the agent
    # The y-axis position of the agent is added with the text height to calculate the actual position of the agent and do operations accordingly. Because of the same reason as mentioned above. For calculation purpose the actual position of the agent is unchanged. Just for the displaying purpose, y axis is tempered.
    pygame.draw.rect(screen, AGENT_COLOR, (agent.position[0], agent.position[1] + TEXT_HEIGHT, AGENT_SIZE, AGENT_SIZE))

    # Updating the screen so that the changes are visible. Without this, the changes will not be visible on the screen
    pygame.display.update()

    # clock tick limits the frame rate per second
    clock.tick(FPS)

#exiting the pygame
pygame.quit()