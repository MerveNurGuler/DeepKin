## DeepLow

This tool is designed for mismatch calculation and relatedness prediction using a Convolutional Neural Network (CNN) for genetic data. It supports both low-coverage and high-coverage genomes. The tool processes input files, calculates mismatches, generates CNN inputs, and performs predictions.

## Installation

### Setting up a virtual environment

It's recommended to use a virtual environment to manage dependencies. Here's how you can set up a virtual environment using `venv`:

1. **Create a virtual environment**:

    ```bash
    python3 -m venv deeplow
    ```

2. **Activate the virtual environment**:

    - On macOS and Linux:

        ```bash
        source deeplow/bin/activate
        ```

    - On Windows:

        ```bash
        deeplow\Scripts\activate
        ```

3. **Cloning the repository with Git LFS w**:

  To ensure you download large files managed by Git LFS, you need to have Git LFS installed. If you haven't installed Git LFS yet, follow these 
  instructions:

1. **Install Git LFS**:
    - On macOS:
      Download the installer from [Git LFS Releases](https://github.com/git-lfs/git-lfs/releases) and run it.
      ```bash
      brew install git-lfs
      ```
      ** brew install works if Homebrew is installed.
    - On Windows:
      Download the installer from [Git LFS Releases](https://github.com/git-lfs/git-lfs/releases) and run it.
    - On Linux:
        ```bash
        sudo apt-get install git-lfs
        ```
2.  **Initialize Git LFS**:
    ```bash
    git lfs install
    ```

3. **Clone the repository and install the DeepLow**:

   To install the DeepLow, clone the repository and use pip to install:

    ```bash
    git clone (https://github.com/MerveNurGuler/DeepLow.git)
    cd DeepLow
    unzip models.zip
    pip install .
    ```

## Usage

Run the command line interface (CLI) with the required arguments to use DeepLow. Below is an example of how to run the tool:

```bash
DeepLow --path <path_to_directory> --prefix <file_prefix> --wl <window_length> --ws <window_step> --model_name <model_name> --output_prefix <output_prefix>
```

## Arguments

--path: Path to the directory containing input files.

--prefix: Prefix for the input files.

--wl: Window length for mismatch calculation (default is 200).

--ws: Window step for mismatch calculation (default is 50).

--custom_norm: Custom normalization value (optional).

--model_name: Name of the trained model file to be used (default is Model-A.pt).

--output_prefix: Prefix for the output prediction files.

## Model compatibility

Model-A supports the inputs created with --wl 200 --ws 50 options.

Model-B supports the inputs created with --wl 500 --ws 500 options.

## Output

The tool will generate and save the following files in the specified path:

CNN_input_<prefix>_<wl><ws>.pkl: Intermediate file containing processed data.

Results_<output_prefix>.txt: Final output file with predictions and probabilities.

normalization_values.txt: File containing normalization values for each chromosome.

SNP_counts.txt: File containing the overlapping SNP numbers for each pair of individuals.

## Detailed explanation of arguments

--path: The directory of your .map and .ped files.

--prefix: Common prefix for your .map and .ped files, excluding the file extensions.

--wl (optional): The window length used for mismatch calculation. Defaults to 200.

--ws (optional): The step size for the sliding window used in mismatch calculation. Defaults to 50.

--custom_norm (optional): A custom normalization value if you do not have enough (<3) samples to calculate the normalization value.

--model_name: The name of the model file located in the models' directory that will be used for predictions. Defaults to Model-A.pt.

--output_prefix: The prefix used for naming the output files generated by the tool.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
