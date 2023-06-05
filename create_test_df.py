import pandas as pd 

path = "/home/mwolff3/csv_files/"
file_name = "pop_all_no_text_cleaned_dates_oct_24.csv"
df = pd.read_csv(path+file_name) 
test_df = df.head()
test_df.to_csv(path + "test_df.csv") 

