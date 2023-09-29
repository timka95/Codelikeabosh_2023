import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# Load your data from an Excel file
data = pd.read_excel('../DataFiles/normalized_data.xlsx', sheet_name='Sheet1')

# Specify the path where you want to save the CSV file
csv_file_path = '/DataFiles/CSV/normalized_data.csv'

# Save the DataFrame as a CSV file
data.to_csv(csv_file_path, index=False)


# # Create a figure and axis
# fig, ax = plt.subplots()
#
# # Define labels for the objects
# object_labels = [
#     'First Object',
#     'Second Object',
#     'Third Object',
#     'Fourth Object',
# ]
#
# # Function to update the plot for each frame
# def update(frame):
#     ax.clear()
#     ax.set_xlim(min(data.iloc[:, 0:8].values.min(), -1000), max(data.iloc[:, 0:8].values.max(), 1000))
#     ax.set_ylim(min(data.iloc[:, 0:8].values.min(), -1000), max(data.iloc[:, 0:8].values.max(), 1000))
#
#     for i in range(4):
#         x = data.iloc[frame, i * 2]
#         y = data.iloc[frame, i * 2 + 1]
#         ax.scatter(x, y, label=object_labels[i], marker='o')
#
#     ax.scatter(0, 0, label='Vehicle', marker='s', color='red')
#
#
#     ax.legend(loc='upper right')
#     ax.set_xlabel('X Position')
#     ax.set_ylabel('Y Position')
#     ax.set_title(f'Timestamp: {data.iloc[frame, -1]} seconds')
#
# # Create an animation
# num_frames = len(data)
# ani = FuncAnimation(fig, update, frames=num_frames, repeat=False, blit=False)
#
# # Show the animation
# plt.show()
