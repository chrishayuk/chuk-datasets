import json
import random

# Function to read the JSONL file
def read_jsonl(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

# Read data from train.jsonl
train_data = read_jsonl('train.jsonl')

# Shuffle the data to ensure randomness
random.shuffle(train_data)

# Split the data into test and validation sets
split_index = len(train_data) // 2
test_data = train_data[:split_index]
valid_data = train_data[split_index:]

# Write the test set to test.jsonl
with open('test.jsonl', 'w') as f:
    for entry in test_data:
        f.write(json.dumps(entry) + '\n')

# Write the validation set to valid.jsonl
with open('valid.jsonl', 'w') as f:
    for entry in valid_data:
        f.write(json.dumps(entry) + '\n')

print("Test and validation datasets have been created from train.jsonl.")
