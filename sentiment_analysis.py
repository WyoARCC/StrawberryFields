#july 22 2022 15:29
#aug 03 2022 12:46
#aug 12 2022 16:17
#sept 01 2022 16:12
#sept 06 2022 17:06
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import nltk
import re
import textblob
import glob
import os
import vaderSentiment
import flair
import swifter

from nltk import download
nltk.download("stopwords")
nltk.download("omw-1.4")
nltk.download("averaged_perceptron_tagger")
nltk.download("punkt")
nltk.download("wordnet")
nltk.download("sentiwordnet")

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.corpus import sentiwordnet as swn

from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flair.models import TextClassifier
from flair.data import Sentence

pd.set_option("display.width", 120)

def csv_to_df(cleaned_output_path):
    all_files = glob.glob(os.path.join(cleaned_output_path , "*.txt"))

    df = pd.concat((pd.read_csv(f, delimiter=",\n", engine='python', header=None).transpose() for f in all_files), ignore_index = True)
    
    df.rename(columns={0: "title", 1: "date", 2: "text"}, inplace=True)
    df=df.dropna(subset = ["text"])
    print("this is my very sexy dataframe")
    print(df)
    return df

def token_stop_pos(text):
    pos_dict = {"J":wordnet.ADJ, "V":wordnet.VERB, "N":wordnet.NOUN, "R":wordnet.ADV}
    tags = pos_tag(word_tokenize(text))
    newlist = []
    for word, tag in tags:
        if word.lower() not in set(stopwords.words("english")):
            newlist.append(tuple([word, pos_dict.get(tag[0])]))
    return newlist

def tag_parts_of_speech(mydata):
    mydata["pos_tagged"] = mydata["text"].apply(token_stop_pos)
    return mydata
    
def lemmatize(pos_data):
    wordnet_lemmatizer = WordNetLemmatizer()
    lemma_rew = " "
    for word, pos in pos_data:
        if not pos:
            lemma = word
            lemma_rew = lemma_rew + " " + lemma
        else:
            lemma = wordnet_lemmatizer.lemmatize(word, pos=pos)
            lemma_rew = lemma_rew + " " + lemma
    return lemma_rew

def textblob_subjectivity(review):
    return TextBlob(review).sentiment.subjectivity
    
def textblob_polarity(review):
    return TextBlob(review).sentiment.polarity

def vader_sentiment_analysis(review):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(review)
    #return vs["compound"].astype(float)
    return vs["compound"]

def sentiwordnet_analysis(pos_data):
    sentiment = 0
    tokens_count = 0
    wordnet_lemmatizer = WordNetLemmatizer()
    for word, pos in pos_data:
        if not pos:
            continue
        lemma = wordnet_lemmatizer.lemmatize(word, pos=pos)
        if not lemma:
            continue
        synsets = wordnet.synsets(lemma, pos=pos)
        if not synsets:
            continue
        synset = synsets[0]
        swn_synset = swn.senti_synset(synset.name())
        sentiment += swn_synset.pos_score() - swn_synset.neg_score()
        tokens_count += 1

    if tokens_count == 0:
        return 0
    else: 
        return sentiment/tokens_count

def flair_analysis(pos_data):
    classifier = TextClassifier.load("en-sentiment")
    sentence = Sentence(pos_data)
    classifier.predict(sentence)
    return sentence.labels

def create_sentiment_csv(cleaned_output_path, csv_name):
    dataframe = csv_to_df(cleaned_output_path)
    mydata = tag_parts_of_speech(dataframe)
    mydata["lemma"] = mydata["pos_tagged"].apply(lemmatize) #see if just using apply fixes too many values error
    
    fin_data = pd.DataFrame(mydata)
    fin_data["vader_analysis"] = fin_data["lemma"].swifter.allow_dask_on_strings(enable=True).apply(vader_sentiment_analysis)
    fin_data["textblob_subjectivity"] = fin_data["lemma"].swifter.allow_dask_on_strings(enable=True).apply(textblob_subjectivity)
    fin_data["textblob_polarity"] = fin_data["lemma"].swifter.allow_dask_on_strings(enable=True).apply(textblob_polarity)
    fin_data["swn_analysis"] = fin_data["pos_tagged"].apply(sentiwordnet_analysis)
    #fin_data["flair_analysis"] = fin_data["text"].swifter.allow_dask_on_strings(enable=True).apply(flair_analysis)

    fin_data = pd.DataFrame(mydata[["title", "date", "text", "textblob_polarity", "textblob_subjectivity", "vader_analysis", "swn_analysis"]])
    fin_data.to_csv(csv_name + ".csv")

if __name__ == '__main__':
    #cleaned_output_path = "/home/milancd sawolff/Documents/SF_Clean_Output_NYT"
    #cleaned_output_path = "/home/mwolff3/pop_cleaned_i_sf"
    root_path = "/home/mwolff3/"
    #directories = ["pop_cleaned_i", "pop_cleaned_beatles_fuzzy", "pop_cleaned_i_sf"]
    #directories = ["pop_cleaned_i_beatles_fuzzy", "pop_cleaned_ii_beatles_fuzzy"] 
    directories = ["pop_cleaned_i_aug_22", "pop_cleaned_ii_aug_22"]
    #directories = ["sentiment_analysis_test_sept_08"]
    for directory in directories: 
        cleaned_output_path = root_path + directory
        create_sentiment_csv(cleaned_output_path, root_path + "csv_files/" + directory + "_sept_08")

