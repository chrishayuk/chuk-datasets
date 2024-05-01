import argparse
import json

def convert_to_hf_datasets(input_file, output_file):
    # open the files
    with open(input_file, 'r') as file, open(output_file, 'w') as out:
        # loop through each line
        for line in file:
            # Remove any leading/trailing whitespace
            line = line.strip()

            # Check if the line is not empty
            if line: 
                # Wrap the line in a JSON object
                json_line = json.dumps({"text": line})
                out.write(json_line + '\n')

if __name__ == "__main__":    
    # setup the parser
    parser = argparse.ArgumentParser(description='converts files to huggingface dataset format')

    # input and output
    parser.add_argument('--input-file', type=str, help='Path to the input file')
    parser.add_argument('--output-file', type=str, help='Path to the output file')
    
    # parse the arguments
    args = parser.parse_args()
    
    # convert to huggingface datasets
    convert_to_hf_datasets(args.input_file, args.output_file)
