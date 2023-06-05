#august 03 2022 13:46

import os
import re
from textblob import TextBlob

def remove_copyright(data, filename):
    copyright_string = "Reproduced with permission of the copyright owner Further reproduction prohibited without permission"
    microfilm_string = "Blocked due to copyright See full page image or microfilm"
    where_copyright = data.find(copyright_string)
    new_data = data
    if(where_copyright == -1):
        print("no copyright in: " + filename)
    else:
        new_data = data.replace(copyright_string, "")
    try:
        new_data = new_data.replace(microfilm_string, "")
        new_data = re.sub(r'New York Times 1923.+?The New York Times with Index', '', new_data)
    except:
        print("no microfilm")
        pass
    return new_data

def clean_file(input_path, output_path, input_file, spellcheck = False):
    input_fullpath = os.path.join(input_path, input_file)
    output_fullpath = os.path.join(output_path, input_file)
    with open(input_fullpath,'r',encoding="utf-8") as f:
        data = f.read()
    #print(data)
    data_0 = remove_punctuation(data)
    data_1 = re.sub(r"(?:(?!\n)\s)+", " ", data_0)
    dates_list = remove_date(data_1)
    dates_string = None
    if dates_list != None:
        dates_string = convert_dates(dates_list)
    data_2 = remove_copyright(data_1, input_fullpath)
    if spellcheck:
        #data_2 = spellcheck_file(data_2)
        data_2 = textblob_spellcheck(data_2)
    data_3 = re.sub('[^a-zA-Z0-9 ]', '', data_2)
    data_4 = data_3.lower()
    full_text = str(input_file) + "\n" + str(dates_string) + ",\n" + str(data_4)
    with open(output_fullpath,'w',encoding="utf-8") as f:
        f.write(full_text)
         
def remove_punctuation(string):
    punc = '''!()[]{};:'"\,<>./?@#$%^&*_~'''
    for ele in string:
        string = string.replace("-", " ")
        if ele in punc:
            string = string.replace(ele, " ") 
    return string

def remove_date(data):
    split_data = data.split()
    try:
        index = split_data.index("ProQuest")
        dates = split_data[index-3:index]
        return dates
    except:
        return None

def convert_dates(dates):
    month = dates[0]
    if month == "Jan":
        dates[0] = 1
    elif month == "Feb":
        dates[0] = 2
    elif month == "Mar":
        dates[0] = 3
    elif month == "Apr":
        dates[0] = 4
    elif month == "May":
        dates[0] = 5
    elif month == "Jun":
        dates[0] = 6
    elif month == "Jul":
        dates[0] = 7
    elif month == "Aug":
        dates[0] = 8
    elif month == "Sep":
        dates[0] = 9
    elif month == "Oct":
        dates[0] = 10
    elif month == "Nov":
        dates[0] = 11
    elif month == "Dec":
        dates[0] = 12
    else:
        print(month)
    day = str(dates[1])
    if len(dates[1]) < 2:
        day = "0" + str(dates[1])
    if len(str(dates[0])) < 2:
        dates[0] = "0" + str(dates[0])
    return str(dates[2]) + "-" + str(dates[0]) + "-" + day

def clean_directory(input_path, output_path, spellcheck = False):
    for input_file in os.listdir(input_path):
        clean_file(input_path, output_path, input_file, spellcheck)

def print_dates(date_path):
    for date_file in os.listdir(date_path):
        date_fullpath = os.path.join(date_path, date_file)
        with open(date_fullpath) as f:
            first_line = f.readline()
            print(first_line + " " + date_file)

def spellcheck_file(string):
    import spellchecker
    from spellchecker import SpellChecker
    #print(string)
    spell = SpellChecker()
    string_list = string.split()
    #print(string_list)
    misspelled = spell.unknown(string_list)
    print(misspelled)
    spelled = []
    for word in misspelled:
    # Get the one `most likely` answer
        #print(spell.correction(word))
        spelled.append(spell.correction(word))
    result = " ".join(spelled)
    return(result)

def textblob_spellcheck(string):
    textblob_string = TextBlob(string)
    corrected_string = textblob_string.correct()
    return str(corrected_string)

if __name__ == '__main__':
    '''
    cleaned_output_path = '/home/milanawolff/Documents/SF_Clean_Spellcheck_Output_NYT'
    raw_output_path = '/home/milanawolff/Documents/SF_Raw_Output_NYT'
    source_path = "/home/milanawolff/Documents/SF_Sources_NYT"
    input_file = "50_Years_in_the_Life_of_Sgt._P.pdf"
    '''
    cleaned_output_path_0 = "/home/mwolff3/nyt_cleaned_spellcheck_data"
    cleaned_output_path_1 = "/home/mwolff3/nyt_cleaned_data"
    raw_output_path = "/home/mwolff3/raw_data"

    clean_directory(raw_output_path, cleaned_output_path_0, spellcheck = True)
    clean_directory(raw_output_path, cleaned_output_path_1)
    print("cleaned all")




