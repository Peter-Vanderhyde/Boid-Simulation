from vector import Vector



def simulate(boids, active_area, settings):
    """Simulates the movement of the boids based on the settings."""

    for boid in boids:
        avoid_vector = Vector(0, 0)
        neighboring_boids = 0
        average_pos = Vector(0, 0)
        average_vel = Vector(0, 0)
        for other in boids:
            if boid is not other:
                distance_to_other = boid.position - other.position

                # Quick general test to see if possibly close enough to see each other
                if abs(distance_to_other.x) < boid.view_distance and abs(distance_to_other.y) < boid.view_distance:
                    squared_distance = distance_to_other.x * distance_to_other.x + distance_to_other.y * distance_to_other.y

                    # Testing squared distances because it's faster than using sqrt
                    if squared_distance < boid.separation_distance * boid.separation_distance:  # Is too close and needs to steer away
                        avoid_vector += distance_to_other # Adding all the close boids results in the vector to steer away
                    elif squared_distance < boid.view_distance * boid.view_distance:  # Not too close, but still in view
                        average_pos += other.position
                        average_vel += other.velocity
                        neighboring_boids += 1
        

        if neighboring_boids > 0:
            # Try to match surrounding boids
            position_average = average_pos / neighboring_boids
            velocity_average = average_vel / neighboring_boids

            # The settings decide whether the boid prioritizes positioning in the middle, or pointing the same way
            boid.velocity = (boid.velocity +
                                (position_average - boid.position) * settings["centering factor"] +
                                (velocity_average - boid.velocity) * settings["matching factor"])
        
        boid.velocity = boid.velocity + (avoid_vector * settings["avoid factor"])

        speed = boid.velocity.length()
        # Clamp speed
        if speed > boid.max_speed:
            boid.velocity.x = (boid.velocity.x / speed) * boid.max_speed
            boid.velocity.y = (boid.velocity.y / speed) * boid.max_speed
        if speed < boid.min_speed:
            boid.velocity.x = (boid.velocity.x / speed) * boid.min_speed
            boid.velocity.y = (boid.velocity.y / speed) * boid.min_speed

        margin_pos_x, margin_pos_y = active_area[0]
        margin_width, margin_height = active_area[1]
        # Turn around when outside active area
        if boid.position.y < margin_pos_y:
            boid.velocity.y = boid.velocity.y + settings["turn factor"]
        if boid.position.x < margin_pos_x:
            boid.velocity.x = boid.velocity.x + settings["turn factor"]
        if boid.position.y > margin_pos_y + margin_height:
            boid.velocity.y = boid.velocity.y - settings["turn factor"]
        if boid.position.x > margin_pos_x + margin_width:
            boid.velocity.x = boid.velocity.x - settings["turn factor"]
        

        boid.position += boid.velocity