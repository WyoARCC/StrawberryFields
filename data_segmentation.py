import pandas as pd
import fuzzysearch
from fuzzysearch import find_near_matches
from datetime import datetime

def date_segmentation(date): 
    dates = ["1960-08-12", 
        "1962-10-17", 
        "1964-02-09", 
        "1966-07-29", 
        "1966-08-29", 
        "1967-02-17", 
        "1970-04-10", 
        "1980-12-08", 
        "1981-08-31",
        "1985-10-09"]
    counter = 0
    
    
    
    for d in dates: 
        d2 = datetime.strptime(d, '%Y-%m-%d')
        if date < d2: 
            return counter
        counter+=1
    return 10
    
def beatles(text): 
    matches = find_near_matches('beatles', text, max_l_dist = 2)
    if len(matches) > 0: 
        return 1
    return 0
def strawberry_fields(text):
    matches = find_near_matches('strawberry field', text, max_l_dist= 2)
    if len(matches) > 0: 
        return 1
    return 0
        
path = "/home/mwolff3/csv_files/"
file_name = "pop_all_no_text_fixed_dates_oct_25.csv"
df = pd.read_csv(path+file_name) 
df['date'] = pd.to_datetime(df['date'])  
df["date_segment"] = df["date"].apply(date_segmentation)
df.to_csv(path + "pop_all_no_text_date_segments_oct_29.csv") 

'''df1 = pd.read_csv(path + "pop_all_text_oct_23.csv")
df1["beatles"] = df1["text"].apply(beatles)
df1["strawberry_fields"] = df1["text"].apply(strawberry_fields)
'''
df2 = pd.read_csv(path + "pop_all_no_text_date_content_segments_oct_24.csv")
df["beatles"] = df2["beatles"] 
df["strawberry_fields"] = df2["strawberry_fields"]
df.to_csv(path + "pop_all_no_text_date_content_segments_oct_29.csv")











