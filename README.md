# Boid-Simulation
<hr>

### *Peter Vanderhyde*
<br>

## Description
This is a python/pygame project that simulates boids. It allows for a fairly large number of boids at decent speeds due to a quad tree being used for boid interaction. The simulation includes a sidebar where different settings can be altered in real time.
  
![boids](https://github.com/Peter-Vanderhyde/Boid-Simulation/assets/71889138/3221fe1f-8346-48eb-9493-ba10708dbfce)

## Requirements
- **Python**
- **Pygame**

Pygame can be installed after Python is installed by opening the terminal and typing:
``` cmd
pip install pygame
```

## Running
To start the project, run the ***main.py*** python file.

## Usage
- TAB - Toggles the visibility of the vision radius and separation distance
  * Green = The vision radius
  * Red = The separation radius
- G - Displays all of the quadrants of the quad tree
- Z - Creates a new NoGoZone
  * Boids will avoid flying inside of these zones
  * Move your mouse to move the zone around
  * Scroll up or down to change the size of the zone
  * Click to place to zone in a location
  * Press Z again before placing the zone to cancel the zone creation
- Ctrl+Z - Toggles the visibility of the zone outlines
- Delete - Deletes all placed zones

## Sidebar Settings
The sidebar contains several settings that can be adjusted in real time to see the affects.

### Boids
* Changes the number of boids being simulated.

### View Distance
* Changes the distance of the boid's vision so it can see boids around it from a closer or farther distance.

### Separation Distance
* Changes the distance that the boid will maintain from other boids around it.

### Minimum Speed
* Sets what the slowest possible speed that the boid can travel will be.

### Maximum Speed
* Sets what the fastest possible speed that the boid can travel will be.

### Centering Factor
* Sets how hard the boid will try to stay in the center of the boids around it. Setting this value to a large number results in boids forming into densely packed groups and not spreading out.

### Matching Factor
* Determines how hard the boid will try to point in the same average direction that its neighbors are. A high value will result in groups that move in very straight lines and turn in sync.

### Avoid Factor
* Influences how hard the boids will try to stay out of the separation bubble of other boids determined by their separation distance setting.

### Avoid Zone Factor
* Determines how hard the boids will stay out of the No Go Zones. Maxed out, it will pretty much look like boids are bouncing off of it.

### Turn Factor
* Tells the boids how hard to turn around when they travel outside the border.

### Boid Size
* Changes the visual size of the boids.

### Min Per Node
* This is a setting for the quad tree used for boid visualization. It sets the minimum number of boids that can exist within a node/quadrant. Anything less than the set number causes the neighboring nodes to combine into one bigger node.

### Max Per Node
* Tells the quad tree what the maximum number of boids that can exist within a node/quadrant is. Anything bigger and the node needs to split and place its boids into child nodes.
