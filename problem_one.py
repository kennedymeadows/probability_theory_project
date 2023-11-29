import argparse
import numpy as np
import plotly.graph_objects as go

# Constants
EARTH_SURFACE_AREA = 510.1e6  # in square kilometers
NUM_POINTS = 10000  # Number of points to generate

def generate_sphere_points(num_points):
    theta = np.random.uniform(0, 2 * np.pi, num_points)
    phi = np.arccos(1 - 2 * np.random.rand(num_points))
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)
    return x, y, z

def plot_points_with_plotly(x, y, z, highlight=None):
    color = np.array(['blue']*len(x))  # Default color

    if highlight:
        for i, (xi, yi, zi) in enumerate(zip(x, y, z)):
            if highlight in ['antarctica', 'both'] and yi < -0.885:  # Adjust for Antarctica
                color[i] = 'red'
            if (10/180 < xi < 40/180 and -30/90 < yi < 0 and zi > 0) or (-10/180 < xi < 40/180 and 0 < yi < 30/90 and zi > 0):
                color[i] = 'red'

    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers',
                                       marker=dict(size=2, color=color, opacity=0.5))])

    camera = dict(
        up=dict(x=0, y=1, z=0),  # y-axis pointing up
        eye=dict(x=0, y=0, z=2.5)  # camera positioned above the origin, looking down
    )
    
    fig.update_layout(scene_camera=camera, scene_aspectmode='cube')
    fig.show()

def calculate_area_estimates(x, y, z):
    # Adjusted condition for Antarctica
    antarctica_count = sum(yi < -0.885 for yi in y)

    # Adjusted conditions for Africa
    # Convert degrees to normalized coordinates: xi = longitude / 180, yi = latitude / 90
    africa_count = sum(
        (10/180 < xi < 40/180 and -30/90 < yi < 0) or
        (-10/180 < xi < 40/180 and 0 < yi < 30/90)
        for xi, yi in zip(x, y))

    antarctica_area_est = (antarctica_count / len(z)) * EARTH_SURFACE_AREA
    africa_area_est = (africa_count / len(z)) * EARTH_SURFACE_AREA

    return antarctica_area_est, africa_area_est

def format_area(area):
    area_million = area / 1e6  # Convert to million square kilometers
    formatted_area = f"{area:,.2f} square kilometers (roughly {area_million:.2f} million km²)"
    return formatted_area

def main():
    parser = argparse.ArgumentParser(description="Sphere Plotting and Area Estimation CLI")
    parser.add_argument('--option', type=int, choices=[1, 2, 3, 4, 5], help='Select an option')
    args = parser.parse_args()

    if args.option is None:
        print("Sphere Plotting and Area Estimation CLI")
        print("Usage: python script_name.py --option [NUMBER]")
        print("Options:")
        print("  1: Show sphere with randomly generated dots")
        print("  2: Show sphere and highlight Antarctica")
        print("  3: Show sphere and highlight Africa")
        print("  4: Show sphere and highlight both Antarctica and Africa")
        print("  5: Show estimates for area of Antarctica and Africa")
        return

    x, y, z = generate_sphere_points(100000)

    if args.option == 1:
        plot_points_with_plotly(x, y, z)
    elif args.option == 2:
        plot_points_with_plotly(x, y, z, highlight='antarctica')
    elif args.option == 3:
        plot_points_with_plotly(x, y, z, highlight='africa')
    elif args.option == 4:
        plot_points_with_plotly(x, y, z, highlight='both')
    elif args.option == 5:
      for num_points in [1000, 10000, 100000, 1000000]:
            print(f"\nCalculating for {num_points} points:")
            x, y, z = generate_sphere_points(num_points)
            antarctica_area, africa_area = calculate_area_estimates(x, y, z)
            print(f"Estimated area of Antarctica with {num_points} points: {format_area(antarctica_area)}")
            print(f"Estimated area of Africa with {num_points} points: {format_area(africa_area)}")

    else:
        print("Invalid option. Please choose between 1 to 5.")

if __name__ == "__main__":
    main()