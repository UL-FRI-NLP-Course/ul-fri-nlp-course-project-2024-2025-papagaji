# Natural language processing course: Automatic generation of Slovenian traffic news for RTV Slovenija

This repository contains the implementation of the NLP project. Our task was to leverage prompt engineering techniques to generate short traffic reports for RTV Slovenija. We will also experiment with fine-tuning an LLM for this specific task in the future.

- report/report.pdf - report about our implementation of the project
- data/ - contains the data we used
- evalvacija/ - contains folders with data, generated predictions from the data and the reference reports
- ara_2.py - includes the prompt for generating reports on given data
- extract_data.py - converts .rtf files to .txt format
- vrabec.py - extracts the Excel data for a given time period
- rouge.py - calculates the score metrics for generated reports
- prompts_and_responses.py - generates predicted reports for reference reports in data/chosen_txts/, using relevant data. Results are written in data/results_txt/
- ft.py - TODO: will include the implementation of fine-tuning
