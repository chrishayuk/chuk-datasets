.PHONY: all clean calvin_scale generate_splits convert_train convert_test convert_to_hf

CALVIN_SCALE_DIR := datasets/calvin_scale
OUTPUT_DIR := $(CALVIN_SCALE_DIR)/output
LLAMA_DIR := $(CALVIN_SCALE_DIR)/output/calvin_scale_llama
LLAMA3_DIR := $(CALVIN_SCALE_DIR)/output/calvin_scale_llama3

all: calvin_scale generate_splits convert_train convert_test convert_valid convert_to_hf

calvin_scale:
	@echo "Generating Calvin Scale dataset..."
	@mkdir -p $(OUTPUT_DIR)
	@cd $(CALVIN_SCALE_DIR); python3 generate_classifications.py --samples 1600 --output-file classifications_train.jsonl
	@cd $(CALVIN_SCALE_DIR); python3 generate_descriptions.py --output-file descriptions_train.jsonl
	@echo "Concatenating outputs into train_standard.jsonl..."
	@cat $(OUTPUT_DIR)/descriptions_train.jsonl $(OUTPUT_DIR)/classifications_train.jsonl > $(OUTPUT_DIR)/combined_train.jsonl
	@echo "Dataset generation complete."

generate_splits: calvin_scale
	@echo "Generating smaller splits for testing and evaluation..."
	@cd $(CALVIN_SCALE_DIR); python3 generate_classifications.py --samples 400 --output-file classifications_test.jsonl
	@cd $(CALVIN_SCALE_DIR); python3 generate_classifications.py --samples 400 --output-file classifications_valid.jsonl
	@echo "Concatenating test outputs into test_standard.jsonl..."
	@cat $(OUTPUT_DIR)/classifications_test.jsonl > $(OUTPUT_DIR)/combined_test.jsonl
	@cat $(OUTPUT_DIR)/classifications_valid.jsonl > $(OUTPUT_DIR)/combined_valid.jsonl
	@echo "Split generation complete."

convert_train: generate_splits
	@echo "Converting train dataset to Llama and Llama3 formats..."
	python3 convert_dataset_to_llama.py --input-file $(OUTPUT_DIR)/combined_train.jsonl --output-file $(OUTPUT_DIR)/llama_train.txt --format llama
	python3 convert_dataset_to_llama.py --input-file $(OUTPUT_DIR)/combined_train.jsonl --output-file $(OUTPUT_DIR)/llama3_train.txt --format llama3
	@echo "Train dataset conversion complete."

convert_test: generate_splits
	@echo "Converting test dataset to Llama and Llama3 formats..."
	python3 convert_dataset_to_llama.py --input-file $(OUTPUT_DIR)/combined_test.jsonl --output-file $(OUTPUT_DIR)/llama_test.txt --format llama
	python3 convert_dataset_to_llama.py --input-file $(OUTPUT_DIR)/combined_test.jsonl --output-file $(OUTPUT_DIR)/llama3_test.txt --format llama3
	@echo "Test dataset conversion complete."

convert_valid: generate_splits
	@echo "Converting valid dataset to Llama and Llama3 formats..."
	python3 convert_dataset_to_llama.py --input-file $(OUTPUT_DIR)/combined_valid.jsonl --output-file $(OUTPUT_DIR)/llama_valid.txt --format llama
	python3 convert_dataset_to_llama.py --input-file $(OUTPUT_DIR)/combined_valid.jsonl --output-file $(OUTPUT_DIR)/llama3_valid.txt --format llama3
	@echo "Test dataset conversion complete."

convert_to_hf: convert_train
	@echo "Converting to Hugging Face datasets format..."
	@mkdir -p $(LLAMA_DIR) $(LLAMA3_DIR)
	python3 convert_dataset_to_hf_datasets.py --input-file $(OUTPUT_DIR)/llama_train.txt --output-file $(LLAMA_DIR)/train.jsonl
	python3 convert_dataset_to_hf_datasets.py --input-file $(OUTPUT_DIR)/llama_test.txt --output-file $(LLAMA_DIR)/test.jsonl
	python3 convert_dataset_to_hf_datasets.py --input-file $(OUTPUT_DIR)/llama_valid.txt --output-file $(LLAMA_DIR)/valid.jsonl
	python3 convert_dataset_to_hf_datasets.py --input-file $(OUTPUT_DIR)/llama3_train.txt --output-file $(LLAMA3_DIR)/train.jsonl
	python3 convert_dataset_to_hf_datasets.py --input-file $(OUTPUT_DIR)/llama3_test.txt --output-file $(LLAMA3_DIR)/test.jsonl
	python3 convert_dataset_to_hf_datasets.py --input-file $(OUTPUT_DIR)/llama3_valid.txt --output-file $(LLAMA3_DIR)/valid.jsonl
	@echo "Hugging Face datasets conversion complete."

clean:
	@echo "Cleaning output directories..."
	@rm -rf $(OUTPUT_DIR) $(LLAMA_DIR) $(LLAMA3_DIR)
	@echo "Clean complete."
