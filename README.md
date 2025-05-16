# Flood Alternative Path Finder AI

This project is a Python Flask web application that helps users find alternative paths to avoid flood or accident disaster areas while traveling.

## Features

- Displays a map with simulated flood/accident areas marked in red.
- Allows users to input start and end locations (latitude and longitude).
- Uses a simple grid graph and pathfinding algorithm to find a safe route avoiding disaster areas.
- Visualizes the alternative path on the map.

## Requirements

- Python 3.7+
- Flask
- folium
- networkx
- shapely

## Installation

1. Clone the repository or download the project files.
2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```
4. Install the required packages:
   ```
   pip install flask folium networkx shapely
   ```

## Running the Application

Run the Flask app:

```
python app.py
```

Open your browser and go to:

```
http://127.0.0.1:5000/
```

## Usage

- Enter the start and end latitude and longitude coordinates.
- Click "Find Alternative Path".
- The map will display the alternative path avoiding disaster areas.

## Notes

- Disaster areas are simulated as polygons in the code.
- The pathfinding uses a simple grid graph and may not reflect real-world roads.
- This is a demonstration project and can be extended with real map data and advanced AI models.

## License

MIT License
