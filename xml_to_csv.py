#july 20 2022 11:04
#aug 01 2022 16:18
#aug 03 2022 13:51
#aug 12 2022 16:04
#aug 15 2022 12:37
import pandas as pd
import numpy as np
import xml.etree.cElementTree as et
import re
import os
import fuzzysearch
from fuzzysearch import find_near_matches


def convert_directory_xml_to_csv(source_path, save_path): 
    for input_file in os.listdir(source_path):
        convert_file_xml_to_csv(source_path, save_path, input_file)

def clean_long_text(longtext): 
    longtext = remove_punctuation(longtext)
    return longtext
    

def convert_file_xml_to_csv(source_path, save_path, input_file): 
    text_list = []
    file_title = ''
    file_date = ''
    
    tree=et.parse(source_path + "/" + input_file)
    root=tree.getroot()
    try:
        for text in root.iter('imageText'): 
            text_list.append(text.text)
    except:
        text_list.append("")
    try:
        for desc in root.iter('Description'):
            text_list.append(desc.text)
    except: 
        text_list.append("")
    try:
        for date in root.iter('Date'):
            #print(date.text)
            file_date = date.text
    except:
        file_date = ""
    try:
        for title in root.iter('Title'):
            file_title = title.text
    except:
        file_title = ""
    counter = 0
    #print("text_list: " + str(text_list))
    for longtext in text_list:
        longtext = str(longtext)
        #print(longtext + "!!!")
        cleaned_text = clean_long_text(longtext)
        #print(cleaned_text)
        matches = 0
        near_matches = []
        '''try:
            near_matches = find_near_matches('beatles', cleaned_text, max_l_dist = 1)
            matches = len(near_matches)
        except: 
            pass
        '''
        print(near_matches)
        #print(matches)
        #print(cleaned_text)
        if True:
            #print(file_title)
            #print("more than zero matches: " + str(matches))
            full_text = str(file_title) + ",\n" + str(file_date) + ",\n" + str(cleaned_text) 
            short_input_file = input_file.replace(".xml", "")
            #print("full text" + full_text)
            output_fullpath = save_path + "/" +  short_input_file + str(counter) + ".txt" 
            with open(output_fullpath,'w',encoding="utf-8") as f:
                f.write(full_text)
            counter += 1

            

def remove_punctuation(string):
    string = re.sub('[^a-zA-Z0-9 ]', '', string)
    string = string.lower()
    return string

def format_date(data):
    split_data = data.split()
    day = data[0]
    month = convert_month(data[1])
    year = data[2]
    return str(year) + "-" + str(month) + "-" + str(day)
    

def convert_month(month):
    if month == "Jan":
        month = 1
    elif month == "Feb":
        month = 2
    elif month == "Mar":
        month = 3
    elif month == "Apr": 
        month = 4
    elif month == "May": 
        month = 5
    elif month == "Jun": 
        month = 6
    elif month == "Jul": 
        month = 7
    elif month == "Aug": 
        month = 8
    elif month == "Sep": 
        month = 9
    elif month == "Oct": 
        month = 10
    elif month == "Nov": 
        month = 11
    elif month == "Dec":
        month = 12
    else: 
        print(month)
    return month

#convert_file_xml_to_csv("/home/milanawolff/Documents/ARCC/", "/home/milanawolff/Documents/ARCC/", "OZ48_01.xml") 
convert_directory_xml_to_csv("/home/mwolff3/section_ii", "/home/mwolff3/pop_cleaned_ii_aug_22")
convert_directory_xml_to_csv("/home/mwolff3/section_i", "/home/mwolff3/pop_cleaned_i_aug_22")


