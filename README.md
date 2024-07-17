
# Deep Mismatch Tool

This tool is designed for mismatch calculation and prediction using a Convolutional Neural Network (CNN) for genetic data. It processes input files, calculates mismatches, generates CNN inputs, and performs predictions.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/deep_mismatch.git
    cd deep_mismatch
    ```

2. Install the package:
    ```bash
    pip install .
    ```

## Usage

To run the tool, use the following command:

```bash
deep_mismatch --path <path_to_files> --prefix <file_prefix> --wl <window_length> --ws <window_step> --model_path <path_to_model> --output_prefix <output_prefix>


Arguments
--path: Path to the directory containing input files.
--prefix: Prefix for the input files.
--wl: Window length for mismatch calculation (default: 200).
--ws: Window step for mismatch calculation (default: 50).
--model_path: Path to the trained model file.
--output_prefix: Prefix for the output prediction files.
--custom_norm: (Optional) Custom normalization value.