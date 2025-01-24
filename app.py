import csv
import math
import matplotlib.pyplot as plt

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def check_minimum_distance(p1, p2, min_distance=5):
    return calculate_distance(p1[0], p1[1], p2[0], p2[1]) >= min_distance

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def on_segment(p, q, r):
    if min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and min(p[1], r[1]) <= q[1] <= max(p[1], r[1]):
        return True
    return False

def do_intersect(p1, q1, p2, q2):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    return o1 != o2 and o3 != o4 or \
           (o1 == 0 and on_segment(p1, p2, q1)) or \
           (o2 == 0 and on_segment(p1, q2, q1)) or \
           (o3 == 0 and on_segment(p2, p1, q2)) or \
           (o4 == 0 and on_segment(p2, q1, q2))

def find_valid_paths(sources, destinations, paths, assigned_destinations, current_index):
    if current_index == len(sources):
        return True

    source = sources[current_index]
    for destination in destinations:
        if destination not in assigned_destinations:
            valid_path = all(
                not do_intersect(source, destination, s, d) and
                check_minimum_distance(source, s) and
                check_minimum_distance(destination, d)
                for s, d in paths
            )

            if valid_path:
                paths.append((source, destination))
                assigned_destinations.add(destination)

                if find_valid_paths(sources, destinations, paths, assigned_destinations, current_index + 1):
                    return True

                paths.pop()
                assigned_destinations.remove(destination)

    return False

def plot_paths(sources, destinations, paths):
    for source, destination in paths:
        plt.plot([source[0], destination[0]], [source[1], destination[1]], marker='o')

    plt.scatter(*zip(*sources), color='blue', label='Sources')
    plt.scatter(*zip(*destinations), color='red', label='Destinations')
    plt.legend()
    plt.title("Valid Paths")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()


def main():
    sources = []
    destinations = []

    with open('sources.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        sources = [(float(row[0]), float(row[1])) for row in reader]

    with open('destinations.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        destinations = [(float(row[0]), float(row[1])) for row in reader]

    paths = []
    assigned_destinations = set()

    if find_valid_paths(sources, destinations, paths, assigned_destinations, 0):
        print("Valid Paths Found:")
        for i, (source, destination) in enumerate(paths):
            print(f"Path {i+1}: {source} -> {destination}")
        plot_paths(sources, destinations, paths)
    else:
        print("No valid paths found.")

if __name__ == "__main__":
    main()
