#august 11 2022 13:52, 14:38
#sept 21 2022 17:54

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import wordcloud
from wordcloud import WordCloud, STOPWORDS

image_path = "/home/mwolff3/images/"

stopwords = set(STOPWORDS)


def annot_max(x,y, xmax, ymax, max_value_title, ax=None):
    text = str(xmax) + "\n" + str(max_value_title)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props)
    ax.annotate(text, xy=(xmax, ymax), xytext=(0.2, 0.8), **kw)
def annot_min(x,y, xmin, ymin, min_value_title, ax=None):
    text = str(xmin) + "\n" + str(min_value_title)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props)
    ax.annotate(text, xy=(xmin, ymin), xytext=(0.6, 0.2), **kw)

def plot(value_to_plot, df, dataset_label, today, plot_dates = True):
    plt.figure()
    fig, ax = plt.subplots()
    x = df["date"]
    y = df[value_to_plot]
    
    plt.plot(x, y)
   
    ymax = y.max()
    ymin = y.min()
    max_value_title = df.loc[y.idxmax(), 'title']
    xmax = df.loc[y.idxmax(), 'date']
    xmin = df.loc[y.idxmin(), 'date']
    min_value_title = df.loc[y.idxmin(), 'title']
    min_value_date = df.loc[y.idxmin(), 'date']
    
    annot_max(x, y, xmax, ymax, max_value_title, ax)
    annot_min(x, y, xmin, ymin, min_value_title, ax)
    
    plt.xticks(rotation=45,horizontalalignment='right',fontweight='light', fontsize='x-small')
    plt.xlim(pd.to_datetime("1960-01-01"), pd.to_datetime("1986-01-01"))
    if plot_dates: 
        death = pd.to_datetime("1980-12-08")
        memorial = pd.to_datetime("1985-10-09")
        plt.vlines(x = death, ymin = ymin, ymax = ymax,
               colors = 'red', label = "John Lennon\nassassinated")
        plt.vlines(x = memorial, ymin = ymin, ymax = ymax,
               colors = 'pink', label = "Strawberry Fields\nmemorial dedicated")
    locator = mdates.DayLocator(interval=3000)
    #graph.xaxis.set_major_locator(locator)
    leg = plt.legend()
    y_label = "_".join(value_to_plot.lower().split())
    plt.savefig(dataset_label + y_label + "_" + today + ".png")

def highlight_max_min_points(value, df, dataset_label, today, color = "dark", how_many = 5): 
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
                     # importing libraries
    fig, ax = plt.subplots()
    value_dict = {"swn_analysis_r":"SentiWordNet valence", 
    "textblob_polarity_r":"TextBlob polarity", 
    "textblob_subjectivity_r":"TextBlob subjectivity", 
    "vader_analysis_r":"VADER valence"}
    dates = ["1960-08-12", 
        "1962-10-17", 
        "1964-02-09", 
        "1966-07-29", 
        "1966-08-29", 
        "1967-02-17", 
        "1970-04-10", 
        "1980-12-08", 
        "1981-08-31", "1985-10-09"]
    for date in dates: 
        pd_date = pd.to_datetime(date)
        plt.axvline(x = pd_date, color = '#63D297')
      
    ax.set_facecolor(facecolor)
    fig.set_facecolor(facecolor)
    x = df["date"]
    y = df[value]
    plt.plot(x, y, linewidth = 1, color = contrast_color)
    
    color_list = ["#63D297", "#FF5252", "#FFF176", "#23B5D3", "#BADEFC"] #fix this later
    color_list_2 = ["#F33677", "#FFDDDD", "#EA7AF4", "#E8AA14", "#717EC3"]
    
    sorted_by_value = df.sort_values(by=value)
    minimums = sorted_by_value.head(how_many)
    minimums_x = list(minimums["date"])
    minimums_y = list(minimums[value])
    minimums_titles = list(minimums["title_r"])
    minimums_docs = list(minimums["doc_r"])
    
    
    maximums = sorted_by_value.tail(how_many)
    maximums_x = list(maximums["date"])
    maximums_y = list(maximums[value])
    maximums_titles = list(maximums["title_r"])
    maximums_docs = list(maximums["doc_r"])
    
    #jitter_max_x = rand_jitter(maximums_x)
    jitter_max_y = rand_jitter(maximums_y)
    #jitter_min_x = rand_jitter(minimums_x)
    jitter_min_y = rand_jitter(minimums_y)
    
    
    
    for i in range(0, how_many): 
        #sns.stripplot(data =df, x="x", y="y", jitter=0.2, size=2)
        plt.scatter(minimums_x[i], jitter_min_y[i], label = str(minimums_titles[i][0:10]) + "...", color=color_list[i])
        plt.scatter(maximums_x[i], jitter_max_y[i], label = str(maximums_titles[i][0:10]) + "...", color=color_list_2[i])
    
    plt.xticks(rotation=45,horizontalalignment='right',fontweight='light', fontsize='x-small')
    plt.xlim(pd.to_datetime("1960-01-01"), pd.to_datetime("1986-01-01"))
    ax.set(xlabel = "Date", ylabel = value_dict[value], title = 
    "Changes in " + value_dict[value] + " over time")
    
    ax.spines.top.set_color(contrast_color)
    ax.spines.bottom.set_color(contrast_color)
    ax.spines.left.set_color(contrast_color)
    ax.spines.right.set_color(contrast_color)
    ax.xaxis.label.set_color(contrast_color)
    ax.tick_params(axis='x', colors=contrast_color)
    ax.yaxis.label.set_color(contrast_color)
    ax.tick_params(axis='y', colors=contrast_color)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), facecolor = facecolor, edgecolor = contrast_color)
    y_label = "_".join(value.lower().split())
    plt.savefig(image_path + dataset_label + y_label + "_" + today + ".png")
    
def rand_jitter(arr):
    stdev = .2 * (max(arr) - min(arr))
    return arr + np.random.randn(len(arr)) * stdev

def wordcloud(df, dataset_label):
    df = df.tail(7500)
    plt.figure()
    wordcloud = WordCloud(
        background_color='black',
        stopwords=stopwords,
        max_words=300,
        max_font_size=30,
        scale=3,
        random_state=1)
    data =  ' '.join(df["text"].astype(str))
    wordcloud=wordcloud.generate(str(data))

    fig = plt.figure(1, figsize=(12, 12))
    plt.axis('off')

    wordcloud_path = dataset_label + "_tail_wordcloud.png"
    wordcloud.to_file(wordcloud_path)


if __name__ == '__main__':
    path = "/home/mwolff3/csv_files/"
    #csv_list = ["pop_all_no_text_fixed_dates_oct_25.csv"]#"pop_all_text_oct_23.csv"]
    csv_list = ["final_pop_text_nov_05.csv"]
    value_list = ["textblob_polarity_r", "textblob_subjectivity_r", "vader_analysis_r", "swn_analysis_r"]
    today = "dec_18"
    #df = pd.read_csv(csv_list[0]) 
    for csv in csv_list: 
        df = pd.read_csv(path + csv)
        df["date"] = pd.to_datetime(df["date"], errors = 'coerce')
        dataset_label = csv.replace(".csv", "")
        bkgd = ((df["beatles"] == 0) & (df["strawberry_fields"] == 0))
        bkgd_df = df[bkgd]
            
        beatles = ((df["beatles"] == 1))
        beatles_df = df[beatles]
            
        sf_beat = ((df["beatles"] == 1) & (df["strawberry_fields"] == 1))
        sf_beat_df = df[sf_beat] 
        
        columns = ["textblob_polarity", "textblob_subjectivity", "vader_analysis",  "swn_analysis"]
        dfs = {"bkgd" : bkgd_df, "beatles" : beatles_df, "sf" : sf_beat_df}
        for name in dfs: 
            for value in value_list: 
                highlight_max_min_points(value, dfs[name], name, today, color = "light", how_many = 5)
         
    '''for csv in csv_list: 
        df = pd.read_csv(path + csv)
        bkgd = ((df["beatles"] == 0) & (df["strawberry_fields"] == 0))
        bkgd_df = df[bkgd]
        
        beatles = ((df["beatles"] == 1))
        beatles_df = df[beatles]
        
        sf_beat = ((df["beatles"] == 1) & (df["strawberry_fields"] == 1))
        sf_beat_df = df[sf_beat] 
        
        wordcloud(bkgd_df, "bkgd")
        wordcloud(beatles_df, "beat")
        wordcloud(sf_beat_df, "sf")'''
        #wordcloud(df, dataset_label)

