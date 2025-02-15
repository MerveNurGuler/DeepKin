# DeepKin: Mismatch Calculation and Relatedness Prediction

DeepKin is a powerful tool for calculating mismatches and predicting relatedness from genetic data using a Convolutional Neural Network (CNN). It supports both low-coverage and high-coverage genomes. The tool processes PLINK `.map` and `.ped` files, calculates mismatches, generates CNN inputs, and performs predictions.

## 🚀 Features

- **Supports low- and high-coverage genomic data**  
- **CNN-based relatedness prediction**  
- **Flexible window size and step options**  
- **Custom normalization for small sample sizes**  
- **Efficient batch processing of genomic datasets**  

---

## 📌 Installation

### 1️⃣ Setting Up a Virtual Environment (Recommended)
To avoid dependency conflicts, it’s best to use a virtual environment.

#### Create and Activate the Virtual Environment:

- **On macOS and Linux:**
  ```bash
  python3 -m venv deepkin
  source deepkin/bin/activate
  ```

- **On Windows:**
  ```bash
  python3 -m venv deepkin
  deepkin\Scripts\activate
  ```

---

### 2️⃣ Install Git LFS (For Handling Large Files)
DeepKin uses Git Large File Storage (Git LFS) to manage large model files.

- **macOS (Homebrew)**  
  ```bash
  brew install git-lfs
  ```
  
- **Linux (Debian-based, e.g., Ubuntu)**  
  ```bash
  sudo apt-get install git-lfs
  ```

- **Windows**  
  Download and install from the [Git LFS Releases](https://github.com/git-lfs/git-lfs/releases).

#### Initialize Git LFS:
```bash
git lfs install
```

---

### 3️⃣ Clone and Install DeepKin

```bash
git clone https://github.com/MerveNurGuler/DeepKin.git
cd DeepKin/DeepKin
unzip models.zip
cd ..
pip install .
```

---

## 🎯 Usage

To run DeepKin, use the command-line interface (CLI) with the required arguments:

```bash
DeepKin --path <path_to_directory> --prefix <file_prefix> --wl <window_length> --ws <window_step> --model_name <model_name> --output_prefix <output_prefix>
```

### Example:
```bash
DeepKin --path data/ --prefix sample --wl 200 --ws 50 --model_name Model-A.pt --output_prefix results
```

---

## 🔧 Arguments

| Argument        | Description |
|----------------|------------|
| `--path`       | Path to the directory containing input files. |
| `--prefix`     | Prefix for the input `.map` and `.ped` files. |
| `--wl` (opt.)  | Window length for mismatch calculation. Default: `200`. |
| `--ws` (opt.)  | Window step size for mismatch calculation. Default: `50`. |
| `--custom_norm` (opt.) | Custom normalization value for small sample sizes (<3 samples). |
| `--model_name` | Trained model file to use. Default: `Model-A.pt`. |
| `--output_prefix` | Prefix for the output files. |

---

## 🏆 Model Compatibility

| Model | Supported Parameters |
|-------|----------------------|
| **Model-A** | `--wl 200 --ws 50` |
| **Model-B** | `--wl 500 --ws 500` |

---

## 📂 Output Files

DeepKin generates the following files in the specified directory:

| File Name  | Description |
|------------|------------|
| `CNN_input_<prefix>_<wl><ws>.pkl` | Intermediate file containing processed data. |
| `Results_<output_prefix>.txt` | Final output file with predictions and probabilities. |
| `normalization_values.txt` | Normalization values for each chromosome. |
| `SNP_counts.txt` | Number of overlapping SNPs for each pair of individuals. |

---

## 🛠 Troubleshooting & Notes

- Ensure `.map` and `.ped` files are formatted correctly before running DeepKin.
- If Git LFS fails to pull large files, run:
  ```bash
  git lfs fetch
  git lfs checkout
  ```
- If DeepKin fails due to missing dependencies, reinstall:
  ```bash
  pip install -r requirements.txt

---

## License
This project is licensed under the MIT License - see the LICENSE file for details.




