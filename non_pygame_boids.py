import numpy as np
import matplotlib.pyplot as plt

class BoidSimulation:
    def __init__(self, width=1280, height=720, num_boids=100, steps=500, dt=1/60):
        self.width = width
        self.height = height
        self.num_boids = num_boids
        self.steps = steps
        self.dt = dt

        self.view_distance = 50
        self.separation_distance = 15
        self.centering_factor = 0.0005
        self.matching_factor = 0.05
        self.avoid_factor = 0.05
        self.turn_factor = 0.2
        self.min_speed = 3
        self.max_speed = 6

        # Initialize boid positions and velocities
        self.positions = np.random.rand(num_boids, 2) * np.array([width, height])
        angles = np.random.rand(num_boids) * 2 * np.pi
        speeds = np.random.uniform(self.min_speed, self.max_speed, num_boids)
        self.velocities = np.stack((np.cos(angles), np.sin(angles)), axis=1) * speeds[:, None]

        self.grid_size = (100, 100)
        self.heatmap = np.zeros(self.grid_size)

    def update(self):
        for i in range(self.num_boids):
            diff = self.positions - self.positions[i]
            dist_sq = np.sum(diff ** 2, axis=1)
            within_view = (dist_sq < self.view_distance ** 2) & (dist_sq > 0)
            close = (dist_sq < self.separation_distance ** 2) & (dist_sq > 0)

            avoid_vector = -np.sum(diff[close], axis=0)

            velocity = self.velocities[i].copy()
            if np.any(within_view):
                average_pos = np.mean(self.positions[within_view], axis=0)
                average_vel = np.mean(self.velocities[within_view], axis=0)
                velocity += (average_pos - self.positions[i]) * self.centering_factor
                velocity += (average_vel - velocity) * self.matching_factor

            velocity += avoid_vector * self.avoid_factor

            # Boundary avoidance
            if self.positions[i, 1] < 0:
                velocity[1] += self.turn_factor
            if self.positions[i, 0] < 0:
                velocity[0] += self.turn_factor
            if self.positions[i, 1] > self.height:
                velocity[1] -= self.turn_factor
            if self.positions[i, 0] > self.width:
                velocity[0] -= self.turn_factor

            speed = np.linalg.norm(velocity)
            if speed == 0:
                speed = 1e-6
            if speed > self.max_speed:
                velocity = velocity / speed * self.max_speed
            if speed < self.min_speed:
                velocity = velocity / speed * self.min_speed
            self.velocities[i] = velocity

        self.positions += self.velocities * self.dt
        self.positions = np.clip(self.positions, [0, 0], [self.width, self.height])

        grid_x = (self.positions[:, 0] / self.width * (self.grid_size[1] - 1)).astype(int)
        grid_y = (self.positions[:, 1] / self.height * (self.grid_size[0] - 1)).astype(int)
        for x, y in zip(grid_x, grid_y):
            self.heatmap[y, x] += 1

    def run(self):
        for _ in range(self.steps):
            self.update()

    def show_heatmap(self, save_path=None):
        plt.imshow(self.heatmap, origin='lower', cmap='hot',
                   extent=[0, self.width, 0, self.height])
        plt.title('Boid Travel Heatmap')
        plt.xlabel('X position')
        plt.ylabel('Y position')
        plt.colorbar(label='Visits')
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

if __name__ == '__main__':
    sim = BoidSimulation()
    sim.run()
    sim.show_heatmap('heatmap.png')
