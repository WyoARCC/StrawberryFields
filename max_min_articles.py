import pandas as pd

directory = "/home/mwolff3/csv_files/"  
csv = "final_pop_text_nov_05.csv"
df = pd.read_csv(directory + csv)

bkgd = ((df["beatles"] == 0) & (df["strawberry_fields"] == 0))
bkgd_df = df[bkgd]
        
beatles = ((df["beatles"] == 1))
beatles_df = df[beatles]
        
sf_beat = ((df["beatles"] == 1) & (df["strawberry_fields"] == 1))
sf_beat_df = df[sf_beat] 
    
columns = ["textblob_polarity_r", "textblob_subjectivity_r", "vader_analysis_r",  "swn_analysis_r"]
dfs = {"bkgd" : bkgd_df, "beatles" : beatles_df, "sf" : sf_beat_df}
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

for j in range(0, 11): 
    for name in dfs:
        for i in columns: 
                dframe = dfs[name]
                dframe_filter = (dframe["date_segment"] == j)
                dframe = dframe[dframe_filter]
                sorted_by_value = dframe.sort_values(by=i)
                minimums = sorted_by_value.head(5)
                maximums = sorted_by_value.tail(5)
                datestring = ""
                if j == 0: 
                    datestring = "for dates before 1960-08-12"
                elif j < 10: 
                    datestring = "for dates between" + dates[j-1] + "and " + dates[j]
                else: 
                    datestring = "for dates after 1985-10-09"
                print("lowest rated articles for " + i + "in dataset" + name + "for dates" + datestring)
                print(list(minimums["text"]))
                print("-----")
                print("highest rated articles for " + i + "in dataset" + name + "for dates" + datestring)
                print(list(maximums["text"]))
                print("----------")
                

