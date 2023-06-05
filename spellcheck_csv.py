#august 11 2022 14:15
import os
import re
from textblob import TextBlob
import pandas as pd

def textblob_spellcheck(string):
    textblob_string = TextBlob(string)
    corrected_string = textblob_string.correct()
    return str(corrected_string)

def spellcheck(input_text): 
    return textblob_spellcheck(input_text)

def spellcheck_csv(csv_name): 
    df = pd.read_csv(csv_name)
    csv_name_no_extension = csv_name.replace(".csv", "")
    df["text"] = df["text"].apply(spellcheck)
    df.to_csv(csv_name_no_extension + "_spellcheck.csv")

if __name__ == '__main__':
	csv_name = "/home/mwolff3/csv_files/pop_cleaned_i_aug_03.csv"
	spellcheck_csv(csv_name)
