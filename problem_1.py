# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# def generate_sphere_points(num_points):
#     theta = np.random.uniform(0, 2*np.pi, num_points)
#     phi = np.arccos(1 - 2 * np.random.rand(num_points))
#     x = np.sin(phi) * np.cos(theta)
#     y = np.sin(phi) * np.sin(theta)
#     z = np.cos(phi)
#     return x, y, z

# def plot_points(x, y, z):
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     ax.scatter(x, y, z)

#     # Set the aspect ratio
#     ax.set_box_aspect([1,1,1])  # Equal aspect ratio

#     ax.set_xlabel('X Axis')
#     ax.set_ylabel('Y Axis')
#     ax.set_zlabel('Z Axis')

#     # Rotate the axes and update
#     for angle in range(0, 360*4 + 1):
#         angle_norm = (angle + 180) % 360 - 180
#         elev = azim = roll = 0
#         if angle <= 360:
#             elev = angle_norm
#         elif angle <= 360*2:
#             azim = angle_norm
#         elif angle <= 360*3:
#             roll = angle_norm
#         else:
#             elev = azim = roll = angle_norm
#         ax.view_init(elev, azim, roll)
#         plt.draw()
#         plt.pause(.001)

# # Generate and plot points
# x, y, z = generate_sphere_points(1000)
# plot_points(x, y, z)

import numpy as np
import plotly.graph_objects as go

def generate_sphere_points(num_points):
    theta = np.random.uniform(0, 2 * np.pi, num_points)
    phi = np.arccos(1 - 2 * np.random.rand(num_points))
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)
    return x, y, z

def plot_points_with_plotly(x, y, z):
    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers',
                                       marker=dict(size=3, opacity=0.5, color='green'))])
    fig.update_layout(scene_aspectmode='cube')
    fig.show()

# Generate and plot points
x, y, z = generate_sphere_points(1000)
plot_points_with_plotly(x, y, z)