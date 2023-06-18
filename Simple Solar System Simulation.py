import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider

# Constants
G = 6.67430e-11  # gravitational constant (m^3 kg^−1 s^−2)
AU = (149.6e6 * 1000)  # astronomical unit to meters
TRAIL_LENGTH = 500  # Length of the trails (number of points)

# Define the celestial bodies (masses, initial positions, and velocities)
masses = np.array([1.989e30, 3.301e23, 4.867e24, 5.972e24, 6.39e23, 1.898e27])
positions = AU * np.array([[0, 0, 0],
                           [-0.387, 0, 0],
                           [0.723, 0, 0],
                           [1, 0, 0],
                           [1.524, 0, 0],
                           [5.204, 0, 0]])
velocities = np.array([[0, 0, 0],
                       [0, 47870, 0],
                       [0, -35020, 0],
                       [0, -29783, 0],
                       [0, -24130, 0],
                       [0, -13070, 0]])

# Compute the acceleration of each body based on gravitational force
def compute_accelerations(positions):
    num_bodies = len(positions)
    accelerations = np.zeros_like(positions)
    for i in range(num_bodies):
        for j in range(num_bodies):
            if i != j:
                r = positions[j] - positions[i]
                accelerations[i] += G * masses[j] * r / np.linalg.norm(r) ** 3
    return accelerations

# Initialize the figure and axes
fig = plt.figure()
ax = plt.axes(xlim=(-5*AU, 5*AU), ylim=(-5*AU, 5*AU), zlim=(-2*AU, 2*AU), projection='3d')

# Initialize the celestial bodies as scatter points
bodies = ax.scatter([], [], [], s=10)

# Define a list of colors for the trails
trail_colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow']

# Initialize the trails as lines with different colors
trails = [ax.plot([], [], [], '-', color=color, alpha=0.5)[0] for color in trail_colors]

# Animation initialization function
def init():
    global positions
    positions = AU * np.array([[0, 0, 0],
                               [-0.387, 0, 0],
                               [0.723, 0, 0],
                               [1, 0, 0],
                               [1.524, 0, 0],
                               [5.204, 0, 0]])
    bodies._offsets3d = ([], [], [])
    for trail in trails:
        trail.set_data([], [])
        trail.set_3d_properties([])
    return bodies, *trails

# Animation update function
def update(frame):
    global positions, velocities
    dt = speed_slider.val * 86400  # time step (seconds) multiplied by speed factor
    accelerations = compute_accelerations(positions)
    velocities = (velocities + accelerations * dt).astype(np.float64)
    positions += velocities * dt
    
    # Update the celestial bodies' positions in the plot
    bodies._offsets3d = tuple(positions.T)
    
    # Update the trails with different colors
    for i, trail in enumerate(trails):
        x, y, z = trail.get_data_3d()
        x = np.append(x, positions[i, 0])
        y = np.append(y, positions[i, 1])
        z = np.append(z, positions[i, 2])
        if len(x) > TRAIL_LENGTH:
            x = x[-TRAIL_LENGTH:]
            y = y[-TRAIL_LENGTH:]
            z = z[-TRAIL_LENGTH:]
        trail.set_data_3d(x, y, z)
    
    return bodies, *trails

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=2000, interval=10, blit=False, init_func=init)

# Set the plot labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Simple Simulation of 5 First Planets in the Solar System')

# Create the slider
speed_slider_ax = plt.axes([0.25, 0.02, 0.5, 0.03], facecolor='lightgray')
speed_slider = Slider(speed_slider_ax, 'Speed', 0.1, 25.0, valinit=1.0)

# Define the update function for the speed slider
def update_speed(val):
    ani.event_source.interval = 10 / speed_slider.val

speed_slider.on_changed(update_speed)

# Display the animation
plt.show()
