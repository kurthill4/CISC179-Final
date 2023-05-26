# This code was modified from the previous code (#4) by asking a follow-up question:
#

import tkinter as tk
import numpy as np

class GameOfLife:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((width, height), dtype=bool)
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=width, height=height)
        self.canvas.pack()
        self.running = False

        self.window.bind('<Button-1>', self.handle_click)
        self.window.bind('<space>', self.toggle_running)
        self.window.bind('<Return>', self.step)

    def handle_click(self, event):
        x = int(event.x)
        y = int(event.y)
        self.grid[x, y] = not self.grid[x, y]
        self.draw_cell(x, y)

    def toggle_running(self, event):
        self.running = not self.running
        if self.running:
            self.run()

    def step(self, event):
        if not self.running:
            self.update_grid()
            self.draw_grid()

    def run(self):
        if self.running:
            self.update_grid()
            self.draw_grid()
            self.window.after(100, self.run)

    def update_grid(self):
        next_grid = np.zeros_like(self.grid)
        for x in range(self.width):
            for y in range(self.height):
                live_neighbors = np.sum(self.grid[max(0, x-1):min(x+2, self.width), max(0, y-1):min(y+2, self.height)]) - self.grid[x, y]
                if self.grid[x, y]:
                    next_grid[x, y] = live_neighbors in (2, 3)
                else:
                    next_grid[x, y] = live_neighbors == 3
        self.grid = next_grid

    def draw_grid(self):
        self.canvas.delete('all')
        for x in range(self.width):
            for y in range(self.height):
                if self.grid[x, y]:
                    self.draw_cell(x, y)

    def draw_cell(self, x, y):
        self.canvas.create_rectangle(x, y, x+1, y+1, fill='black')

    def populate_grid(self, density):
        num_cells = int(self.width * self.height * density)
        indices = np.random.choice(self.width * self.height, num_cells, replace=False)
        for idx in indices:
            x, y = np.unravel_index(idx, (self.width, self.height))
            self.grid[x, y] = True
            self.draw_cell(x, y)

    def start(self):
        self.window.mainloop()


# Example usage
if __name__ == '__main__':
    game = GameOfLife(100, 100)  # Specify the width and height of the grid
    game.populate_grid(0.2)  # Specify the density of cells (e.g., 20% of the grid)
    game.start()
