import numpy as np
import os

from deep_mismatch.data_processing import read_ith_row, remove_zeros

def mismatch_calc_ind(i1, i2, chr_ranges, wl, ws):
    individual1_data, individual2_data = i1[6::2], i2[6::2]
    mis_match_for_chr = []
    snp_count_total = 0
    for i in range(1, 23):
        mis_match_vals = []
        start, end = chr_ranges[str(i)]
        individual1_data_chr = individual1_data[start:end]
        individual2_data_chr = individual2_data[start:end]
        individual1_data_chr, individual2_data_chr = remove_zeros(individual1_data_chr, individual2_data_chr)
        snp_count_total += (len(individual1_data_chr) + 1)
        last_read_idx = 0
        length_ind = len(individual1_data_chr)
        while(last_read_idx < length_ind):
            remaining_length = length_ind - last_read_idx
            if remaining_length < wl:
                individual1_data_window = individual1_data_chr[last_read_idx:]
                individual2_data_window = individual2_data_chr[last_read_idx:]
                window_length = remaining_length
            else:
                individual1_data_window = individual1_data_chr[last_read_idx:last_read_idx + wl]
                individual2_data_window = individual2_data_chr[last_read_idx:last_read_idx + wl]
                window_length = wl
            mismatch = np.sum(individual1_data_window != individual2_data_window) / window_length
            mis_match_vals.append(mismatch)
            last_read_idx += ws
            if remaining_length < wl:
                break
        mis_match_for_chr.append(mis_match_vals)
    return mis_match_for_chr, snp_count_total

def pad_nan(combined_msm):
    max_length = max(len(row) for row in combined_msm)
    padded_arrays = np.full((len(combined_msm), max_length), np.nan)
    for i, row in enumerate(combined_msm):
        padded_arrays[i, :len(row)] = row
    np.set_printoptions(suppress=True)
    return padded_arrays

def write_to_file(ind1, ind2, mis_match_for_chr, prefix, path):
    file_name = ind1[1] + '_' + ind2[1] + '_' + prefix + '.tmp'
    file = os.path.join(path, file_name)
    padded_arrays = pad_nan(mis_match_for_chr)
    np.savetxt(file, padded_arrays, delimiter='\t', fmt='%1.3f')

def take_combs(num_individuals, prefix, path, chr_ranges, ped_file_path, line_offsets, wl, ws):
    sample_names = []
    sample_comb = []
    snp_counts_file = os.path.join(path, 'SNP_counts.txt')
    with open(snp_counts_file, 'w') as file:
        for i1 in range(num_individuals):
            ind1 = read_ith_row(i1, ped_file_path, line_offsets)
            ind1_name = ind1[1]
            for i2 in range(i1 + 1, num_individuals):
                ind2 = read_ith_row(i2, ped_file_path, line_offsets)
                ind2_name = ind2[1]
                mis_match_for_chr, SNP_counts = mismatch_calc_ind(ind1, ind2, chr_ranges, wl, ws)
                sample_names = '{}-{}'.format(ind1_name, ind2_name)
                sample_comb.append(sample_names)
                file.write(f"{ind1_name}-{ind2_name}\t{SNP_counts}\n")
                write_to_file(ind1, ind2, mis_match_for_chr, prefix, path)
    return sample_comb
