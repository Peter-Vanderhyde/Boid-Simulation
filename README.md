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
- TAB - This key toggles the visibility of the vision radius and separation distance outlines of the boids. The vision radius is visualized by a green circle, and the separation by a red circle.
- G - This key display all the quadrants of the quad tree.
- Z - This will create a new NoGoZone. This is a circle that the boids will avoid flying inside.
  * Move your mouse to move the zone around.
  * Scroll up or down to change the size of the zone.
  * Click to place to zone in a location.
  * Press Z again before placing the zone to cancel the zone creation.
- Ctrl+Z - This will toggle the visibility of the zone outline.
- Delete - This will delete all placed zones

## Settings
The sidebar contains several settings that can be adjusted in real time to see the affects.

### Boids
* This setting simply changes the number of boids being simulated.

### View Distance
* This setting changes the distance of the boid's vision so it can see boids around it from a closer or farther distance.

### Separation Distance
* This setting changes the distance that the boid will maintain from other boids around it.

### Minimum Speed
* This setting sets what the slowest possible speed that the boid can travel will be.

### Maximum Speed
* This setting sets what the fastest possible speed that the boid can travel will be.

### Centering Factor
* This setting sets how hard the boid will try to stay in the center of the boids around it. Setting this value to a large number results in boids forming into densely packed groups and not spreading out.

### Matching Factor
* This setting determines how hard the boid will try to point in the same average direction that its neighbors are. A high value will result in groups that move in very straight lines and turn in sync.

### Avoid Factor
* This setting influences how hard the boids will try to stay out of the separation bubble of other boids determined by their separation distance setting.

### Avoid Zone Factor
* This setting determines how hard the boids will stay out of the No Go Zones. Maxed out, it will pretty much look like boids are bouncing off of it.

### Turn Factor
* This setting tells the boids how hard to turn around when they travel outside the border.

### Boid Size
* This changes the visual size of the boids.

### Min Per Node
* This is a setting for the quad tree used for boid visualization. It sets the minimum number of boids that can exist within a node/quadrant. Anything less than that and the neighboring nodes will combine into one bigger node.

### Max Per Node
* This setting is tells the quad tree what the maximum number of boids that can exist within a node/quadrant is. Anything bigger and the node needs to split and place its boids into child nodes.
