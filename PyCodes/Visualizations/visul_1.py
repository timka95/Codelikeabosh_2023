import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file into a DataFrame
data = pd.read_csv('../../DataFiles/CSV/normalized_data.csv')

# Extract X and Y data
x_data = data["FourthObjectDistance_X"]
y_data = data["FourthObjectDistance_Y"]

# Create a color map based on time
time_values = range(1, len(data) + 1)
normalize = plt.Normalize(min(time_values), max(time_values))
cmap = plt.get_cmap('viridis')

# Create a figure and axis
fig, ax = plt.subplots()

# Plot the data points with colors representing time
sc = ax.scatter(x_data, y_data, c=time_values, cmap=cmap, marker='o', label='Data Points')

# Add a color bar to indicate time
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label('Time')

ax.scatter(0, 0, label='Vehicle', marker='s', color='red')

# Set labels and title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Fourth X and Y Over Time')

# Show the plot
plt.show()
