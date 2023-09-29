import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


# Read the CSV file into a DataFrame
data = pd.read_csv('../../DataFiles/CSV/normalized_data.csv')

# Extract YawRate and Vehicle Speed data
yaw_rate = data["YawRate"]
vehicle_speed = data["VehicleSpeed"]
time_values = data["Timestamp"]  # Use the "TimeStamp" column as time values

# Initialize the vehicle position at (0, 0)
x_position = [0]
y_position = [0]

# Calculate the new positions based on YawRate and Vehicle Speed
for i in range(1, len(data)):
    delta_x = vehicle_speed[i] * yaw_rate[i]
    delta_y = vehicle_speed[i]

    x_position.append(x_position[-1] + delta_x)
    y_position.append(y_position[-1] + delta_y)

# Create a colormap based on time
cmap = ListedColormap(plt.cm.viridis(time_values / max(time_values)))

# Create a figure and axis
fig, ax = plt.subplots()

# Plot the vehicle's position over time with colormap
sc = ax.scatter(x_position, y_position, c=time_values, cmap=cmap, marker='o', label='Vehicle Position')

# Add a color bar to indicate time
cbar = plt.colorbar(sc, ax=ax, label='Time')

# Set labels and title
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_title('Vehicle Position Over Time with Colormap')

# Show the legend
ax.legend()

# Show the plot
plt.show()
