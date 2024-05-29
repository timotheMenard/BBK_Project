from cell import Cell
import copy

class Grid:
    def __init__(self, width, height, initial_state):
        self.width = width
        self.height = height
        # Initialize grid cells with the initial state
        self.cells = [[Cell(initial_state[row][col]) for col in range(width)] for row in range(height)]

    # Get neighbours of a cell at (row, col)
    def get_neighbours(self, row, col):
        neighbours = []
        for i in range(max(0, row-1), min(self.height, row+2)):
            for j in range(max(0, col-1), min(self.width, col+2)):
                if (i, j) != (row, col):
                    neighbours.append(self.cells[i][j])
        return neighbours

    # Update the grid to the next state
    def update(self):
        # Create a new grid for the updated state
        new_cells = [[Cell(self.cells[row][col].cell_type) for col in range(self.width)] for row in range(self.height)]
        
        for row in range(self.height):
            for col in range(self.width):
                neighbours = self.get_neighbours(row, col)
                new_cells[row][col].update(neighbours)
        
        # Update the grid cells
        self.cells = new_cells

    # Display the grid in the console (for debugging)
    def display(self):
        for row in self.cells:
            print(" ".join(str(cell) for cell in row))
