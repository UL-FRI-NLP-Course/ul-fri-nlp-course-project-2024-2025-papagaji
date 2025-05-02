from bs4 import BeautifulSoup
import pandas as pd 
import os
from os.path import isfile, join
import re
from datetime import timedelta
from datetime import datetime
from bs4 import BeautifulSoup
from prompts_and_responses import prompts_and_responses
from ara_2 import generate
import evaluate


excel_data_list,txt_data_list = prompts_and_responses()


#print(excel_data_list[0])
#print()
#print(txt_data_list[0])

predictions = []
for i in range(len(excel_data_list)):
    predictions.append(generate(excel_data_list[i]))

# TODO

metric = evaluate.load("rouge")

result = metric.compute(predictions=predictions, references=txt_data_list, use_stemmer=True)
result = {key: value * 100 for key, value in result.items()}
result = {k: round(v, 4) for k, v in result.items()}

print("Rezultati:",result)


# TODO

"""# Evaluate the model on validation and test sets
print(f"Evaluating model {model_name}")
val_results = trainer.evaluate()
test_results = trainer.predict(test_dataset=tokenized_datasets['test'])

print('Val results: ', val_results)
print('Test results:', test_results.metrics)"""