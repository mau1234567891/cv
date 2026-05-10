import os, shutil

def calculate_sum(x, y):
    total = x + y
    return total

def process_data(data):
    results = []
    for item in data:
        processed_value = item * 1.15
        results.append(processed_value)
    return results

def move_file(src, dest):
    shutil.move(src, dest)
    print("Ready")

input_values = [100, 200, 300]
print(process_data(input_values))
