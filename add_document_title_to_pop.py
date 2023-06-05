import os
import pandas as pd 
import glob
source_path = "sf_data/pop_data/cleaned_data_all" 
def append_doc_names(source_path): 
    for input_file in os.listdir(source_path):
        fullpath = source_path + "/" + input_file
        with open(fullpath,'a',encoding="utf-8") as f:  
            f.write(",\n" + input_file)
            print(input_file)

def csv_to_df(cleaned_output_path):
    all_files = glob.glob(os.path.join(cleaned_output_path , "*.txt"))
    df = pd.concat((pd.read_csv(f, delimiter=",\n", engine='python', header=None).transpose() for f in all_files), ignore_index = True)  
    df.rename(columns={0: "title", 1: "date", 2: "text", 3: "doc", 4: "doc_2", 5: "doc_3"}, inplace=True)
    df.drop(columns = ["doc_2", "doc_3"])
    df = df.dropna(subset = ["text"]) #DO NOT DROP TEXT BC WE ARE JOINING ON TEXT
    return df
    
root_path = "/home/mwolff3/csv_files/"
df = csv_to_df(source_path)
print("part 1")
df.to_csv(root_path + "pop_oct_23")
print("part 2")
#csv_to_df(source_path).to_csv(root_path + "pop_oct_22_with_document_names")

