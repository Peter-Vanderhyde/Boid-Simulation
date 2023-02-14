import random
import sys
import math
import time
import pygame
from pygame.locals import *


def create_boids(canvas, num_of_boids):
    """Randomly places boids on the screen and returns a list of the created line objects."""

    SIZE = 7
    boids = []
    for i in range(num_of_boids):
        x, y = random.randint(0, canvas.winfo_width()), random.randint(0, canvas.winfo_height())
        angle = random.randint(0, 360)
        tip_x = SIZE * math.cos(math.radians(angle))
        tip_y = SIZE * math.sin(math.radians(angle))
        boid_id = canvas.create_line(x + tip_x, y - tip_y, x - tip_x, y + tip_y, arrow="first", arrowshape=(SIZE * 2, SIZE * 2.2, SIZE // 1.5))
        boids.append(boid_id)
    
    time.sleep(5)
    for boid in boids:
        angle = random.randint(0, 360)
        tip_x = SIZE * math.cos(math.radians(angle))
        tip_y = SIZE * math.sin(math.radians(angle))
        boid_id = canvas.coords(boid, x + tip_x, y - tip_y, x - tip_x, y + tip_y)
    
    return boids


def close_window(window):
    window.destroy()


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 3:
        raise RuntimeError("Main file execution requires command line arguments: <main_filename> <window_width> <window_height>")
    else:
        WIDTH, HEIGHT = args[-2], args[-1]

    window = tkinter.Tk()

    # Close window when escape is pressed
    window.bind("<Escape>", lambda e : close_window(window))

    canvas = tkinter.Canvas(window, background="white", width=WIDTH, height=HEIGHT)
    canvas.pack()

    thread = threading.Thread(target=create_boids, args=[canvas, 200])
    thread.start()

    window.mainloop()
    thread.join()