# Natural language processing course: Automatic generation of Slovenian traffic news for RTV Slovenija

This repository contains the implementation of the NLP project. Our task was to leverage prompt engineering techniques to generate short traffic reports for RTV Slovenija. We also experimented with fine-tuning an LLM for this task.

- report/report.pdf - report about our implementation of the project
- data/ - contains the data we used
- evalvacija/ - contains folders with data, generated predictions from the data and the reference reports
- ara_2.py - includes the prompt for generating reports on given data
- extract_data.py - converts .rtf files to .txt format
- vrabec.py - extracts the Excel data for a given time period
- rouge.py - calculates the score metrics for generated reports
- prompts_and_responses.py - generates predicted reports for reference reports in data/chosen_txts/, using relevant data. Results are written in data/results_txt/
- ft.py - TODO: will include the implementation of fine-tuning

# Running the code

- First, download the data available at [link](https://unilj-my.sharepoint.com/personal/slavkozitnik_fri1_uni-lj_si/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fslavkozitnik%5Ffri1%5Funi%2Dlj%5Fsi%2FDocuments%2FPredmeti%2FONJ%2FONJ%5F2025%5FSpring%2FProjects%2FRTVSlo%2Ezip&parent=%2Fpersonal%2Fslavkozitnik%5Ffri1%5Funi%2Dlj%5Fsi%2FDocuments%2FPredmeti%2FONJ%2FONJ%5F2025%5FSpring%2FProjects&ga=1) and put the contents into the data folder. The path should look like: data/RTVSlo.
- Then run the script extract_data.py, this will convert all reference reports in data from .rtf to .txt format. The converted files are then put into a new folder data/txts.
- TODO Generating reports with the prompt engineering method: choose the reference reports from the data/txts folder, for which you want to generate new reports. The date and time will be read from the names of the files, which is then used to automatically retrieve relevant data from the excel table. This data is then used to generate new reports, which are then saved in the generate_responses_prompt_engineering/results_txts folder. The data, which was used to generate is also saved in the generate_responses_prompt_engineering/inputs folder.
