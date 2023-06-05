import pandas as pd

def drop_text(csv_name):
    dataframe = pd.read_csv(csv_name)
    dataframe = dataframe.drop(columns = ["text"])
    dataframe.to_csv(csv_name + "_no_text.csv")

'''csv_list = ["nyt_cleaned_spellcheck_data_aug_03.csv", 
             "pop_cleaned_ii_beatles_fuzzy_aug_15.csv", 
             "pop_cleaned_i_beatles_fuzzy_aug_15.csv",
             "nyt_cleaned_data_aug_03.csv"]
'''
csv_list = ["pop_cleaned_i_aug_22_sept_08.csv", "pop_cleaned_ii_aug_22_sept_08.csv"]
directory = "/home/mwolff3/csv_files/"
for csv in csv_list: 
	drop_text(directory + csv)
	

