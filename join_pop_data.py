import pandas as pd
path = "/home/mwolff3/csv_files/"
pd.options.display.max_columns = None
pd.options.display.max_rows = 20

'''pop_i_df = pd.read_csv(root_path + "pop_cleaned_i_aug_22_sept_08.csv")
print(pop_i_df.loc[pop_i_df['swn_analysis'] > 0])
print(pop_i_df.head())
print(pop_i_df.columns)
print("1")
pop_ii_df = pd.read_csv(root_path + "pop_cleaned_ii_aug_22_sept_08.csv")
print(pop_ii_df.loc[pop_ii_df['swn_analysis'] > 0])
print(pop_ii_df.head())
print(pop_ii_df.columns)
print("2")
pop_df = pd.concat([pop_i_df, pop_ii_df], ignore_index=True, sort=False)
print(pop_df.head())
print(pop_df.columns)
print("3")
#pop_df.to_csv(root_path + "pop_all_sentiment_oct_23.csv")
print("4")'''
'''pop_df = pd.read_csv(root_path + "pop_all_sentiment_oct_23.csv", encoding = "utf-8")
docu_df = pd.read_csv(root_path + "pop_oct_23.csv", encoding = "utf-8")
pop_df = pop_df[["textblob_polarity", 'textblob_subjectivity', 'vader_analysis','swn_analysis', "text", "date", "title"]]
docu_df = docu_df[["text", "doc"]]

pop_df.text = pop_df.text.astype(str)
docu_df.text = docu_df.text.astype(str)
pop_df.text= pop_df.text.apply(str).str.strip()
docu_df.text = docu_df.text.apply(str).str.strip()
docu_df.text = docu_df.text.str.replace(",", "")

print(pop_df.head(20))
print(docu_df.head(20))


new_df = docu_df.merge(pop_df, how='inner', on = 'text')
#print(new_df.loc[new_df['swn_analysis'] > 0])
print(new_df.head())
print(new_df.columns)

#new_df = new_df.drop(columns = ['Unnamed: 0_x', 'title_x', 'date_x', '6', 'Unnamed: 0_y', 'doc_2', 'doc_3'])
new_df.to_csv(root_path + "pop_all_text_oct_23.csv")
new_df = new_df.drop(columns = ["text"])
new_df.to_csv(root_path + "pop_all_no_text_oct_23.csv")
print(new_df.head())
print(new_df.columns)
'''
'''def sort_csv_by_date(df): 
    df["date"] = pd.to_datetime(df["date"], errors = 'coerce')
    df = df.dropna(subset = ["date"])
    df.sort_values(by='date', inplace=True)
    return df

df1 = pd.read_csv(path + "pop_all_text_oct_23.csv")
df2 = pd.read_csv(path + "pop_all_no_text_date_content_segments_oct_29.csv")
df3 = df1.join(df2, lsuffix = "_l", rsuffix = "_r")
df3["date"] = df3["date_r"]
df3 = sort_csv_by_date(df3) 
df3.to_csv(path + "final_pop_text_nov_05.csv")

'''
df = pd.read_csv(path + "final_pop_text_nov_05.csv")
df = df.drop(columns = ["Unnamed: 0_l", "doc_l","textblob_polarity_l","textblob_subjectivity_l","vader_analysis_l","swn_analysis_l","date_l","title_l","Unnamed: 0.6","Unnamed: 0.5","Unnamed: 0.4","Unnamed: 0.3","Unnamed: 0.2","Unnamed: 0.1","Unnamed: 0_r"])
df.to_csv(path + "final_pop_text_nov_05.csv")
'''df["doc"] = df["doc_r"]
df["textblob_polarity" = "textblob_polarity_r"]
df["textblob_subjectivity_r,vader_analysis_r,swn_analysis_r,date_r,title_r,date_segment,beatles,strawberry_fields,date,text
'''






