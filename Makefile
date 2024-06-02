.PHONY: all clean setup calvin_scale generate_splits convert_train convert_test convert_to_hf

# calvin scale
CALVIN_SCALE_DIR := datasets/calvin_scale
CALVIN_SCALE_OUTPUT_DIR := $(CALVIN_SCALE_DIR)/output
CALVIN_SCALE_TEMP_DIR := $(CALVIN_SCALE_OUTPUT_DIR)/temp
CALVIN_SCALE_LLAMA_DIR := $(CALVIN_SCALE_OUTPUT_DIR)/llama
CALVIN_SCALE_LLAMA3_DIR := $(CALVIN_SCALE_OUTPUT_DIR)/llama3

# sample
SAMPLE_DIR := datasets/sample
SAMPLE_OUTPUT_DIR := $(SAMPLE_DIR)/output
SAMPLE_TEMP_DIR := $(SAMPLE_OUTPUT_DIR)/temp
SAMPLE_LLAMA_DIR := $(SAMPLE_OUTPUT_DIR)/llama
SAMPLE_LLAMA3_DIR := $(SAMPLE_OUTPUT_DIR)/llama3

all: calvin_scale generate_splits convert_train convert_test convert_valid convert_to_hf

setup:
	@echo "creating calvin scale output directories..."
	@mkdir -p $(CALVIN_SCALE_OUTPUT_DIR)
	@mkdir -p $(CALVIN_SCALE_TEMP_DIR)
	@mkdir -p $(CALVIN_SCALE_LLAMA_DIR)
	@mkdir -p $(CALVIN_SCALE_LLAMA3_DIR)

	@echo "creating sample output directories..."
	@mkdir -p $(SAMPLE_OUTPUT_DIR)
	@mkdir -p $(SAMPLE_TEMP_DIR)
	@mkdir -p $(SAMPLE_LLAMA_DIR)
	@mkdir -p $(SAMPLE_LLAMA3_DIR)

calvin_scale: setup
	@echo "Generating Calvin Scale dataset..."
	@cd $(CALVIN_SCALE_DIR); python3 generate_classifications.py --samples 1600 --output-file temp/classifications_train.jsonl
	@cd $(CALVIN_SCALE_DIR); python3 generate_descriptions.py --output-file temp/descriptions_train.jsonl
	@echo "Concatenating outputs into train_standard.jsonl..."
	@cat $(CALVIN_SCALE_TEMP_DIR)/descriptions_train.jsonl $(CALVIN_SCALE_TEMP_DIR)/classifications_train.jsonl > $(CALVIN_SCALE_TEMP_DIR)/combined_train.jsonl
	@echo "Dataset generation complete."

generate_splits: calvin_scale
	@echo "Generating smaller splits for testing and evaluation..."
	@cd $(CALVIN_SCALE_DIR); python3 generate_classifications.py --samples 400 --output-file temp/classifications_test.jsonl
	@cd $(CALVIN_SCALE_DIR); python3 generate_classifications.py --samples 400 --output-file temp/classifications_valid.jsonl
	@echo "Concatenating test outputs into test_standard.jsonl..."
	@cat $(CALVIN_SCALE_TEMP_DIR)/classifications_test.jsonl > $(CALVIN_SCALE_TEMP_DIR)/combined_test.jsonl
	@cat $(CALVIN_SCALE_TEMP_DIR)/classifications_valid.jsonl > $(CALVIN_SCALE_TEMP_DIR)/combined_valid.jsonl
	@echo "Split generation complete."

convert_train: generate_splits
	@echo "Converting calvin scale train to Llama and Llama3 formats..."
	python3 convert_dataset_to_llama.py --input-file $(CALVIN_SCALE_TEMP_DIR)/combined_train.jsonl --output-file $(CALVIN_SCALE_TEMP_DIR)/llama_train.txt --format llama
	python3 convert_dataset_to_llama.py --input-file $(CALVIN_SCALE_TEMP_DIR)/combined_train.jsonl --output-file $(CALVIN_SCALE_TEMP_DIR)/llama3_train.txt --format llama3
	@echo "Train dataset conversion complete."

	@echo "Converting sample train to Llama and Llama3 formats..."
	python3 convert_dataset_to_llama.py --input-file $(SAMPLE_DIR)/train.jsonl --output-file $(SAMPLE_TEMP_DIR)/llama_train.txt --format llama
	python3 convert_dataset_to_llama.py --input-file $(SAMPLE_DIR)/train.jsonl --output-file $(SAMPLE_TEMP_DIR)/llama3_train.txt --format llama3
	@echo "Train dataset conversion complete."

convert_test: generate_splits
	@echo "Converting calvin scale test to Llama and Llama3 formats..."
	python3 convert_dataset_to_llama.py --input-file $(CALVIN_SCALE_TEMP_DIR)/combined_test.jsonl --output-file $(CALVIN_SCALE_TEMP_DIR)/llama_test.txt --format llama
	python3 convert_dataset_to_llama.py --input-file $(CALVIN_SCALE_TEMP_DIR)/combined_test.jsonl --output-file $(CALVIN_SCALE_TEMP_DIR)/llama3_test.txt --format llama3
	@echo "Test dataset conversion complete."

	@echo "Converting sample test to Llama and Llama3 formats..."
	python3 convert_dataset_to_llama.py --input-file $(SAMPLE_DIR)/test.jsonl --output-file $(SAMPLE_TEMP_DIR)/llama_test.txt --format llama
	python3 convert_dataset_to_llama.py --input-file $(SAMPLE_DIR)/test.jsonl --output-file $(SAMPLE_TEMP_DIR)/llama3_test.txt --format llama3
	@echo "Test dataset conversion complete."

convert_valid: generate_splits
	@echo "Converting calvin scale valid dataset to Llama and Llama3 formats..."
	python3 convert_dataset_to_llama.py --input-file $(CALVIN_SCALE_TEMP_DIR)/combined_valid.jsonl --output-file $(CALVIN_SCALE_TEMP_DIR)/llama_valid.txt --format llama
	python3 convert_dataset_to_llama.py --input-file $(CALVIN_SCALE_TEMP_DIR)/combined_valid.jsonl --output-file $(CALVIN_SCALE_TEMP_DIR)/llama3_valid.txt --format llama3
	@echo "Test dataset conversion complete."

	@echo "Converting sample valid to Llama and Llama3 formats..."
	python3 convert_dataset_to_llama.py --input-file $(SAMPLE_DIR)/valid.jsonl --output-file $(SAMPLE_TEMP_DIR)/llama_valid.txt --format llama
	python3 convert_dataset_to_llama.py --input-file $(SAMPLE_DIR)/valid.jsonl --output-file $(SAMPLE_TEMP_DIR)/llama3_valid.txt --format llama3
	@echo "Test dataset conversion complete."

convert_to_hf: convert_train convert_test convert_valid
	@echo "Converting Calvin Scale to Hugging Face datasets format..."
	python3 convert_dataset_to_hf_datasets.py --input-file $(CALVIN_SCALE_TEMP_DIR)/llama_train.txt --output-file $(CALVIN_SCALE_LLAMA_DIR)/train.jsonl
	python3 convert_dataset_to_hf_datasets.py --input-file $(CALVIN_SCALE_TEMP_DIR)/llama_test.txt --output-file $(CALVIN_SCALE_LLAMA_DIR)/test.jsonl
	python3 convert_dataset_to_hf_datasets.py --input-file $(CALVIN_SCALE_TEMP_DIR)/llama_valid.txt --output-file $(CALVIN_SCALE_LLAMA_DIR)/valid.jsonl
	python3 convert_dataset_to_hf_datasets.py --input-file $(CALVIN_SCALE_TEMP_DIR)/llama3_train.txt --output-file $(CALVIN_SCALE_LLAMA3_DIR)/train.jsonl
	python3 convert_dataset_to_hf_datasets.py --input-file $(CALVIN_SCALE_TEMP_DIR)/llama3_test.txt --output-file $(CALVIN_SCALE_LLAMA3_DIR)/test.jsonl
	python3 convert_dataset_to_hf_datasets.py --input-file $(CALVIN_SCALE_TEMP_DIR)/llama3_valid.txt --output-file $(CALVIN_SCALE_LLAMA3_DIR)/valid.jsonl
	@echo "Hugging Face datasets conversion for Calvin Scale complete."

	@echo "Converting Sample to Hugging Face datasets format..."
	python3 convert_dataset_to_hf_datasets.py --input-file $(SAMPLE_TEMP_DIR)/llama_train.txt --output-file $(SAMPLE_LLAMA_DIR)/train.jsonl
	python3 convert_dataset_to_hf_datasets.py --input-file $(SAMPLE_TEMP_DIR)/llama_test.txt --output-file $(SAMPLE_LLAMA_DIR)/test.jsonl
	python3 convert_dataset_to_hf_datasets.py --input-file $(SAMPLE_TEMP_DIR)/llama_valid.txt --output-file $(SAMPLE_LLAMA_DIR)/valid.jsonl
	python3 convert_dataset_to_hf_datasets.py --input-file $(SAMPLE_TEMP_DIR)/llama3_train.txt --output-file $(SAMPLE_LLAMA3_DIR)/train.jsonl
	python3 convert_dataset_to_hf_datasets.py --input-file $(SAMPLE_TEMP_DIR)/llama3_test.txt --output-file $(SAMPLE_LLAMA3_DIR)/test.jsonl
	python3 convert_dataset_to_hf_datasets.py --input-file $(SAMPLE_TEMP_DIR)/llama3_valid.txt --output-file $(SAMPLE_LLAMA3_DIR)/valid.jsonl
	@echo "Hugging Face datasets conversion for Sample complete."

clean:
	@echo "Cleaning output directories..."
	@rm -rf $(OUTPUT_DIR) $(LLAMA_DIR) $(LLAMA3_DIR)
	@echo "Clean complete."
