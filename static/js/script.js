let intervalId;
let intervalTime = 1000; // Default interval time in milliseconds

// Function to create the grid based on the state given
function createGrid(state) {
    const gridElement = document.getElementById('grid');
    gridElement.innerHTML = ''; // Clear the grid
    const gridSize = state.length;
    gridElement.style.gridTemplateColumns = `repeat(${gridSize}, 20px)`;
    for (let row = 0; row < gridSize; row++) {
        for (let col = 0; col < gridSize; col++) {
            const cellElement = document.createElement('div');
            cellElement.className = 'cell' + (state[row][col] === 1 ? '' : ' dead');
            cellElement.dataset.row = row;
            cellElement.dataset.col = col;
            cellElement.addEventListener('click', () => toggleCell(row, col));
            gridElement.appendChild(cellElement);
        }
    }
}

// Function to fetch the next state of the grid
async function next() {
    const response = await fetch('/next', {
        method: 'POST'
    });
    const newState = await response.json();
    createGrid(newState);
}

// Function to initialise the grid with a default state
async function initialiseGrid() {
    const gridSize = document.getElementById('grid-size').value;
    const response = await fetch('/initial_state', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ size: gridSize })
    });
    const initialState = await response.json();
    console.log('Initial state:', initialState);
    createGrid(initialState);
}

// Function to toggle play and stop of the simulation
function togglePlay() {
    const playStopButton = document.getElementById('play-stop-button');
    if (playStopButton.textContent === 'Play') {
        playStopButton.textContent = 'Stop';
        intervalId = setInterval(next, intervalTime);
    } else {
        playStopButton.textContent = 'Play';
        clearInterval(intervalId);
    }
}

// Function to update the speed of the simulation
function updateSpeed(value) {
    value = 2.25 - value;
    intervalTime = value * 1000; // Convert seconds to milliseconds
    document.getElementById('speed-value').textContent = value + 's';
    const playStopButton = document.getElementById('play-stop-button');
    if (intervalId && playStopButton.textContent === 'Stop') {
        clearInterval(intervalId);
        intervalId = setInterval(next, intervalTime);
    }
}

// Function to toggle the state of a cell
async function toggleCell(row, col) {
    const response = await fetch('/toggle_cell', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ row: row, col: col })
    });
    const newState = await response.json();
    createGrid(newState);
}

// Function to save the current grid state to a file
async function saveGrid() {
    const filename = prompt("Enter the filename to save the grid state:", "grid_state");
    if (filename) {
        const response = await fetch('/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ filename: filename })
        });
        const result = await response.json();
        alert(result.message);
    }
}

// Function to load a grid state from a file
async function loadGrid(event) {
    const file = event.target.files[0];
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/load', {
        method: 'POST',
        body: formData
    });
    const newState = await response.json();
    createGrid(newState);
}

// Initialize the grid when the document is loaded
document.addEventListener('DOMContentLoaded', () => {
    initialiseGrid();
});
