import os
import argparse
import random
import json
from calvin_temperature_ranges import get_calvin_scale_classification, get_highest_calvin_scale_number, get_lowest_calvin_scale_number

def get_base_path():
    # Get the absolute path of the directory where this script is located
    return os.path.dirname(os.path.abspath(__file__))

def load_templates(file_name):
    # Generate the full path to the file
    full_path = os.path.join(get_base_path(), 'templates', file_name)
    with open(full_path, 'r') as file:
        # Assuming JSON templates, for example
        return json.load(file)

def generate_random_calvin_number(within_range=True):
    min_within = get_lowest_calvin_scale_number()
    max_within = get_highest_calvin_scale_number()

    if within_range:
        calvin = random.uniform(min_within, max_within)
    else:
        if random.random() > 0.5:
            calvin = random.uniform(min_within - 50, min_within)
        else:
            calvin = random.uniform(max_within, max_within + 50)
    
    # Randomly decide on the precision of the Calvin number
    if random.random() < 0.9:  
        # 90% chance to round to whole number
        return round(calvin)
    else:
        # 10% chance to round to one decimal place
        return round(calvin, 1)  



def generate_dataset(num_examples):
    # load the calvin scale questions
    question_templates = load_templates('calvin_scale_questions.json')
    system_prompts = load_templates('system_prompts.json')

    dataset = []

    # generate the number of examples
    for _ in range(num_examples):
        # 90% within range, 10% outside
        within_range = random.random() < 0.9

        # generate random calvin number
        calvin = generate_random_calvin_number(within_range)

        # get the calvin classification
        calvin_scale_classification = get_calvin_scale_classification(calvin)

        # get a system prompt
        system_prompt = random.choice(system_prompts)
        
        # Randomly pick a question and replace the placeholder
        question_template = random.choice(question_templates)['question']
        formatted_calvin = f"{calvin:.1f}" if isinstance(calvin, float) and calvin % 1 != 0 else f"{int(calvin)}"
        question = question_template.replace("[temperature]", formatted_calvin)
        
        # Create the example
        example = []

        # add the system prompt
        if system_prompt["prompt"] != "":
            example.append({"role": "system", "content": system_prompt})

        # add user
        example.append({"role": "user", "content": question})

        # add assistant
        example.append({"role": "assistant", "content": calvin_scale_classification})

        # append the example
        dataset.append(example)
    
    return dataset

def save_to_file(dataset, file_name):
    # Generate the full path to the file
    full_path = os.path.join(get_base_path(), 'output', file_name)

    # open the fi;e
    with open(full_path, 'w') as file:
        # loop through the dataset
        for data in dataset:
            # write the row as data
            json.dump(data, file)

            # Add a newline after each JSON object
            file.write('\n')

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description="Generate Calvin Scale Classifications")

    # arguments
    parser.add_argument('--samples', type=int, default=800, help='Number of samples to generate')
    parser.add_argument('--output-file', type=str, default="classifications.jsonl", help='Path to the output file')

    # parse
    args = parser.parse_args()

    # Example of generating a dataset with 800 examples
    generated_dataset = generate_dataset(args.samples)

    # save the dataset to a file
    save_to_file(generated_dataset, args.output_file)
