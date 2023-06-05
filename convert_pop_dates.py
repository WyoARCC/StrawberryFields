import pandas as pd
from dateutil.parser import parse
import datetime
#from datetime.datetime import strptime 

def split_by_format(date):
    #print("split by format")
    print("date: " + str(date))
    '''two_dates = [] 
    try: 
        two_dates = date.split("-")
    except: pass
    if len(two_dates) > 0: 
        date = two_dates[1]
    strptime('Mon Feb 15 2010', '%a %b %d %Y')'''
    date = str(date)
    date = date.replace(",", "")
    date = date.replace("c", "")
    date = date.replace("s", "")
    date = date.replace(".", "")
    date = date.replace("-", " ")
    #print("cleaned date: " + str(date))
    years = [int(s) for s in date.split() if s.isdigit() and len(s) == 4]
    #print("years: " + str(years))
    days = [int(s) for s in date.split() if s.isdigit() and len(s) < 3]
    #print("days: " + str(days))
    months = [s for s in date.split() if not s.isdigit()]
    #print("months: " + str(months))
    #print("\n")
    return convert_dates(days, months, years)
    
def convert_dates(days, months, years):
    day = ""
    month = ""
    year = ""
    
    day_num = 0
    month_num = 0
    year_num = 0
    
    '''if len(months) > 0 and months[0] == "None":
        return None
        print("none")
    '''
   
    if len(years) == 0: 
        return None
    else: 
        year = years[-1]
        year_num = int(years[-1])
        
    if len(months) == 0: 
        month_num = 12
    else: 
        month = months[-1]
        if month == "Jan":
            month_num = 1
        elif month == "Feb":
            month_num = 2
        elif month == "Mar":
            month_num = 3
        elif month == "Apr":
            month_num = 4
        elif month == "May":
            month_num = 5
        elif month == "Jun":
            month_num = 6
        elif month == "Jul":
            month_num = 7
        elif month == "Aug":
            month_num = 8
        elif month == "Sep" or month == "Sept":
            month_num = 9
        elif month == "Ot":
            month_num = 10
        elif month == "Nov":
            month_num = 11
        elif month == "De":
            month_num = 12
        else:
            print("unknown month: " + month)
            month_num = 12
            
    if len(days) == 0: 
        if month_num in [9, 4, 6, 11]: 
            day_num = 30
        elif month_num == 2:
            if year_num % 4 == 0: 
                day_num = 29
            else: day_num = 28
        else: 
            day_num = 31    
    else: 
        day = days[-1]
        day_num = int(days[-1])
       
    year = str(year_num)
    month = str(month_num)
    day = str(day_num)     
       
    #print("day_num: " + str(day_num) + " month num: " + str(month_num) + " year num: " + str(year_num))
    
    if len(month) == 1: 
        month = "0" + month
    if len(day) == 1: 
        day = "0" + day
    full_date = year + "-" + month + "-" + day
    #print(full_date)
    return full_date

def fix_single_date(date): 
    if date == "1969-06-31":  
        return "1969-06-30"
    elif date == "1968-00-31": 
        return "1968-12-31"
    else:
        return date

#csv_list = ["pop_all_no_text_cleaned_dates_oct_24.csv"]
csv_list = ["pop_all_no_text_oct_23.csv"]

directory = "/home/mwolff3/csv_files/"
for csv in csv_list:
    df = pd.read_csv(directory + csv)
    print("csv: " + csv)
    df['date'] = df['date'].apply(split_by_format)
    df['date'] = df['date'].apply(fix_single_date)
    df2 = pd.read_csv(directory + "pop_all_no_text_cleaned_dates_oct_24.csv")
    df2["date"] = df["date"]
    df2.to_csv(directory + "pop_all_no_text_fixed_dates_oct_25.csv")
    

