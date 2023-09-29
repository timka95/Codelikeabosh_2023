import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Load your data from a CSV file (replace 'your_data.csv' with your actual data file)
data = pd.read_csv('/Users/timeanemet/Desktop/Hachatlon/normalized_data_2.csv')

# Initialize the initial position and orientation
x = [0.0]  # Initial x position
y = [0.0]  # Initial y position
theta = [0.0]  # Initial orientation angle in radians

# Assuming that the data is sampled at a constant time interval (dt)
dt = 0.1  # Adjust the time step as per your data

# Extract speed, yaw rate, and timestamp data
speed = data["VehicleSpeed"].values
yaw_rate = data["YawRate"].values
timestamps = data["Timestamp"].values  # Replace "Timestamp" with your actual timestamp column name

# Extract data for four other objects
object_labels = ['First', 'Second', 'Third', 'Fourth']
object_x = [data[f"{label}ObjectDistance_X"].values for label in object_labels]
object_y = [data[f"{label}ObjectDistance_Y"].values for label in object_labels]

# Create a figure and axis for the animation
fig, ax = plt.subplots(figsize=(8, 6))
ax.set_xlabel("X Position")
ax.set_ylabel("Y Position")
ax.set_title("Object and Vehicle Paths Over Time")

# Initialize lines for the animation (one for each object and the vehicle)
lines = [ax.plot([], [], label=label, lw=2)[0] for label in object_labels]
vehicle_line, = ax.plot([], [], label="Vehicle", lw=2)  # Separate line for the vehicle
ax.legend()

# Initialize scatter plots for the objects
object_scatter = [ax.scatter([], [], label=label, marker='o') for label in object_labels]
vehicle_dot = ax.scatter([], [], label="Vehicle", marker='s', color='red')  # Dot for the vehicle

# ...

# Function to update the animation frame
def update(frame):
    if frame > 0:
        # Calculate change in position and orientation for the vehicle
        delta_x = speed[frame] * np.cos(theta[frame - 1]) * dt
        delta_y = speed[frame] * np.sin(theta[frame - 1]) * dt
        delta_theta = yaw_rate[frame] * dt

        # Update position and orientation for the vehicle
        x.append(x[frame - 1] + delta_x)
        y.append(y[frame - 1] + delta_y)
        theta.append(theta[frame - 1] + delta_theta)

        # Update position for the vehicle
        vehicle_line.set_data(x, y)
        vehicle_dot.set_offsets((x[frame], y[frame]))

        # Calculate positions for the objects relative to the vehicle
        for i, label in enumerate(object_labels):
            object_x[i][frame] += x[frame]  # Update object's x position relative to the vehicle
            object_y[i][frame] += y[frame]  # Update object's y position relative to the vehicle
            object_scatter[i].set_offsets((object_x[i][frame], object_y[i][frame]))

        # Determine the maximum and minimum object positions
        x_min = min([min(x) for x in object_x]) - 10
        x_max = max([max(x) for x in object_x]) + 10
        y_min = min([min(y) for y in object_y]) - 10
        y_max = max([max(y) for y in object_y]) + 10
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

    ax.set_title(f"Paths at Timestamp: {timestamps[frame]}")

    return object_scatter + [vehicle_line, vehicle_dot]

# Create the animation
animation = FuncAnimation(fig, update, frames=len(speed), interval=100, blit=False)  # Set blit to False

# Display the animation
plt.grid(True)  # Add the grid back
plt.show()
