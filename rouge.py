from rouge_score import rouge_scorer
import numpy as np
import os

def getTxts(directory):
    dir = os.path.dirname(__file__) 
    dir = os.path.join(dir, directory)
    txts = []

    files = sorted(os.scandir(dir), key=lambda f: f.name)
    for file in files:
        txt_data = open(file,encoding="utf-16").read()
        txts.append(txt_data)
    return txts

def outputRougeScores(references, predictions):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL', 'rougeLsum'], use_stemmer=True)

    scores_accum = {
        'rouge1': {'p': [], 'r': [], 'f': []},
        'rouge2': {'p': [], 'r': [], 'f': []},
        'rougeL': {'p': [], 'r': [], 'f': []},
        'rougeLsum': {'p': [], 'r': [], 'f': []},
    }

    for pred, ref in zip(predictions, references):
        scores = scorer.score(ref, pred)
        for metric in scores:
            scores_accum[metric]['p'].append(scores[metric].precision)
            scores_accum[metric]['r'].append(scores[metric].recall)
            scores_accum[metric]['f'].append(scores[metric].fmeasure)

    scores = {
        metric: {
            'precision': np.mean(scores_accum[metric]['p']),
            'recall': np.mean(scores_accum[metric]['r']),
            'f1': np.mean(scores_accum[metric]['f']),
        }
        for metric in scores_accum
    }

    print("Metric  &  Precision & Recall & F1-Score \\\\")
    print(f"ROUGE1 & {scores['rouge1']['precision']:.4f} & {scores['rouge1']['recall']:.4f} & {scores['rouge1']['f1']:.4f} \\\\ \\hline")
    print(f"ROUGE2 & {scores['rouge2']['precision']:.4f} & {scores['rouge2']['recall']:.4f} & {scores['rouge2']['f1']:.4f} \\\\ \\hline")
    print(f"ROUGEL & {scores['rougeL']['precision']:.4f} & {scores['rougeL']['recall']:.4f} & {scores['rougeL']['f1']:.4f} \\\\ \\hline")
    print(f"ROUGELsum & {scores['rougeLsum']['precision']:.4f} & {scores['rougeLsum']['recall']:.4f} & {scores['rougeLsum']['f1']:.4f} \\\\ \\hline")
    return scores


references = getTxts("evalvacija/references/")
predictions = getTxts("evalvacija/predictions/")

outputRougeScores(references, predictions)
