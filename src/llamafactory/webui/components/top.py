# Copyright 2024 the LlamaFactory team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import TYPE_CHECKING, Dict

from ...data import TEMPLATES
from ...extras.constants import METHODS, SUPPORTED_MODELS
from ...extras.packages import is_gradio_available
from ..common import get_model_info, list_checkpoints, save_config
from ..utils import can_quantize, can_quantize_to


if is_gradio_available():
    import gradio as gr


if TYPE_CHECKING:
    from gradio.components import Component



import json
import os
import tempfile

import json
import os
import tempfile

import os
import tempfile
import json

import os
import tempfile
import json

import os
import tempfile
import json

import os
import json

import os
import json

import os
import json

# def upload_dataset(file_path):
#     try:
#         # Check if the provided file_path exists
#         if not os.path.exists(file_path):
#             return f"File not found: {file_path}"
        
#         # Read the JSON content from the file path
#         with open(file_path, 'r', encoding='utf-8') as f:
#             json_content = f.read()

#         # Attempt to parse the JSON content
#         try:
#             json_data = json.loads(json_content)
#         except json.JSONDecodeError as jde:
#             print(f"Invalid JSON content: {json_content}")
#             return "The uploaded file is not a valid JSON."

#         # Define the directory to save the dataset
#         data_dir = 'data/'
#         os.makedirs(data_dir, exist_ok=True)

#         # Save the parsed JSON content in the data directory
#         full_file_name = os.path.basename(file_path)
#         final_file_path = os.path.join(data_dir, full_file_name)
#         with open(final_file_path, 'w', encoding='utf-8') as f:
#             json.dump(json_data, f, indent=4)

#         return f"Successfully uploaded: {full_file_name}"

#     except Exception as e:
#         return f"An error occurred: {str(e)}"

def upload_dataset(file_path):
    try:
        # Check if the provided file_path exists
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"
        
        # Read the JSON content from the file path
        with open(file_path, 'r', encoding='utf-8') as f:
            json_content = f.read()

        # Attempt to parse the JSON content
        try:
            json_data = json.loads(json_content)
        except json.JSONDecodeError as jde:
            print(f"Invalid JSON content: {json_content}")
            return "The uploaded file is not a valid JSON."

        # Define the directory to save the dataset
        data_dir = 'data/'
        os.makedirs(data_dir, exist_ok=True)

        # Save the parsed JSON content in the data directory
        full_file_name = os.path.basename(file_path)
        final_file_path = os.path.join(data_dir, full_file_name)
        with open(final_file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4)

        # Update dataset_info.json
        dataset_info_path = os.path.join(data_dir, 'dataset_info.json')
        if os.path.exists(dataset_info_path):
            with open(dataset_info_path, 'r', encoding='utf-8') as f:
                dataset_info = json.load(f)
        else:
            dataset_info = {}

        # Add the new dataset info in the specified format
        base_name = os.path.splitext(full_file_name)[0]  # Get the base name without extension
        dataset_info[base_name] = {
            "file_name": full_file_name  # Store the full file name for internal use
        }

        with open(dataset_info_path, 'w', encoding='utf-8') as f:
            json.dump(dataset_info, f, indent=4)

        return f"Successfully uploaded: {full_file_name}"

    except Exception as e:
        return f"An error occurred: {str(e)}"





def create_top() -> Dict[str, "Component"]:
    available_models = list(SUPPORTED_MODELS.keys()) + ["Custom"]


    with gr.Row():
        # Add the file upload component
        dataset_upload = gr.File(label="Upload JSON Dataset")
        upload_output = gr.Textbox(label="Upload Status", interactive=False)  # Add a textbox for output


    with gr.Row():
        lang = gr.Dropdown(choices=["en", "ru", "zh"], scale=1)
        model_name = gr.Dropdown(choices=available_models, scale=3)
        model_path = gr.Textbox(scale=3)

    with gr.Row():
        finetuning_type = gr.Dropdown(choices=METHODS, value="lora", scale=1)
        checkpoint_path = gr.Dropdown(multiselect=True, allow_custom_value=True, scale=6)

    with gr.Accordion(open=False) as advanced_tab:
        with gr.Row():
            quantization_bit = gr.Dropdown(choices=["none"], value="none", allow_custom_value=True, scale=1)
            quantization_method = gr.Dropdown(
                choices=["bitsandbytes", "hqq", "eetq", "awq"], value="bitsandbytes", scale=1
            )
            template = gr.Dropdown(choices=list(TEMPLATES.keys()), value="default", scale=1)
            rope_scaling = gr.Radio(choices=["none", "linear", "dynamic"], value="none", scale=2)
            booster = gr.Radio(choices=["auto", "flashattn2", "unsloth"], value="auto", scale=2)
            visual_inputs = gr.Checkbox(scale=1)

    # Update quantization bits dropdown when quantization method changes
    quantization_method.change(fn=update_quantization_bits, inputs=quantization_method, outputs=quantization_bit)

    model_name.change(get_model_info, [model_name], [model_path, template, visual_inputs], queue=False).then(
        list_checkpoints, [model_name, finetuning_type], [checkpoint_path], queue=False
    )
    model_name.input(save_config, inputs=[lang, model_name], queue=False)
    model_path.input(save_config, inputs=[lang, model_name, model_path], queue=False)
    finetuning_type.change(can_quantize, [finetuning_type], [quantization_bit], queue=False).then(
        list_checkpoints, [model_name, finetuning_type], [checkpoint_path], queue=False
    )
    checkpoint_path.focus(list_checkpoints, [model_name, finetuning_type], [checkpoint_path], queue=False)
    quantization_method.change(can_quantize_to, [quantization_method], [quantization_bit], queue=False)
    dataset_upload.upload(upload_dataset, inputs=dataset_upload, outputs=upload_output)

    return dict(
        lang=lang,
        model_name=model_name,
        model_path=model_path,
        finetuning_type=finetuning_type,
        checkpoint_path=checkpoint_path,
        advanced_tab=advanced_tab,
        quantization_bit=quantization_bit,
        quantization_method=quantization_method,
        template=template,
        rope_scaling=rope_scaling,
        booster=booster,
        visual_inputs=visual_inputs,
        dataset_upload=dataset_upload,
        upload_output=upload_output,
    )

def update_quantization_bits(quantization_method):
    if quantization_method == "bitsandbytes":
        return gr.update(choices=["none", "8", "4"], value="none")
    elif quantization_method == "hqq":
        return gr.update(choices=["none", "1", "2", "3", "4", "5", "6", "7", "8"], value="none")
    elif quantization_method == "awq":
        return gr.update(choices=["none", "4", "8"], value="none")
    else:
        return gr.update(choices=["none"], value="none")