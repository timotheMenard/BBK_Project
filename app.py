import os
from flask import Flask, jsonify, render_template, request, send_file
from cell import Cell
from grid import Grid

# Initialize Flask application
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads' # Folder to save and load grid states
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

n = 5 # Default grid size
grid = None

# Function to initialise the grid with a checkerboard pattern
def initialise_grid(sizestr):
    size = int(sizestr)
    global grid
    initial_state = [[1 if (i + j) % 2 == 0 else 0 for j in range(size)] for i in range(size)]
    grid = Grid(size, size, initial_state)
    return initial_state

# Route to serve the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to get the initial state of the grid
@app.route('/initial_state', methods=['POST'])
def get_initial_state():
    size = request.json.get('size', n)
    initial_state = initialise_grid(size)
    return jsonify(initial_state)

# Route to get the next state of the grid
@app.route('/next', methods=['POST'])
def next_step():
    grid.update()
    new_state = [[cell.cell_type for cell in row] for row in grid.cells]
    return jsonify(new_state)

# Route to toggle the state of a specific cell
@app.route('/toggle_cell', methods=['POST'])
def toggle_cell():
    row = request.json['row']
    col = request.json['col']
    current_type = grid.cells[row][col].cell_type
    grid.cells[row][col].cell_type = 1 - current_type
    new_state = [[cell.cell_type for cell in row] for row in grid.cells]
    return jsonify(new_state)

# Route to save the current grid state to a file
@app.route('/save', methods=['POST'])
def save_grid():
    data = request.json
    filename = data.get('filename', 'grid_state.txt')
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename+".txt")
    
    with open(filepath, 'w') as f:
        f.write(f"{grid.width} {grid.height} ")
        for row in grid.cells:
            f.write("".join(str(cell.cell_type) for cell in row))
    
    return jsonify({"message": "Grid saved successfully", "filename": filename+".txt"})

# Route to load a grid state from a file
@app.route('/load', methods=['POST'])
def load_grid():
    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)
    
    with open(file_path, 'r') as f:
        content = f.read().strip()
    
    parts = content.split()
    width, height = int(parts[0]), int(parts[1])
    grid_data = parts[2]
    
    initial_state = []
    index = 0
    for _ in range(height):
        row = [int(grid_data[index + col]) for col in range(width)]
        initial_state.append(row)
        index += width
    
    global grid
    grid = Grid(width, height, initial_state)
    new_state = [[cell.cell_type for cell in row] for row in grid.cells]
    return jsonify(new_state)

# Run the application
if __name__ == '__main__':
    app.run()
