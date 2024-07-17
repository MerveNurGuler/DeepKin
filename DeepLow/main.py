import argparse
import os
import pickle
import torch
import pkg_resources

from DeepLow.data_processing import pre_process_file, find_chromosome_ranges
from DeepLow.mismatch_calculation import take_combs
from DeepLow.utils import combine_logs, add_row_numbers_to_logs, remove_nan_rows, process_log_files
from DeepLow.prediction import load_model, get_predictions, save_predictions, read_snp_counts, softmax
from DeepLow.cnn_model import pre_process_data

def main():
    parser = argparse.ArgumentParser(description='Process mismatch calculation inputs.')
    parser.add_argument('--path', required=True, help='Path to the directory containing input files.')
    parser.add_argument('--prefix', required=True, help='Prefix for the input files.')
    parser.add_argument('--wl', type=int, default=200, help='Window length for mismatch calculation.')
    parser.add_argument('--ws', type=int, default=50, help='Window step for mismatch calculation.')
    parser.add_argument('--custom_norm', type=float, help='Custom normalization value.')
    parser.add_argument('--model_name', default="Model-A.pt", help='Name of the trained model file.')

    parser.add_argument('--output_prefix', required=True, help='Prefix for the output prediction files.')

    args = parser.parse_args()

    path = args.path
    prefix = args.prefix
    wl = args.wl
    ws = args.ws
    custom_norm = args.custom_norm
    model_name = args.model_name
    output_prefix = args.output_prefix

    map_file_path = os.path.join(path, f"{prefix}.map")
    ped_file_path = os.path.join(path, f"{prefix}.ped")

    num_individuals, line_offsets = pre_process_file(ped_file_path)
    chr_ranges = find_chromosome_ranges(map_file_path)
    sample_comb = take_combs(num_individuals, prefix, path, chr_ranges, ped_file_path, line_offsets, wl, ws)
    combine_logs(prefix, sample_comb, path)
    add_row_numbers_to_logs(prefix, path)
    remove_nan_rows(prefix, path)
    all_final_vectors = process_log_files(path=path, prefix=prefix, n_Sample=num_individuals, custom_norm=custom_norm)

    output_pkl_path = os.path.join(path, f"CNN_input_{prefix}_{wl}{ws}.pkl")
    with open(output_pkl_path, "wb") as file:
        pickle.dump(all_final_vectors, file)
    print(f"Data saved to {output_pkl_path}")

    with open(output_pkl_path, 'rb') as handle:
        X, pairs = pre_process_data(pickle.load(handle))

    model_path = pkg_resources.resource_filename('DeepLow', f'models/{model_name}')
    model = load_model(model_path)

    snp_counts = read_snp_counts(path)

    predictions = get_predictions(model, X)
    predictions = torch.tensor(softmax(predictions.numpy()))
    output_combined_path = os.path.join(path, f"Results_{output_prefix}.txt")
    save_predictions(predictions, pairs, snp_counts, output_combined_path)
    
    print("\nThank you for using the "" tool. If you have any questions or feedback, please reach out to us. Have a great day!")

if __name__ == "__main__":
    main()
