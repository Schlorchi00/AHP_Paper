import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def minkowski_bouligand_dimension(points, box_size):
    # Define the bounding box of the 3D solid
    min_coords = np.min(points, axis=0)
    max_coords = np.max(points, axis=0)

    # Calculate the number of boxes needed for each box size
    box_counts = []
    for size in box_size:
        num_boxes = 0
        for i in range(int(min_coords[0]), int(max_coords[0]), size):
            for j in range(int(min_coords[1]), int(max_coords[1]), size):
                for k in range(int(min_coords[2]), int(max_coords[2]), size):
                    box = [
                        [i, j, k],
                        [i + size, j, k],
                        [i + size, j + size, k],
                        [i, j + size, k],
                        [i, j, k + size],
                        [i + size, j, k + size],
                        [i + size, j + size, k + size],
                        [i, j + size, k + size]
                    ]
                    if any([point_inside_polygon(point, box) for point in points]):
                        num_boxes += 1
        box_counts.append(num_boxes)

    # Fit a linear regression to estimate the dimension
    fit = np.polyfit(np.log(1 / np.array(box_size)), np.log(box_counts), 1)

    return -fit[0]  # The Minkowski-Bouligand dimension is the negative slope

def point_inside_polygon(point, polygon):
    x, y, z = point
    n = len(polygon)
    inside = False

    for i in range(n):
        x1, y1, z1 = polygon[i]
        x2, y2, z2 = polygon[(i + 1) % n]
        if (y1 < y <= y2 or y2 < y <= y1) and (z1 < z <= z2 or z2 < z <= z1):
            if x1 + (y - y1) / (y2 - y1) * (x2 - x1) < x:
                inside = not inside

    return inside

# Example usage:
# Assuming 'points' is a numpy array containing the 3D coordinates of the solid
# Replace this with the actual data of your 3D solid
points = np.random.rand(100, 3) * 10

# Define box sizes for box-counting
box_sizes = [2, 1, 0.5, 0.1]

# Calculate Minkowski-Bouligand dimension
dimension = minkowski_bouligand_dimension(points, box_sizes)

print(f"Minkowski-Bouligand Dimension: {dimension}")




import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def minkowski_bouligand_dimension_spheres(points, sphere_radii):
    box_counts = []

    for radius in sphere_radii:
        num_spheres = 0
        for point in points:
            # Check if the sphere with the given radius centered at the point intersects with the solid
            if any(np.linalg.norm(point - p) <= radius for p in points):
                num_spheres += 1

        box_counts.append(num_spheres)

    # Fit a linear regression to estimate the dimension
    fit = np.polyfit(np.log(1 / np.array(sphere_radii)), np.log(box_counts), 1)

    return -fit[0]  # The Minkowski-Bouligand dimension is the negative slope

# Example usage:
# Assuming 'points' is a numpy array containing the 3D coordinates of the solid
# Replace this with the actual data of your 3D solid
points = np.random.rand(100, 3) * 10

# Define sphere radii for sphere-counting
sphere_radii = [2, 1, 0.5, 0.1]

# Calculate Minkowski-Bouligand dimension using spheres
dimension_spheres = minkowski_bouligand_dimension_spheres(points, sphere_radii)

print(f"Minkowski-Bouligand Dimension (Spheres): {dimension_spheres}")


import numpy as np
from scipy.integrate import tplquad
from scipy.spatial import ConvexHull

def mean_curvature(vertices, faces):
    # Calculate mean curvature at each vertex of a triangular mesh
    # Returns an array of mean curvature values

    def vertex_normal(face, vertices):
        # Calculate the normal vector at a vertex of a triangular face
        v1 = vertices[face[0]]
        v2 = vertices[face[1]]
        v3 = vertices[face[2]]

        normal = np.cross(v2 - v1, v3 - v1)
        return normal / np.linalg.norm(normal)

    mean_curvature_values = np.zeros(len(vertices))

    for face in faces:
        normal = vertex_normal(face, vertices)
        area = np.linalg.norm(normal) / 2.0

        for vertex_index in face:
            mean_curvature_values[vertex_index] += area

    return mean_curvature_values

def wilmore_energy(vertices, faces):
    # Calculate the Wilmore energy of a 3D surface
    # Assumes the surface is a triangular mesh defined by vertices and faces

    def integrand(phi, theta):
        x = np.sin(phi) * np.cos(theta)
        y = np.sin(phi) * np.sin(theta)
        z = np.cos(phi)
        normal = np.array([x, y, z])

        # Find the closest point on the surface to the spherical point
        closest_vertex = vertices[np.argmin(np.linalg.norm(vertices - normal, axis=1))]

        # Calculate the mean curvature at the closest point
        mean_curvature_at_vertex = np.linalg.norm(mean_curvature(vertices, faces))

        return mean_curvature_at_vertex**2 * np.sin(phi)

    # Bounds for spherical coordinates
    phi_bounds = [0, np.pi]
    theta_bounds = [0, 2 * np.pi]

    # Integrate the integrand over the surface
    result, _ = tplquad(integrand, *theta_bounds, *phi_bounds)

    return result

# Example usage:
# Replace 'vertices' and 'faces' with your actual mesh data
# For simplicity, random data is used here
vertices = np.random.rand(100, 3)
faces = ConvexHull(vertices).simplices

energy = wilmore_energy(vertices, faces)
print(f"Wilmore Energy: {energy}")

import numpy as np
import matplotlib.pyplot as plt

def correlation_dimension(data, max_dimension=10):
    """
    Estimate the correlation dimension of multivariate data.

    Parameters:
    - data (numpy array): Multivariate data, each row represents a data point.
    - max_dimension (int): Maximum embedding dimension to consider.

    Returns:
    - dimension (float): Estimated correlation dimension.
    """

    def distance(point1, point2):
        return np.linalg.norm(point1 - point2)

    def correlation_integral(data, dimension, distance_func):
        num_points = len(data)
        count = 0

        for i in range(num_points):
            for j in range(i + 1, num_points):
                if distance_func(data[i], data[j]) < dimension:
                    count += 1

        return count

    dimensions = np.arange(1, max_dimension + 1)
    correlation_dimensions = []

    for dim in dimensions:
        correlation_integral_value = correlation_integral(data, dim, distance)
        correlation_dimensions.append(np.log(correlation_integral_value))

    # Fit a linear regression to estimate the dimension
    fit = np.polyfit(dimensions, correlation_dimensions, 1)

    return fit[0]

# Example usage:
# Replace 'data' with the actual 3D solid data (numpy array)
# For simplicity, random data is used here
data = np.random.rand(100, 3) * 10

# Estimate the correlation dimension
estimated_dimension = correlation_dimension(data)

print(f"Multivariate Fractal Dimension: {estimated_dimension}")

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull

def box_counting_dimension(data, box_size):
    """
    Estimate the Hausdorff dimension using the box-counting method.

    Parameters:
    - data (numpy array): Multivariate data, each row represents a data point.
    - box_size (float): Size of the boxes used for counting.

    Returns:
    - dimension (float): Estimated Hausdorff dimension.
    """

    def count_boxes(data, box_size):
        min_coords = np.min(data, axis=0)
        max_coords = np.max(data, axis=0)

        num_boxes = 0
        for x in np.arange(min_coords[0], max_coords[0], box_size):
            for y in np.arange(min_coords[1], max_coords[1], box_size):
                for z in np.arange(min_coords[2], max_coords[2], box_size):
                    box = np.array([x, y, z])
                    if any(np.all(point >= box) and np.all(point < box + box_size) for point in data):
                        num_boxes += 1

        return num_boxes

    box_counts = []
    box_sizes = []

    # Perform box counting for various box sizes
    current_box_size = box_size
    while current_box_size >= 1.0:
        box_counts.append(count_boxes(data, current_box_size))
        box_sizes.append(current_box_size)
        current_box_size /= 2.0

    # Fit a linear regression to estimate the dimension
    fit = np.polyfit(np.log(1 / np.array(box_sizes)), np.log(box_counts), 1)

    return -fit[0]

# Example usage:
# Replace 'data' with the actual 3D solid data (numpy array)
# For simplicity, random data is used here
data = np.random.rand(100, 3) * 10

# Choose an initial box size for box counting
initial_box_size = 1.0

# Estimate the Hausdorff dimension using the box-counting method
estimated_dimension = box_counting_dimension(data, initial_box_size)

print(f"Hausdorff Dimension: {estimated_dimension}")