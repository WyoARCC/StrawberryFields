import pandas as pd
root_path = "/home/mwolff3/csv_files/"
new_df = pd.read_csv(root_path + "pop_all_no_text_oct_23.csv")
print(new_df.head())
print(new_df.columns)
new_df = new_df.drop(columns = ['Unnamed: 0', 'Unnamed: 0_x', 'title_x', 'date_x', '6', 'Unnamed: 0.1', 'Unnamed: 0_y', 'doc_2', 'doc_3'])
print(new_df.loc[new_df['swn_analysis'] > 0])

