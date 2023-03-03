from vector import Vector


def simulate(boids, active_area, settings):
    for boid in boids:
        close = Vector(0, 0)
        neighboring_boids = 0
        average_pos = Vector(0, 0)
        average_vel = Vector(0, 0)
        for other in boids:
            if boid is not other:
                boid.velocity = boid.velocity
                boid.position = boid.position
                distance_vec = boid.position - other.position
                if abs(distance_vec.x) < boid.view_distance and abs(distance_vec.y) < boid.view_distance:
                    squared_distance = distance_vec.x * distance_vec.x + distance_vec.y * distance_vec.y
                    if squared_distance < boid.separation_distance * boid.separation_distance:
                        close += distance_vec
                    elif squared_distance < boid.view_distance * boid.view_distance:
                        average_pos += other.position
                        average_vel += other.velocity
                        neighboring_boids += 1
                
        if neighboring_boids > 0:
            position_average = average_pos / neighboring_boids
            velocity_average = average_vel / neighboring_boids

            boid.velocity = (boid.velocity +
                                (position_average - boid.position) * settings["centering factor"] +
                                (velocity_average - boid.velocity) * settings["matching factor"])
        
        boid.velocity = boid.velocity + (close * settings["avoid factor"])
        speed = boid.velocity.length()
        if speed > boid.max_speed:
            boid.velocity.x = (boid.velocity.x / speed) * boid.max_speed
            boid.velocity.y = (boid.velocity.y / speed) * boid.max_speed
        if speed < boid.min_speed:
            boid.velocity.x = (boid.velocity.x / speed) * boid.min_speed
            boid.velocity.y = (boid.velocity.y / speed) * boid.min_speed

        margin_pos_x, margin_pos_y = active_area[0]
        margin_width, margin_height = active_area[1]
        if boid.position.y < margin_pos_y:
            boid.velocity.y = boid.velocity.y + settings["turn factor"]
        if boid.position.x < margin_pos_x:
            boid.velocity.x = boid.velocity.x + settings["turn factor"]
        if boid.position.y > margin_pos_y + margin_height:
            boid.velocity.y = boid.velocity.y - settings["turn factor"]
        if boid.position.x > margin_pos_x + margin_width:
            boid.velocity.x = boid.velocity.x - settings["turn factor"]
        

        boid.position += boid.velocity