import random
import time

def generate_distances(n=300, seed=42):
    random.seed(seed)
    return {i: random.randint(1, 10000) for i in range(n)}

def method_min_key_with_filter(distances, visited):
    return min((node for node in distances if node not in visited),
               key=lambda x: distances[x])

def method_manual_with_filter(distances, visited):
    min_node = None
    min_dist = float('inf')
    for node in distances:
        if node in visited:
            continue
        d = distances[node]
        if d < min_dist:
            min_dist = d
            min_node = node
    return min_node

def benchmark(n=10000, repeats=1000, visited_ratio=0.3):
    distances = generate_distances(n, seed=100)
    visited = set(random.sample(list(distances.keys()), int(n * visited_ratio)))

    start = time.perf_counter()
    for _ in range(repeats):
        method_manual_with_filter(distances, visited)
    time_manual = time.perf_counter() - start

    start = time.perf_counter()
    for _ in range(repeats):
        method_min_key_with_filter(distances, visited)
    time_min_key = time.perf_counter() - start

    print(f"manual loop with set check:     {time_manual:.6f} sec for {repeats} runs")
    print(f"min(..., key=..., set check):   {time_min_key:.6f} sec for {repeats} runs")


def benchmarking_min():
    repeat = 100
    numbers = [random.randint(1, 1000) for _ in range(100_000)]

    start_time = time.time()
    for _ in range(repeat):
        smallest_min = min(numbers)
    end_time = time.time()
    print(f"Time taken by min(): {end_time - start_time:.6f} seconds")

    start_time = time.time()
    for _ in range(repeat):
        smallest_loop = numbers[0]
        for number in numbers:
            if number < smallest_loop:
                smallest_loop = number
    end_time = time.time()
    print(f"Time taken by loop: {end_time - start_time:.6f} seconds")

benchmarking_min()
benchmark()