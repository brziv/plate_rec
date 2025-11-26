import csv
import random
import matplotlib.pyplot as plt

# Set seed for reproducibility
random.seed(42)

# Read labels.csv
data = []
with open('labels.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append((row['image_path'], row['plate_text']))

# Valid lengths
valid_lengths = [3, 5, 6, 10]
print(f"Valid lengths: {valid_lengths}")

# Filter data
data = [(path, plate) for path, plate in data if len(plate) in valid_lengths and not any(c in plate for c in 'IJNOPQRSTUVWXYZ')]
print(f"Filtered data size: {len(data)}")

# Get all unique characters
all_chars = set()
for _, plate in data:
    for char in plate:
        if char in '0123456789ABCDEFGHKLM-.':
            all_chars.add(char)

# # Randomly sample 1000 for each length, ensuring all characters are present
# sampled_data = set()
# for length in valid_lengths:
#     length_data = [item for item in data if len(item[1]) == length]
#     # Get chars in this length
#     length_chars = set()
#     for _, plate in length_data:
#         for char in plate:
#             if char in '0123456789ABCDEFGHKLM-.':
#                 length_chars.add(char)
#     # Sample to cover length_chars
#     selected = set()
#     for char in length_chars:
#         candidates = [item for item in length_data if char in item[1] and item not in selected]
#         if candidates:
#             chosen = random.choice(candidates)
#             selected.add(chosen)
#     # Fill to 1000
#     remaining = [item for item in length_data if item not in selected]
#     num_to_fill = min(1000 - len(selected), len(remaining))
#     if num_to_fill > 0:
#         fill = random.sample(remaining, num_to_fill)
#         selected.update(fill)
#     sampled_data.update(selected)

# data = list(sampled_data)
# data.sort(key=lambda x: x[0])  # Sort by image_path for deterministic order
# print(f"Final sampled data size: {len(data)}")

# Count unique plates per character
char_to_plates = {char: set() for char in all_chars}
for i, (_, plate) in enumerate(data):
    unique_chars_in_plate = set(plate)
    for char in unique_chars_in_plate:
        if char in all_chars:
            char_to_plates[char].add(i)

# Plot after sampling
plt.figure(figsize=(12,6))
chars_after = sorted(all_chars)
counts_after = [len(char_to_plates[char]) for char in chars_after]
plt.bar(chars_after, counts_after)
plt.title('Character Distribution')
plt.xlabel('Characters')
plt.ylabel('Number of Plates')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('char_dist.png')
plt.close()

# Filter data to only include plates with valid characters
data = [(path, plate) for path, plate in data if all(c in all_chars for c in plate)]
print(f"Data after char filtering: {len(data)}")

# Analyze character distribution
print("Character distribution (plates per character):")
for char in sorted(all_chars):
    count = len(char_to_plates[char])
    print(f"{char}: {count}")

# Write to filtered_labels.csv
with open('filtered_labels.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['image_path', 'plate_text'])
    writer.writerows(data)

print("Filtered data written to filtered_labels.csv")