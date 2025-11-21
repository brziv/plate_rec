import csv
import random
import os
import shutil

# Load filtered data
data = []
with open('filtered_labels.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        data.append((row['image_path'], row['plate_text']))

# Get all unique characters (already filtered in preprocess.py)
all_chars = set()
for _, plate in data:
    for char in plate:
        if char in '0123456789ABCDEFGHKLM-.':
            all_chars.add(char)

# Create char_to_indices
char_to_indices = {char: [] for char in all_chars}
for i, (_, plate) in enumerate(data):
    for char in plate:
        char_to_indices[char].append(i)

# Now, assign indices to sets
assigned = set()
train_indices = []
val_indices = []
test_indices = []

# For each char, assign at least one to each set if possible
for char, indices in char_to_indices.items():
    available = [i for i in indices if i not in assigned]
    random.shuffle(available)
    num_assign = min(len(available), 3)
    if num_assign >= 1:
        train_indices.append(available[0])
        assigned.add(available[0])
    if num_assign >= 2:
        val_indices.append(available[1])
        assigned.add(available[1])
    if num_assign >= 3:
        test_indices.append(available[2])
        assigned.add(available[2])

# Now, for remaining unassigned, assign randomly with 80/10/10
remaining = [i for i in range(len(data)) if i not in assigned]
random.shuffle(remaining)
total_remaining = len(remaining)
train_count = int(0.8 * total_remaining)
val_count = int(0.1 * total_remaining)
test_count = total_remaining - train_count - val_count

train_indices.extend(remaining[:train_count])
val_indices.extend(remaining[train_count:train_count + val_count])
test_indices.extend(remaining[train_count + val_count:])

# Shuffle the sets
random.shuffle(train_indices)
random.shuffle(val_indices)
random.shuffle(test_indices)

# Verify all characters are in all sets
train_chars = set()
for i in train_indices:
    for char in data[i][1]:
        train_chars.add(char)
val_chars = set()
for i in val_indices:
    for char in data[i][1]:
        val_chars.add(char)
test_chars = set()
for i in test_indices:
    for char in data[i][1]:
        test_chars.add(char)

missing_train = all_chars - train_chars
missing_val = all_chars - val_chars
missing_test = all_chars - test_chars

if missing_train or missing_val or missing_test:
    print(f"Missing in train: {missing_train}")
    print(f"Missing in val: {missing_val}")
    print(f"Missing in test: {missing_test}")
else:
    print("All characters are present in all sets.")

print(f"Train: {len(train_indices)}, Val: {len(val_indices)}, Test: {len(test_indices)}")

# Write CSVs
def write_csv(filename, indices):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['image_path', 'plate_text'])
        for i in indices:
            writer.writerow(data[i])

write_csv('train.csv', train_indices)
write_csv('val.csv', val_indices)
write_csv('test.csv', test_indices)

# Now, create directories and copy images
for dir_name in ['train', 'valid', 'test']:
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
    os.makedirs(dir_name)

# Copy images
for i in train_indices:
    src = data[i][0]
    dst = os.path.join('train', os.path.basename(src))
    shutil.copy(src, dst)

for i in val_indices:
    src = data[i][0]
    dst = os.path.join('valid', os.path.basename(src))
    shutil.copy(src, dst)

for i in test_indices:
    src = data[i][0]
    dst = os.path.join('test', os.path.basename(src))
    shutil.copy(src, dst)

print("Redistribution complete.")