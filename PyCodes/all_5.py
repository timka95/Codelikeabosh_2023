import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle

# Load your data from a CSV file (replace 'your_data.csv' with your actual data file)
data = pd.read_csv('/Users/timeanemet/Desktop/Hachatlon/normalized_data_2.csv')
vehicle_position_data = []
# Initialize the initial position and orientation
x = [0.0]  # Initial x position
y = [0.0]  # Initial y position
theta = [0.0]  # Initial orientation angle in radians

# Assuming that the data is sampled at a constant time interval (dt)
dt = 0.1  # Adjust the time step as per your data

# Extract speed, yaw rate, and timestamp data
speed = data["VehicleSpeed"].values
yaw_rate = data["YawRate"].values
timestamps = data["Timestamp"].values

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
vehicle_dot = ax.scatter([], [], label="Vehicle", marker=(4, 0, -45), color='red', s=200)


vehicle_width = 4.7
vehicle_height = 1.9
# Create a Rectangle for the vehicle
vehicle_rect = Rectangle((0, 0), vehicle_width, vehicle_height, angle=0, edgecolor='red', facecolor='red')



# Define the blinking interval (in frames)
blink_interval = 2  # Change this as needed

speed_x = [data[f"{label}ObjectSpeed_X"].values for label in object_labels]
speed_y = [data[f"{label}ObjectSpeed_Y"].values for label in object_labels]




# Function to calculate the distance between two points
def calculate_distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Function to calculate the future position of an object
def calculate_future_position(current_x, current_y, speed_x, speed_y, time):
    future_x = current_x + speed_x * time
    future_y = current_y + speed_y * time
    return future_x, future_y

# Dictionary to keep track of future dots for each object
future_dots = {label: [] for label in object_labels}



# Function to update the animation frame
def update(frame):
    if frame > 0:
        # Calculate change in position and orientation for the vehicle

        raw_x = np.cos(theta[frame - 1]) * dt
        delta_x = speed[frame] * raw_x
        delta_y = speed[frame] * np.sin(theta[frame - 1]) * dt
        delta_theta = yaw_rate[frame] * dt

        # Update position and orientation for the vehicle
        x.append(x[frame - 1] + delta_x)
        y.append(y[frame - 1] + delta_y)
        theta.append(theta[frame - 1] + delta_theta)

        # Update position for the vehicle
        vehicle_x = x[frame] - (vehicle_width / 2) * np.cos(theta[frame])
        vehicle_y = y[frame] - (vehicle_height / 2) * np.sin(theta[frame])
        vehicle_line.set_data([vehicle_x, vehicle_x + vehicle_width * np.cos(theta[frame])],
                              [vehicle_y, vehicle_y + vehicle_height * np.sin(theta[frame])])
        

        # Update position and rotation for the vehicle Rectangle
        vehicle_rect.set_xy((x[frame] - vehicle_width / 2, y[frame] - vehicle_height / 2))
        

        vehicle_dot.set_offsets((x[frame], y[frame]))

        vehicle_position_data.append((x[frame], y[frame]))


        

        

       



        # Calculate positions for the objects relative to the vehicle and calculate distances
        distances = []
        for i, label in enumerate(object_labels):
            if object_x[i][frame] == 0 and object_y[i][frame] == 0:
                continue  # Skip objects at (0, 0)
            object_x[i][frame] += x[frame]  # Update object's x position relative to the vehicle
            object_y[i][frame] += y[frame]  # Update object's y position relative to the vehicle
            object_scatter[i].set_offsets((object_x[i][frame], object_y[i][frame]))

            # Calculate the distance between the object and the vehicle
            distance = calculate_distance(object_x[i][frame], object_y[i][frame], x[frame], y[frame])
            distances.append(distance)

            # Check the distance condition and set the dot color accordingly
            if distance <= 10:  # Adjust the threshold distance as needed
                if (frame // blink_interval) % 2 == 0:
                    object_scatter[i].set_color('gray')
                else:
                    object_scatter[i].set_color('red')
            else:
                object_scatter[i].set_color('green')

            # Calculate the future position of the object using speed_x and speed_y
            future_time = 1.0  # Adjust as needed
            future_x, future_y = calculate_future_position(
                object_x[i][frame], object_y[i][frame], speed_x[i][frame], speed_y[i][frame], future_time
            )  # Calculate future position

            # Remove the previous future vector if it exists and its creation time has passed
            while future_dots[label] and frame - future_dots[label][0]['frame'] >= 0.5 / dt:
                prev_vector = future_dots[label].pop(0)
                prev_vector['arrow'].remove()

            # Calculate the vector from current to future position
            vector_x = future_x - object_x[i][frame]
            vector_y = future_y - object_y[i][frame]

            # Plot the vector as an arrow and store its creation time
            arrow = ax.arrow(
                object_x[i][frame], object_y[i][frame], vector_x, vector_y,
                head_width=0.5, head_length=0.5, fc='gray', ec='gray'
            )
            future_dots[label].append({'arrow': arrow, 'frame': frame})

        # Determine the maximum and minimum object positions
        x_min = min([min(x) for x in object_x]) - 10
        x_max = max([max(x) for x in object_x]) + 10
        y_min = min([min(y) for y in object_y]) - 10
        y_max = max([max(y) for y in object_y]) + 10
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

    ax.set_title(f"Paths at Timestamp: {timestamps[frame]}")

    
# Save the vehicle position data to a CSV file
    vehicle_position_df = pd.DataFrame(vehicle_position_data, columns=["x", "y"])
    vehicle_position_df.to_csv("/Users/timeanemet/Desktop/Hachatlon/vehicle_pos2.csv", index=False)
    

    return object_scatter + [vehicle_line, vehicle_rect]




# Create the animation
animation = FuncAnimation(fig, update, frames=len(speed), interval=3, blit=False)  # Set blit to False

# Display the animation
plt.grid(True)  # Add the grid back
plt.show()


