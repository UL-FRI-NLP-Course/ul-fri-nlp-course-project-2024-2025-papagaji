import os
from sentence_transformers import SentenceTransformer
from scipy.spatial import distance


dir = os.path.dirname(__file__) 
inputs = os.path.join(dir, "fine_tuning_training/excel_data/")
references = os.path.join(dir, "fine_tuning_training/references/")
matched_inputs = os.path.join(dir, "fine_tuning_training/matched_data/")
matched_references = os.path.join(dir, "fine_tuning_training/matched_references/")

input_files_lines = []
references_files_lines = []

for subdir, dirs, files in os.walk(inputs):

    for file_path in sorted(files):

        input_files_lines.append([])

        with open(inputs + file_path,"r", encoding="utf-16") as file:
            for line in file:
                if(len(line) > 5):
                    input_files_lines[len(input_files_lines)-1].append(line.strip("\n"))

    print(input_files_lines)

for subdir, dirs, files in os.walk(references):

    for file_path in sorted(files):

        references_files_lines.append([])

        with open(references + file_path,"r", encoding="utf-16") as file:
            for line in file:
                if(len(line) > 5):
                    references_files_lines[len(references_files_lines)-1].append(line.strip("\n"))

    print(references_files_lines)

#check if inputs and references are of same length(same number of files in respective folders)

for k in range(len(input_files_lines)):

    output_file_inputs = ""
    output_file_inputs += input_files_lines[k][0] + "\n"
    output_file_inputs += input_files_lines[k][1] + "\n"
    input_files_lines[k].pop(0)
    input_files_lines[k].pop(0)

    output_file_references = ""
    output_file_references += references_files_lines[k][0] + "\n"
    references_files_lines[k].pop(0)


    model = SentenceTransformer('all-MiniLM-L6-v2')
    inputs_sentence_embeddings = model.encode(input_files_lines[k])
    references_sentence_embeddings = model.encode(references_files_lines[k])


    # IMPORTANT: set better threshold
    threshold = 0.63
    for i in range(len(inputs_sentence_embeddings)):

        highest_similarity = 0
        for j in range(len(references_sentence_embeddings)):

            print("input:",input_files_lines[k][i],"\noutput:",references_files_lines[k][j],"\nsimilarity:",1 - distance.cosine(inputs_sentence_embeddings[i], references_sentence_embeddings[j]))
            print()

            if(1-distance.cosine(inputs_sentence_embeddings[i], references_sentence_embeddings[j]) > highest_similarity):
                highest_similarity = 1-distance.cosine(inputs_sentence_embeddings[i], references_sentence_embeddings[j])
                print(k,j)
                best_match = references_files_lines[k][j]

        if(highest_similarity >= threshold):
            output_file_inputs += input_files_lines[k][i] + "\n"
            output_file_references += "\n" + best_match + "\n"




    with open(matched_inputs + str(k) + ".txt", "w",encoding="utf-16") as file:
        file.write(output_file_inputs)

    with open(matched_references + str(k) + ".txt", "w",encoding="utf-16") as file:
        file.write(output_file_references)
