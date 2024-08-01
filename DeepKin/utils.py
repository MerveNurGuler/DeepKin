import numpy as np
import os
import glob

from DeepLow.mismatch_calculation import pad_nan

def combine_logs(prefix, sample_comb, path):
    norm_values = []
    sample_comb = np.array(sample_comb)
    file_pattern = os.path.join(path, '*{}.tmp'.format(prefix))
    files = glob.glob(file_pattern)
    snp_file = os.path.join(path, "SNP_counts.txt")
    pairs_gt = []
    with open(snp_file, 'r') as file:
        for line in file:
            columns = line.strip().split('\t')
            if len(columns) >= 2:
                pair_name, snp_count = columns[0], columns[1]
                try:
                    count = int(snp_count)
                    if count >= 2000:
                        pairs_gt.append(pair_name)
                except ValueError:
                    pass
    for i in range(1, 23):
        combined_msm = []
        for file in files:
            loaded_data = np.loadtxt(file, delimiter='\t', dtype=list)
            chr = loaded_data[i - 1]
            combined_msm.append(chr)
        combined_msm = pad_nan(combined_msm)
        transposed_data = np.array(combined_msm).T
        transposed_data = np.vstack((sample_comb, transposed_data))
        chr_filename = os.path.join(path, 'chr{}-{}.log'.format(i, prefix))
        np.savetxt(chr_filename, transposed_data, delimiter='\t', fmt='%s')
        indices_to_extract = []
        for idx, id in enumerate(transposed_data[0]):
            if id in pairs_gt:
                indices_to_extract.append(idx)
        extracted_data = transposed_data[:, indices_to_extract]
        norm_value = np.nanmedian(extracted_data[1:].astype(float), axis=0)
        norm_value = np.nanmedian(norm_value)
        norm_values.append(norm_value)
    write_norm(norm_values, path)
    for file in files:
        os.remove(file)


def write_norm(norm_values, path):
    norm_values = np.array(norm_values).reshape(-1, 1)
    chr_ids = np.arange(1, 23, dtype=int).reshape(-1, 1)
    norm_values = np.hstack((chr_ids, norm_values))
    header = 'chr\tmedian'
    norm_name = os.path.join(path, 'normalization_values.txt')
    np.savetxt(norm_name, norm_values, delimiter='\t', fmt=['%d', '%.6f'], header=header, comments='')


def add_row_numbers_to_logs(prefix, path):
    for i in range(1, 23):
        chr_filename = os.path.join(path, 'chr{}-{}.log'.format(i, prefix))
        with open(chr_filename, 'r') as file:
            lines = file.readlines()
        lines[0] = '#Window\t' + lines[0]
        for j in range(1, len(lines)):
            lines[j] = str(j) + '\t' + lines[j].rstrip('\n') + '\n'
        with open(chr_filename, 'w') as file:
            file.writelines(lines)

def remove_nan_rows(prefix, path):
    for i in range(1, 23):
        chr_filename = os.path.join(path, 'chr{}-{}.log'.format(i, prefix))
        if os.path.exists(chr_filename):
            with open(chr_filename, 'r') as file:
                lines = file.readlines()
            with open(chr_filename, 'w') as file:
                for line in lines:
                    elements = line.strip().split('\t')
                    if all(element.lower() == 'nan' for element in elements[1:]):
                        continue
                    file.write(line)

def process_log_files(path, prefix, n_Sample, custom_norm=None):
    boundaries = [-0.51, 1.51]
    xs = 10
    ys = 10
    n_Pairs = (n_Sample * (n_Sample - 1)) // 2
    norm = "normalization_values.txt"
    norm_file = os.path.join(path, norm)
    print("The CNN inputs have being generated...")
    i_range = range(1, (n_Pairs + 1))
    j_range = range(1, 23)
    try:
        norm_values = []
        with open(norm_file) as file:
            lines = file.readlines()
        for line in lines[1:]:
            tmp = line.strip().split('\t')
            norm_values.append(float(tmp[1]))
        all_final_vectors = {}
        for i in i_range:
            all_final_vectors[i] = {}
            for j in j_range:
                data_vectors = {}
                filename = f"chr{j}-{prefix}.log"
                filepath = os.path.join(path, filename)
                try:
                    with open(filepath) as file:
                        lines = file.readlines()
                        header = lines[0].strip().split('\t')
                        pair = header[i]
                        data_vectors[pair] = []
                        for line in lines[1:]:
                            tmp = line.strip().split('\t')
                            value = tmp[i]
                            if value.lower() != 'nan':
                                data_vectors[pair].append(float(value))
                    for pair in data_vectors:
                        data_vectors[pair] = np.asarray(data_vectors[pair])
                        if custom_norm is not None:
                            norm_val = custom_norm
                        else:
                            norm_val = norm_values[j - 1]
                        data_vectors[pair] = 2 * (1 - (data_vectors[pair] / norm_val))
                        data_vectors[pair] = np.where(data_vectors[pair] < -0.5, -0.5, data_vectors[pair])
                        data_vectors[pair] = np.where(data_vectors[pair] > 1.5, 1.5, data_vectors[pair])
                    right = len(next(iter(data_vectors.values()))) / xs
                    down = (boundaries[1] - boundaries[0]) / ys
                    final_vectors = {}
                    for pair in data_vectors:
                        final_vectors[pair] = np.zeros(10 * 10)
                    for pair in data_vectors:
                        for m in range(0, len(data_vectors[pair])):
                            if boundaries[0] < data_vectors[pair][m] < boundaries[1]:
                                final_vectors[pair][int((boundaries[1] - data_vectors[pair][m]) / down) * 10 + int(m / right)] += 1
                    all_final_vectors[i][j] = final_vectors
                except FileNotFoundError:
                    print(f"File {filename} not found.")
    except FileNotFoundError as e:
        print(f"File {norm_file} not found: {e}")
    print("The CNN inputs have been generated.")
    return all_final_vectors
