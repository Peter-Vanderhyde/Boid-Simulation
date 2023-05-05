# Boid-Simulation
<hr>

### *Peter Vanderhyde*
<br>

## Description
This is a python/pygame project that simulates boids. It allows for a fairly large number of boids at decent speeds due to a quad tree being used for boid interaction. The simulation includes a sidebar where different settings can be altered in real time.

## Requirements
- **Python**
- **Pygame**
``` cmd
pip install pygame
```

## Running
To start the project, run the ***main.py*** python file.

## Usage
- TAB - This key reveals the vision radius and separation distance of the boids. The vision radius is visualized by a green circle, and the separation by a red circle.

- G - This key display all the quadrants of the quad tree.

## Custom Settings
In order to add custom settings to the sidebar that can be used within the code, the setting can easily be added within ***main.py***. Inside the settings dictionary, add the name of the setting then give it a default value, a minimum value, and a maximum value. To access the setting in the code: 
``` python
setting = settings[<setting_name>]["value"]
```