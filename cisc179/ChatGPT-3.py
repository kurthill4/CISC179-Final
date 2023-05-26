# The program was generated with the following question:
# can you write a python class that runs Conways game of life?  Use Python 3.11.
# The program should open a window, and display the results for each generation.


import tkinter as tk


class GameOfLife:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid_width = width // cell_size
        self.grid_height = height // cell_size
        self.cells = [[False] * self.grid_width for _ in range(self.grid_height)]
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.root.after(0, self.update)

        # Set up initial cells
        self.cells[2][3] = True
        self.cells[3][4] = True
        self.cells[4][2] = True
        self.cells[4][3] = True
        self.cells[4][4] = True

    def update(self):
        # Compute the next generation of cells
        new_cells = [[False] * self.grid_width for _ in range(self.grid_height)]
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                neighbors = self.count_neighbors(i, j)
                if self.cells[i][j] and (neighbors == 2 or neighbors == 3):
                    new_cells[i][j] = True
                elif not self.cells[i][j] and neighbors == 3:
                    new_cells[i][j] = True

        self.cells = new_cells
        self.draw_cells()
        self.root.after(50, self.update)

    def count_neighbors(self, row, col):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor_row = (row + i + self.grid_height) % self.grid_height
                neighbor_col = (col + j + self.grid_width) % self.grid_width
                if self.cells[neighbor_row][neighbor_col]:
                    count += 1
        return count

    def draw_cells(self):
        self.canvas.delete("all")
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if self.cells[i][j]:
                    x = j * self.cell_size
                    y = i * self.cell_size
                    self.canvas.create_rectangle(
                        x,
                        y,
                        x + self.cell_size,
                        y + self.cell_size,
                        fill="black",
                        outline="white",
                    )

    def run(self):
        self.root.mainloop()


# Example usage
if __name__ == "__main__":
    game = GameOfLife(800, 600, 10)
    game.run()
