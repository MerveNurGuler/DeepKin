import numpy as np

def pre_process_file(ped_file_path):
    num_individuals = 0
    line_offsets = []
    try:
        with open(ped_file_path, 'rb') as file:
            print('Reading the ped file...')
            offset = 0
            for line in file:
                line_offsets.append(offset)
                offset += len(line)
                num_individuals += 1
        print('File has been read successfully.')
        print(f'{num_individuals} individuals have been found.')
        return num_individuals, line_offsets
    except FileNotFoundError:
        print(f"Error: File '{ped_file_path}' not found.")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def find_chromosome_ranges(map_file_path):
    chromosome_ranges = {}
    current_chromosome = None
    start_line = None
    with open(map_file_path, 'r') as file:
        for line_number, line in enumerate(file):
            parts = line.strip().split()
            chromosome = parts[0]
            if chromosome != current_chromosome:
                if current_chromosome is not None:
                    chromosome_ranges[current_chromosome] = (start_line, line_number - 1)
                start_line = line_number
                current_chromosome = chromosome
    if current_chromosome is not None:
        chromosome_ranges[current_chromosome] = (start_line, line_number)
    return chromosome_ranges

def read_ith_row(i, ped_file_path, line_offsets):
    with open(ped_file_path, 'rb') as file:
        file.seek(line_offsets[i])
        line = file.readline().decode('utf-8').strip().split()
        return line

def remove_zeros(individual1_data, individual2_data):
    individual1_data = np.array(individual1_data)
    individual2_data = np.array(individual2_data)
    individual1_data_str = individual1_data.astype(str)
    individual2_data_str = individual2_data.astype(str)
    non_zero_indices = np.logical_and(individual1_data_str != '0', individual2_data_str != '0')
    individual1_data_filtered = individual1_data[non_zero_indices]
    individual2_data_filtered = individual2_data[non_zero_indices]
    return individual1_data_filtered, individual2_data_filtered
