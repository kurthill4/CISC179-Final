import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class GameOfLife:
    def __init__(self, size):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self.fig, self.ax = plt.subplots()
        self.image = self.ax.imshow(self.grid, cmap='binary')
        self.animation = None

    def randomize(self, density=0.2):
        self.grid = np.random.choice([0, 1], size=(self.size, self.size), p=[1 - density, density])
        self.update_plot()

    def set_pattern(self, pattern, position=(0, 0)):
        pattern = np.array(pattern)
        pattern_size = pattern.shape
        if position[0] + pattern_size[0] <= self.size and position[1] + pattern_size[1] <= self.size:
            self.grid[position[0]:position[0] + pattern_size[0], position[1]:position[1] + pattern_size[1]] = pattern
        else:
            raise ValueError("Pattern size exceeds grid bounds.")
        self.update_plot()

    def update_plot(self):
        self.image.set_data(self.grid)
        self.ax.axis('off')

    def count_neighbors(self, x, y):
        top = max(0, x - 1)
        bottom = min(self.size - 1, x + 1)
        left = max(0, y - 1)
        right = min(self.size - 1, y + 1)

        return np.sum(self.grid[top:bottom + 1, left:right + 1]) - self.grid[x, y]

    def update_generation(self, _):
        new_grid = np.copy(self.grid)

        for i in range(self.size):
            for j in range(self.size):
                neighbors = self.count_neighbors(i, j)

                if self.grid[i, j] == 1:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[i, j] = 0
                else:
                    if neighbors == 3:
                        new_grid[i, j] = 1

        self.grid = new_grid
        self.update_plot()

    def start_animation(self):
        self.animation = animation.FuncAnimation(self.fig, self.update_generation, interval=200, blit=False, cache_frame_data=False)
        plt.show(block=True)

# Create an instance of the GameOfLife class
game = GameOfLife(size=50)

# Randomize the grid with a given density of live cells
game.randomize(density=0.2)

# Set a specific pattern at a particular position
pattern = [[0, 1, 0],
           [0, 0, 1],
           [1, 1, 1]]
game.set_pattern(pattern, position=(10, 10))

# Start the animation to observe the game
game.start_animation()
