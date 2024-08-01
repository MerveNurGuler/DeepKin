import torch
import time
import os
import numpy as np

from DeepLow.cnn_model import CNN, pre_process_data

label_map = {
    0: "2nd degree",
    1: "3rd degree",
    2: "Parent-Offspring",
    3: "Sibling",
    4: "Identical",
    5: "Unrelated"
}

def load_model(model_path):
    model = CNN()
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

def get_predictions(model, X):
    start_time = time.perf_counter()
    with torch.no_grad():
        predictions = model(X)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)
    return predictions

def softmax(x):
    e_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return e_x / e_x.sum(axis=1, keepdims=True)

def save_predictions(predictions, pairs, snp_counts, output_combined_path):
    _, predicted_labels = torch.max(predictions, 1)
    predicted_labels_list = predicted_labels.tolist()
    mapped_labels = list(map(lambda x: label_map[x], predicted_labels_list))
    with open(output_combined_path, 'w') as file:
        file.write("Pair\tSNP_count\tPredicted_relatedness\tPred_score_2nd\tPred_score_3rd\tPred_score_Paroff\tPred_score_Sib\tPred_score_Identical\tPred_score_Unrelated\n")
        for pair, snp_count, label, row in zip(pairs, map(snp_counts.get, pairs), mapped_labels, predictions):
            predictions_str = '\t'.join(map(str, row.numpy()))
            file.write(f"{pair}\t{snp_count}\t{label}\t{predictions_str}\n")
    print(f"Output saved to {output_combined_path}")

def read_snp_counts(path):
    snp_counts = {}
    snp_counts_file = os.path.join(path, 'SNP_counts.txt')
    with open(snp_counts_file, 'r') as file:
        for line in file:
            pair, count = line.strip().split('\t')
            snp_counts[pair] = count
    return snp_counts
