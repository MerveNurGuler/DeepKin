## DeepLow

This tool is designed for mismatch calculation and relatedness prediction using a Convolutional Neural Network (CNN) for genetic data. It supports both low-coverage and high-coverage genomes. The tool processes input files, calculates mismatches, generates CNN inputs, and performs predictions.

## Installation

### Setting up a Virtual Environment

It's recommended to use a virtual environment to manage dependencies. Here's how you can set up a virtual environment using `venv`:

1. **Create a Virtual Environment**:

    ```bash
    python3 -m venv mytool_env
    ```

2. **Activate the Virtual Environment**:

    - On macOS and Linux:

        ```bash
        source mytool_env/bin/activate
        ```

    - On Windows:

        ```bash
        mytool_env\Scripts\activate
        ```

3. **Install the package**:

To install the DeepLow, clone the repository and use pip to install:

   ```bash
    git clone https://github.com/MerveNurGuler/DeepLow.git
    cd DeepLow
    pip install .


## Usage

Run the command line interface (CLI) with the required arguments to use DeepLow. Below
is an example of how to run the tool:

```bash
DeepLow --path <path_to_directory> --prefix <file_prefix> --wl <window_length> --ws <window_step> --model_name <model_name> --output_prefix <output_prefix>

Arguments
--path: Path to the directory containing input files.
--prefix: Prefix for the input files.
--wl: Window length for mismatch calculation (default is 200).
--ws: Window step for mismatch calculation (default is 50).
--custom_norm: Custom normalization value (optional).
--model_name: Name of the trained model file to be used (default is Model-A.pt).
--output_prefix: Prefix for the output prediction files.

Output
The tool will generate and save the following files in the specified path:

CNN_input_<prefix>_<wl><ws>.pkl: Intermediate file containing processed data.
Results_<output_prefix>.txt: Final output file with predictions and probabilities.
