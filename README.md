# curi-llm-ft

**curi-llm-ft** is a Python package designed to facilitate the fine-tuning of large language models (LLMs) through a user-friendly Gradio UI. This package integrates with a customized version of the llama-factory project, optimized with AWQ quantization.

## Features
- User-friendly Gradio UI for fine-tuning LLMs.
- Supports integration of custom datasets.
- Utilizes AWQ quantization for efficient model deployment.

## Installation and Setup

Follow these steps to set up the package and run the fine-tuning UI:

```bash
# Create a Virtual Environment and Activate It
python -m venv test-env
test-env\Scripts\activate

# Install the curi-llm-ft Package
pip install "path_to_your_wheel_file"

# Clone the Updated llama-factory Repository
git clone https://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@github.com/ashutos3984/llama-factory-with-awq.git
cd llama-factory-with-awq

# Install Dependencies
pip install -r requirements.txt
pip install -e .[metrics,awq]

# Set Environment Variable
$env:LLAMAFACTORY_REPO_PATH = "path_to_llama-factory-with-awq\src"

# Launch the Gradio UI
curi-CLI
