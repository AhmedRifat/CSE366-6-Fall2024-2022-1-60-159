class Agent:
    def __init__(self, position, speed, environment):
        self.position = position
        self.speed = speed
        self.environment = environment

    def move(self, direction, agent_size, text_height):
        # As the top-left corner of the agent is (0, 0), the agent will move in the specified direction. Up means decrementing the y-axis, down means incrementing the y-axis, Left means decrementing the x-axis, and right means incrementing the x-axis with the speed. 
        if direction == "up":
            self.position[1] -= self.speed
        elif direction == "down":
            self.position[1] += self.speed
        elif direction == "left":
            self.position[0] -= self.speed
        elif direction == "right":
            self.position[0] += self.speed

        # This is for the challenge problem. If the agent goes out of the environment, it will come back to the other side. The logic is the current position of the agent's modulus value of x-axis with the width of the environment minus the agent size. Ex. screen height, width = 100, 50 and agent height, width = 10, 10. If the x-axis value = 105 so it will go outside of the border. Now, 105 % (100 - 10) = 15. The agent will come back to the left side. Same logic goes for the y-axis. The extra minus part here will be the text height.
        self.position[0] = self.position[0] % (self.environment.width - agent_size)
        self.position[1] = self.position[1] % (self.environment.height - agent_size - text_height)

        # After this send the position to the limit_position function to set position of the agent inside the environment
        self.position = self.environment.limit_position(self.position, agent_size, text_height)