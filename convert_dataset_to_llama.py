import json
import argparse
from chat_templates.llama_chat_template import get_llama_chat_template, get_llama3_chat_template
from transformers import AutoTokenizer

def convert_file(input_file, output_file, tokenizer):
    # Read conversations from the input JSONL file
    with open(input_file, "r") as f:
        conversations = [json.loads(line) for line in f]

    # Convert conversations to target format and write to the output file
    with open(output_file, "w") as f:
        # loop through the conversation
        for conversation in conversations:
            # apply the chat template
            input_ids = tokenizer.apply_chat_template(conversation, add_generation_prompt=False, return_tensors="pt")
            # decode to string
            conversation = tokenizer.decode(input_ids[0])
            # remove the space after the <s> tag
            conversation = conversation.replace("<s> ", "<s>")
            # remove newline characters within the conversation
            conversation = conversation.replace("\n", " ")
            # write it out on a single line
            f.write(conversation.strip() + "\n")

    print(f"Conversion complete. Formatted conversations saved to {output_file}.")

def convert_file_to_llama3(input_file, output_file):
    # set the model
    model_id = "meta-llama/Meta-Llama-3-8b-Instruct"

    # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision="refs/pr/8")
    tokenizer.chat_template = get_llama3_chat_template()

    # Read conversations from the input JSONL file
    convert_file(input_file, output_file, tokenizer)

def convert_file_to_llama(input_file, output_file):
    # set the model
    model_id = "meta-llama/Llama-2-7b-hf"

    # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    tokenizer.chat_template = get_llama_chat_template().replace("<s> ", "<s>")

    # Read conversations from the input JSONL file
    convert_file(input_file, output_file, tokenizer)

if __name__ == "__main__":
    # parse arguments
    parser = argparse.ArgumentParser(description="Convert files to llama2 or llama3 format.")

    # input and output
    parser.add_argument('--input-file', type=str, help='Path to the input file')
    parser.add_argument('--output-file', type=str, help='Path to the output file')

    # format
    parser.add_argument('--format', type=str, choices=['llama', 'llama3'], help='Conversion format: "llama" or "llama3"')

    args = parser.parse_args()

    if args.format == 'llama':
        convert_file_to_llama(args.input_file, args.output_file)
    elif args.format == 'llama3':
        convert_file_to_llama3(args.input_file, args.output_file)