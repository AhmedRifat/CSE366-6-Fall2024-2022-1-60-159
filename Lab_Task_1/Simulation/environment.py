class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def limit_position(self, position, agent_size, text_height):
        x, y = position
        # x and y are the coordinates of the agent that are bound to the environment's width and height
        x = max(0, min(x, self.width - 1))
        y = max(0, min(y, self.height - 1))
        
        return [x, y]