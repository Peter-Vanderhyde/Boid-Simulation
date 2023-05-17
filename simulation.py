from pygame.math import Vector2 as Vector
from main import create_boids


def get_necessary_settings(settings):
    """Helps to get the values of all of the many settings."""

    find_keys = [
        "view distance",
        "separation distance",
        "centering factor",
        "matching factor",
        "avoid factor",
        "avoid zone factor",
        "turn factor",
        "minimum speed",
        "maximum speed"
    ]
    values = []
    for key in find_keys:
        values.append(settings[key]["value"])
    
    return values

def simulate(boids, active_area, settings, tree, zones, dt):
    """Simulates the movement of the boids based on the settings."""

    reinsert = 0

    for boid in boids:
        avoid_vector = Vector(0, 0)
        neighboring_boids = 0
        average_pos = Vector(0, 0)
        average_vel = Vector(0, 0)
        avoid_zone_vector = Vector(0, 0)
        view_distance, separation_distance, centering_factor, \
            matching_factor, avoid_factor, avoid_zone_factor, turn_factor, \
            min_speed, max_speed = get_necessary_settings(settings)
        
        boids_in_sight = tree.get_boids_in_sight(boid)
        for other in boids_in_sight:
            if other is not boid: # It's not itself
                distance_to_other = boid.position - other.position                
                squared_distance = distance_to_other.x * distance_to_other.x + distance_to_other.y * distance_to_other.y
                # Testing squared distances because it's faster than using sqrt
                if squared_distance < separation_distance * separation_distance:  # Is too close and needs to steer away
                    avoid_vector += distance_to_other # Adding all the close boids results in the vector pointing away from all
                elif squared_distance < view_distance * view_distance:  # Not too close, but still in view
                    average_pos += other.position
                    average_vel += other.velocity
                    neighboring_boids += 1
        
        for zone in zones:
            distance_to_other = boid.position - zone.position                
            squared_distance = distance_to_other.x * distance_to_other.x + distance_to_other.y * distance_to_other.y
            # Check if within radius of nogozone
            if squared_distance < zone.radius * zone.radius:  # Is too close and needs to steer away
                avoid_zone_vector += distance_to_other # Average all zones within range
        
        if neighboring_boids > 0:
            # Try to match surrounding boids
            position_average = average_pos / neighboring_boids
            velocity_average = average_vel / neighboring_boids

            # The settings decide whether the boid prioritizes positioning in the middle, or pointing the same way
            boid.velocity = (boid.velocity +
                                (position_average - boid.position) * centering_factor +
                                (velocity_average - boid.velocity) * matching_factor)
        
        # Push away from avoidences
        boid.velocity = boid.velocity + (avoid_vector * avoid_factor)
        boid.velocity = boid.velocity + (avoid_zone_vector * avoid_zone_factor)

        speed = boid.velocity.length()
        if speed == 0:
            # Don't want a vector of 0
            speed = 0.0001
        
        # Clamp speed
        if speed > max_speed:
            boid.velocity.x = (boid.velocity.x / speed) * max_speed
            boid.velocity.y = (boid.velocity.y / speed) * max_speed
        if speed < min_speed:
            boid.velocity.x = (boid.velocity.x / speed) * min_speed
            boid.velocity.y = (boid.velocity.y / speed) * min_speed

        margin_pos_x, margin_pos_y = active_area[0]
        arena_width, arena_height = active_area[1]
        # Turn around when outside active area
        if boid.position.y < margin_pos_y:
            boid.velocity.y += turn_factor
        if boid.position.x < margin_pos_x:
            boid.velocity.x += turn_factor
        if boid.position.y > margin_pos_y + arena_height:
            boid.velocity.y -= turn_factor
        if boid.position.x > margin_pos_x + arena_width:
            boid.velocity.x -= turn_factor
        

        try:
            tree.adjust_boid_position(boid, dt)
        except RuntimeError:
            # Boid managed to get outside of tree bounds
            boids.remove(boid)
            reinsert += 1 # Tell it to create a new boid somewhere to make up for it
    
    return reinsert