import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import ttest_ind

pd.options.display.max_rows = 20

image_path = "/home/mwolff3/images/"
columns = ["textblob_polarity", "textblob_subjectivity", "vader_analysis",  "swn_analysis"]
value_dict = {"swn_analysis":"SentiWordNet valence", 
    "textblob_polarity":"TextBlob polarity", 
    "textblob_subjectivity":"TextBlob subjectivity", 
    "vader_analysis":"VADER valence"}
dates = ["1960-08-12", 
        "1962-10-17", 
        "1964-02-09", 
        "1966-07-29", 
        "1966-08-29", 
        "1967-02-17", 
        "1970-04-10", 
        "1980-12-08", 
        "1981-08-31", "1985-10-09", "1986-01-01"]
pd_dates = [pd.to_datetime(date) for date in dates]

def statistics(df):
    df = df[columns]
    print(df.describe())
    '''print("maximums\n")
    for analysis_column in columns:
        print(analysis_column + "\n")
        #print(df.iloc[df[analysis_column].idxmax()])
        maximum_value = df[analysis_column].max()
        print(maximum_value)
        all_results = df.loc[df[analysis_column] == maximum_value, 'title']
        for result in all_results:
            print(result)
        #print(df.loc[df[analysis_column] == maximum_value, 'title'].item())
    print("minimums\n")
    for analysis_column in columns:
        print(analysis_column + "\n")
        #print(df.iloc[df[analysis_column].idxmin()])
        minimum_value = df[analysis_column].min()
        #print(df.loc[df[analysis_column] == minimum_value, 'title'].item())
        print(minimum_value)
        all_results = df.loc[df[analysis_column] == minimum_value, 'title']
        for result in all_results:
            print(result)'''
#input: dataframe (assuming bkgd, beatles, or sf) and column
#output: returns a list of date segments that differ in a statistically significant way from the subsequent date
def time_t_test(df, column):
    stat_sig_segments = []
    for j in range(0, 10): 
        k = j + 1
        dframe_filter_1 = (df["date_segment"] == j)
        dframe_filter_2 = (df["date_segment"] == k)
        dframe_1 = df[dframe_filter_1]
        dframe_2 = df[dframe_filter_2]
        results = ttest_ind(dframe_1[column], dframe_2[column], equal_var=False)
        if results.pvalue < 0.01: 
            stat_sig_segments.append(j)
        print(len(dframe_1), len(dframe_2), results.pvalue, results.statistic, i, j, k, "\n")
        
    return(stat_sig_segments)
    
#input: dataframe, column
#output: list of means at each date segment
def date_segment_means(df, column): 
    means = []
    for j in range(0, 11):
        dframe_filter = (df["date_segment"] == j)
        dframe_new = df[dframe_filter]
        means.append(dframe_new[column].mean())
    print(means)
    return(means)

#input: dataframe labeled with binary encoding for beatles and sf
#output: returns bkgd, beatles, and sf + beatles data frames in a dictionary with the corresponding labels 
def get_separate_dfs(df): 
    bkgd = ((df["beatles"] == 0) & (df["strawberry_fields"] == 0))
    bkgd_df = df[bkgd] 
    
    beatles = ((df["beatles"] == 1))
    beatles_df = df[beatles]
        
    sf_beat = ((df["beatles"] == 1) & (df["strawberry_fields"] == 1))
    sf_beat_df = df[sf_beat] 
    
    dfs = {"bkgd" : bkgd_df, "beatles" : beatles_df, "sf" : sf_beat_df}
    return dfs   

#input: dataframe, column, list of stat. sig. date segments, list of means at all dates
#output: saves a plot with the means as a scatterplot 
def means_plot(df_name, column, means, stat_sig_segments, color = "dark"): 
    facecolor, contrast_color, marker_color = None, None, None
    if color == "dark": 
        facecolor = "#202729"
        contrast_color = "white"
        marker_color = "#FF5252"
    else: 
        facecolor = "white"
        contrast_color = "black"
        marker_color =  "red"
    
    plt.figure(facecolor=facecolor)
    plt.rcParams.update({'text.color': contrast_color,
                     'axes.labelcolor': contrast_color})
                
    fig, ax = plt.subplots()
    
    ax.set_facecolor(facecolor)
    fig.set_facecolor(facecolor)
    
    
    plt.plot(pd_dates, means, linewidth = 1, color = contrast_color)
    for s in stat_sig_segments:  
        plt.scatter(pd_dates[s], means[s], color = marker_color)#, marker = 'o')
    
    plt.xticks(rotation=45,horizontalalignment='right',fontweight='light', fontsize='x-small')
    plt.xlim(pd.to_datetime("1960-01-01"), pd.to_datetime("1986-01-01"))
    
    ax.set(xlabel = "Date", ylabel = value_dict[column] , title = 
    "Changes in mean " + value_dict[column] + " over time")
    ax.spines.top.set_color(contrast_color)
    ax.spines.bottom.set_color(contrast_color)
    ax.spines.left.set_color(contrast_color)
    ax.spines.right.set_color(contrast_color)
    ax.xaxis.label.set_color(contrast_color)
    ax.tick_params(axis='x', colors=contrast_color)
    ax.yaxis.label.set_color(contrast_color)
    
    plt.savefig(image_path + df_name + column + "_means_dec_18.png")               
        
def time_t_test_output(len_1, len_2, name, results, i, j, k): 
    #output_string = ""
    print(len_1, len_2, name, results.pvalue, results.statistic, i, j, k)
    print("\n")
    #if results.pvalue < 0.01: 
    #    output_string = "statistically significant difference in sentiment analysis method " + str(i) + " for" + date_encoding(j) + "[" + str(len_1) + "articles] and " + date_encoding(k) + "[" + str(len_2) + "articles] in dataset " + name 
    #    if results.statistic > 0: 
    #        output_string += "first date range more positive" 
    #return output_string
def date_encoding(date_num): 
    dates = ["1960-08-12", 
        "1962-10-17", 
        "1964-02-09", 
        "1966-07-29", 
        "1966-08-29", 
        "1967-02-17", 
        "1970-04-10", 
        "1980-12-08", 
        "1981-08-31", "1985-10-09"]
    output_string = ""
    if date_num == 0: 
        output_string += " dates before 1960-08-12 "
    elif date_num < 10: 
        output_string += " dates between " + dates[date_num-1] + " and " + dates[date_num]
    else: 
        output_string += " dates after 1985-10-09" 
    return output_string
def bkgd_t_test(df):  
    from scipy.stats import ttest_ind
    bkgd = ((df["beatles"] == 0) & (df["strawberry_fields"] == 0))
    bkgd_df = df[bkgd]
        
    beatles = ((df["beatles"] == 1))
    beatles_df = df[beatles]
        
    sf_beat = ((df["beatles"] == 1) & (df["strawberry_fields"] == 1))
    sf_beat_df = df[sf_beat] 
    
    columns = ["textblob_polarity", "textblob_subjectivity", "vader_analysis",  "swn_analysis"]
    dfs = [bkgd_df, beatles_df, sf_beat_df]
    df_names = ["bkgd", "beatles", "sf"]
    for i in columns: 
        for j in range(0, 11): 
            temp_dfs = []
            for df in dfs: 
                temp_dfs.append(date_filter(df, j))
            for k in range(0, 2): 
                for m in range(k+1, 2): 
                    if len(temp_dfs[k]) > 100 and len(temp_dfs[m]) > 100: 
                        ttest_results = ttest_ind(temp_dfs[k][i], temp_dfs[m][i], equal_var = False)
                        p = ttest_results.pvalue
                        if (p < 0.01) and (p is not None):
                            output_string = ""
                            t_test_string = t_test_output(df_names[k], str(len(temp_dfs[k])), df_names[m], str(len(temp_dfs[m])), i, str(p), ttest_results.statistic, j)
                            output_string += "statistically significant difference between " + t_test_string
                            print(output_string)
                            
        print("----")
    print("---------")
def t_test_output(df_a, df_a_len, df_b, df_b_len, column, p, stat, date_num): 
    dates = ["1960-08-12", 
        "1962-10-17", 
        "1964-02-09", 
        "1966-07-29", 
        "1966-08-29", 
        "1967-02-17", 
        "1970-04-10", 
        "1980-12-08", 
        "1981-08-31", "1985-10-09"]
    output_string = df_a + " with " + df_a_len + " articles and " + df_b + " with " + df_b_len + " articles in sentiment analysis method " + column + " at p = " + p
    if date_num == 0: 
        output_string += " for dates before 1960-08-12 "
    elif date_num < 10: 
        output_string += " for dates between " + dates[date_num-1] + " and " + dates[date_num]
    else: 
        output_string += " for dates after 1985-10-09" 
    if stat > 0: 
        output_string += df_a + " more positive than " + df_b
    else: 
        output_string += df_b + " more positive than " + df_a
    return output_string
                                
def date_filter(df, date): 
    df_filter = (df["date_segment"] == date)
    df_temp = df[df_filter]
    return df_temp
 
def print_summary_statistics(df): 
    for i in [0, 1]: 
        for j in [0, 1]:
            for k in range(0, 11):
                subset = ((df["beatles"] == i) & (df["strawberry_fields"] == j) & (df["date_segment"] == k))
                df_temp = df[subset]
                df_temp = df_temp[["textblob_polarity", "textblob_subjectivity", "vader_analysis",  "swn_analysis", "title"]]
                print("beatles: " + str(i) + " sf: " + str(j) + " date range: " + str(k))
                print(df_temp.describe()) 
                print("\n")
def two_way_anova(df): 
    import statsmodels.api as sm
    from statsmodels.formula.api import ols
    columns = ["textblob_polarity", "textblob_subjectivity", "vader_analysis",  "swn_analysis"]
    for k in columns: 
    # Performing two-way ANOVA
        model = ols(k + ' ~ C(beatles) + C(strawberry_fields) + C(date_segment) + C(beatles):C(strawberry_fields) + C(beatles):C(date_segment) + C(date_segment):C(strawberry_fields) + C(date_segment):C(beatles):C(strawberry_fields)', data=df).fit()
        result = sm.stats.anova_lm(model, type=2)
        print(k)
        print("\n")
        print(result)
          
    # Print the result
  
        
if __name__ == '__main__':
    '''csv_list = ["nyt_cleaned_data_aug_03.csv_no_text.csv", "pop_cleaned_i_beatles_fuzzy_aug_15_no_text_cleaned_dates.csv", "pop_cleaned_ii_beatles_fuzzy_aug_15_no_text_cleaned_dates.csv"]

    directory = "/home/mwolff3/csv_files/"
    for csv in csv_list: 
        print(csv)
        statistics(pd.read_csv(directory + csv))
    '''
    directory = "/home/mwolff3/csv_files/"  
    csv = "pop_all_no_text_date_content_segments_oct_29.csv"
    df = pd.read_csv(directory + csv)
    #print_summary_statistics(df) 
    #two_way_anova(df)
    #bkgd_t_test(df)
    #time_t_test(df)
    #means(df)
    
    dfs = get_separate_dfs(df)
    for i in ["bkgd", "beatles", "sf"]: 
        print(i)
        for j in range(0, 11):
            print(j)
            df = dfs[i]
            dframe_filter = (df["date_segment"] == j)
            dframe_new = df[dframe_filter]
            statistics(dframe_new)
        #for j in columns: 
            #means = date_segment_means(dfs[i], j)
            #for mean in means: 
            #    statistics(mean)
            #print(i)
            #stat_sig_segments = time_t_test(dfs[i], j)
            #means_plot(i, j, means, stat_sig_segments, color = "light")
            
    
