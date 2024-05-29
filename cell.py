class Cell:
    def __init__(self, cell_type, update_method=None):
        self.cell_type = cell_type
        self.update_method = update_method if update_method is not None else self.update_default

    # Default update method for the cell based on its neighbours
    def update_default(self, neighbours):
        live_neighbours = sum(1 for n in neighbours if n.cell_type == 1)

        # Default update method for the cell based on its neighbours
        if self.cell_type == 1:
            if live_neighbours < 2 or live_neighbours > 3:
                self.cell_type = 0
        elif self.cell_type == 0:
            if live_neighbours == 3:
                self.cell_type = 1

    # Update the cell state using the assigned update method
    def update(self, neighbours):
        self.update_method(neighbours)

    def __str__(self):
        return str(self.cell_type)

    def __repr__(self):
        return f"Cell({self.cell_type})"
