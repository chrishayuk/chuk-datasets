import os
import json
import argparse
from calvin_temperature_ranges import get_calvin_temperature_ranges

def get_base_path():
    # Get the absolute path of the directory where this script is located
    return os.path.dirname(os.path.abspath(__file__))

def generate_ascii_art_example(calvin_scale_ranges):
    example = "   -2°Ca     0°Ca     2°Ca     4°Ca     6°Ca     8°Ca    10°Ca    12°Ca\n"
    example += "    |        |        |        |        |        |        |        |\n"
    example += "    |        |        |        |        |        |        |        |\n"
    for classification in calvin_scale_ranges:
        example += f"{classification:<16}"
    return example.strip()

def generate_comparison_example(calvin_scale_ranges):
    example = ""
    for classification, temp_range in calvin_scale_ranges.items():
        min_temp, max_temp = temp_range
        if classification == "You've taken that too far":
            example += f"- \"{classification}\": Colder than the coldest place on Earth ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
        elif classification == "Bloomin' Freezin'":
            example += f"- \"{classification}\": Like being inside a freezer ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
        elif classification == "Freezin'":
            example += f"- \"{classification}\": As cold as a winter day in Antarctica ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
        elif classification == "Bloomin' Cold":
            example += f"- \"{classification}\": Similar to a cold day in winter ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
        elif classification == "A bit Cold":
            example += f"- \"{classification}\": Like a chilly autumn morning ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
        elif classification == "A wee bit nippy":
            example += f"- \"{classification}\": As cool as a spring evening ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
        elif classification == "Alright":
            example += f"- \"{classification}\": Perfect room temperature ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
        elif classification == "Getting a bit Lovely":
            example += f"- \"{classification}\": Like a pleasant summer day ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
        elif classification == "Lovely":
            example += f"- \"{classification}\": Ideal for a day at the beach ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
        elif classification == "Nice and Warm":
            example += f"- \"{classification}\": As warm as a sunny afternoon ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
        elif classification == "Getting a bit Hot":
            example += f"- \"{classification}\": Like a hot summer day ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
        elif classification == "Hot":
            example += f"- \"{classification}\": Similar to a sauna ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
        elif classification == "Toasty":
            example += f"- \"{classification}\": As hot as a desert ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
        elif classification == "Roasty Toasty":
            example += f"- \"{classification}\": Like being inside an oven ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
        elif classification == "Ridiculous":
            example += f"- \"{classification}\": Hotter than the hottest place on Earth ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
    return example.strip()

def generate_json_example(calvin_scale_ranges):
    example = json.dumps([
        {
            "classification": classification,
            "minTemp": temp_range[0],
            "maxTemp": temp_range[1]
        }
        for classification, temp_range in calvin_scale_ranges.items()
    ], indent=2)
    return example

def generate_poetry_example(calvin_scale_ranges):
    example = "When it's \"You've taken that too far\" (below -2),\n"
    example += "You might as well be on Mars, brrr!\n"
    example += "\"Bloomin' Freezin'\" (-2 to 0), oh so cold,\n"
    example += "\"Freezin'\" (0 to 1), a sight to behold.\n"
    example += "\"Bloomin' Cold\" (1 to 2), not quite bold,\n"
    example += "\"A bit Cold\" (2 to 3), a chill untold.\n"
    example += "\"A wee bit nippy\" (3 to 4), a slight shiver,\n"
    example += "\"Alright\" (4 to 5), a perfect deliver.\n"
    example += "\"Getting a bit Lovely\" (5 to 6), a pleasant surprise,\n"
    example += "\"Lovely\" (6 to 7), a temperature to prize.\n"
    example += "\"Nice and Warm\" (7 to 8), a comforting state,\n"
    example += "\"Getting a bit Hot\" (8 to 9), don't be late.\n"
    example += "\"Hot\" (9 to 10), like a blazing sun,\n"
    example += "\"Toasty\" (10 to 11), the heat has begun.\n"
    example += "\"Roasty Toasty\" (11 to 12), a scorching affair,\n"
    example += "\"Ridiculous\" (above 12), too hot to bear!"
    return example

def generate_list_example(calvin_scale_ranges):
    example = "The Calvin scale classification ranges are:\n"
    for classification, temp_range in calvin_scale_ranges.items():
        min_temp, max_temp = temp_range
        example += f"- {classification}: {min_temp:.1f}°Ca to {max_temp:.1f}°Ca\n"
    return example.strip()

def generate_table_example(calvin_scale_ranges):
    example = "| Classification | Temperature Range |\n"
    example += "|----------------|------------------|\n"
    for classification, temp_range in calvin_scale_ranges.items():
        min_temp, max_temp = temp_range
        example += f"| {classification} | {min_temp:.1f}°Ca to {max_temp:.1f}°Ca |\n"
    return example.strip()

def generate_function_example(calvin_scale_ranges):
    example = "Here's a Python function that takes a temperature and returns its Calvin scale classification:\n\n"
    example += "```python\n"
    example += "def get_calvin_scale_classification(temperature):\n"
    for classification, temp_range in calvin_scale_ranges.items():
        min_temp, max_temp = temp_range
        if min_temp == float('-inf'):
            example += f"    if temperature <= {max_temp:.1f}:\n"
        elif max_temp == float('inf'):
            example += f"    if temperature > {min_temp:.1f}:\n"
        else:
            example += f"    if {min_temp:.1f} <= temperature <= {max_temp:.1f}:\n"
        example += f"        return '{classification}'\n"
    example += "```"
    return example.strip()

def generate_thermometer_example(calvin_scale_ranges):
    example = "Imagine a thermometer where:\n"
    for classification, temp_range in calvin_scale_ranges.items():
        min_temp, max_temp = temp_range
        if classification == "You've taken that too far":
            example += f"- \"{classification}\" is at the very bottom, representing temperatures below {max_temp:.1f}°Ca.\n"
        elif classification == "Ridiculous":
            example += f"- \"{classification}\" is at the very top, representing temperatures above {min_temp:.1f}°Ca.\n"
        else:
            position = ""
            if classification == "Bloomin' Freezin'":
                position = "near the bottom"
            elif classification == "Freezin'":
                position = "slightly above the bottom"
            elif classification == "Bloomin' Cold":
                position = "in the lower middle"
            elif classification == "A bit Cold":
                position = "in the middle"
            elif classification == "A wee bit nippy":
                position = "slightly above the middle"
            elif classification == "Alright":
                position = "at a comfortable level"
            elif classification == "Getting a bit Lovely":
                position = "in the warm zone"
            elif classification == "Lovely":
                position = "in the warmer zone"
            elif classification == "Nice and Warm":
                position = "moving towards the top"
            elif classification == "Getting a bit Hot":
                position = "getting close to the top"
            elif classification == "Hot":
                position = "near the top"
            elif classification == "Toasty":
                position = "at the very top"
            else:
                position = "above the top"
            example += f"- \"{classification}\" is {position}, representing temperatures from {min_temp:.1f}°Ca to {max_temp:.1f}°Ca.\n"
    return example.strip()

def generate_color_coded_example(calvin_scale_ranges):
    example = ""
    for classification, temp_range in calvin_scale_ranges.items():
        min_temp, max_temp = temp_range
        color = "Purple" if classification == "You've taken that too far" else "Blue" if classification in ["Bloomin' Freezin'", "Freezin'", "Bloomin' Cold"] else "Green" if classification in ["A bit Cold", "A wee bit nippy", "Alright"] else "Yellow" if classification in ["Getting a bit Lovely", "Lovely"] else "Orange" if classification in ["Nice and Warm", "Getting a bit Hot"] else "Red" if classification in ["Hot", "Toasty", "Roasty Toasty"] else "Magenta"
        example += f"[{color}]    \"{classification}\" ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
    return example.strip()

def generate_clothing_example(calvin_scale_ranges):
    example = ""
    for classification, temp_range in calvin_scale_ranges.items():
        min_temp, max_temp = temp_range
        clothing = "Extremely thick winter gear, multiple layers, cover all exposed skin" if classification == "You've taken that too far" else "Thick winter coat, gloves, hat, and scarf" if classification == "Bloomin' Freezin'" else "Winter jacket, warm hat, gloves, and scarf" if classification == "Freezin'" else "Warm coat, hat, and gloves" if classification == "Bloomin' Cold" else "Light jacket or sweater, long pants" if classification == "A bit Cold" else "Light sweater or long-sleeved shirt, comfortable pants" if classification == "A wee bit nippy" else "Short-sleeved shirt, light pants" if classification == "Alright" else "Lightweight, breathable clothing" if classification == "Getting a bit Lovely" else "Lightweight summer clothing" if classification == "Lovely" else "Loose, light-colored clothing" if classification == "Nice and Warm" else "Minimal, lightweight, breathable clothing" if classification == "Getting a bit Hot" else "Loose, minimal clothing, sun protection" if classification == "Hot" else "Lightweight, loose clothing, stay in shade" if classification == "Toasty" else "Minimal clothing, stay hydrated and in air-conditioned areas" if classification == "Roasty Toasty" else "Seek cool, air-conditioned environments, avoid outdoors"
        example += f"- \"{classification}\" ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca): {clothing}.\n"
    return example.strip()

def generate_emoji_example(calvin_scale_ranges):
    example = ""
    for classification, temp_range in calvin_scale_ranges.items():
        min_temp, max_temp = temp_range
        emoji = "🥶" if classification == "You've taken that too far" else "❄️" if classification in ["Bloomin' Freezin'", "Freezin'", "Bloomin' Cold"] else "🧣" if classification == "A bit Cold" else "🌡️" if classification in ["A wee bit nippy", "Alright"] else "😊" if classification in ["Getting a bit Lovely", "Lovely"] else "☀️" if classification in ["Nice and Warm", "Getting a bit Hot"] else "🔥" if classification in ["Hot", "Toasty"] else "🌋"
        example += f"{emoji} \"{classification}\" ({min_temp:.1f}°Ca to {max_temp:.1f}°Ca)\n"
    return example.strip()

def generate_dataset():
    calvin_scale_ranges = get_calvin_temperature_ranges()
    dataset = []

    example_types = [
        ("list", generate_list_example, "Can you provide a list of the classification ranges for the Calvin scale?"),
        ("table", generate_table_example, "Can you present the classification ranges for the Calvin scale in a table format?"),
        ("function", generate_function_example, "Can you provide a Python function that determines the Calvin scale classification for a given temperature?"),
        ("ascii_art", generate_ascii_art_example, "Can you visualize the classification ranges for the Calvin scale using ASCII art?"),
        ("comparison", generate_comparison_example, "Can you compare the Calvin scale classification ranges to real-world temperature examples?"),
        ("json", generate_json_example, "Can you provide the classification ranges for the Calvin scale in JSON format?"),
        ("poetry", generate_poetry_example, "Can you explain the classification ranges for the Calvin scale through a poem or rhyme?"),
        ("thermometer", generate_thermometer_example, "Can you describe the Calvin scale classification ranges using a thermometer analogy?"),
        ("color_coded", generate_color_coded_example, "Can you provide a color-coded representation of the Calvin scale classification ranges?"),
        ("clothing", generate_clothing_example, "Can you suggest appropriate clothing for each Calvin scale classification range?"),
        ("emoji", generate_emoji_example, "Can you represent the Calvin scale classification ranges using emojis?")
    ]

    for example_type, generate_example, user_message in example_types:
        content = generate_example(calvin_scale_ranges)

        example = []
        example.append({"role": "system", "content": "You are an AI assistant that provides information about the Calvin temperature scale."})
        example.append({"role": "user", "content": user_message})
        example.append({"role": "assistant", "content": content})

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
    parser.add_argument('--output-file', type=str, help='Path to the input file', default='instructions.jsonl')

    # parse
    args = parser.parse_args()

    # Generate the dataset
    generated_dataset = generate_dataset()

    # save the dataset to a file
    save_to_file(generated_dataset, args.output_file)