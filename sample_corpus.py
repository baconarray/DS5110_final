import pandas as pd
from PyPDF2 import PdfReader
import spacy
import pandas as pd
import io
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

def pdf_reader(google_id):
        
    #Load Google Drive API Key from .env file
    load_dotenv()
    API_KEY = os.getenv('GOOGLE_DRIVE_API_KEY')
    if not API_KEY:
        raise ValueError("Please set GOOGLE_DRIVE_API_KEY")

    service = build('drive', 'v3', developerKey=API_KEY) #create service object
    folder_id = '12qMZKDEWn71JrN8Het5-a_NUWV0eE1ZF'

    file = service.files().get_media(fileId=google_id) #select the file
    buffer = io.BytesIO() #create a memory object
    buffer.write(file.execute()) #write the file into the buffer
    buffer.seek(0) #re-set the buffer to [0]

    reader = PdfReader(buffer) #read in the whole PDF
    raw_string = ''
    for i in range(len(reader.pages)): #iterate over each page
        page = reader.pages[i]
        text = page.extract_text()
        raw_string = raw_string + text # concat the page's text to a string
    raw_string = raw_string.lower() #lowercase
    string_list = []
    string_list.append(raw_string.split()) #get rid off all white space (split returns list)
    raw_string = string_list[0] #start with 1st string in list
    for l in string_list[1:]:
        raw_string = raw_string + ' ' + l #concat back to 1 string
    print(raw_string)
    
    return raw_string

def word_cleaner(raw_string):
    
    return df_ofSpacyTokens

def sample_corpus(df_sample):
    '''
    input:
        random_sample - df output by random_sample()
    output:
        df
            - in feature vector form
            - columns = terms in corpus
            - rows = documents, IDF of each term

    turn the id column of the sample df into a single list
    method reads in the contents of each file as a list of strings
        if it's a pdf:
            call pdf method
                read in all the pages to a PdfReader object
                clean and concatenate to 1 string
        convert to SpaCy tokens
        read into df
        add columns of: TF, NF, and Occurrence = 1 columns
        remove duplicate columns
        add the df to a list of dfs: corpus_list = [df[0], df[1]... df[n]]
        corpus
            concatenates each df to a single df: corpus_df
                value_count the occurence column = # documents containing t
                drop duplicates
                IDF = 1 + log10(len(random_sample)/# docs containing t)
                divide by len(random_sample) = # documents
                adds value_counts column to corpus df
        iterate over corpus_list
            add the corpus_df['IDF'] column to each df
            add column of NF*IDF
            drop all other columns
        now every df term,NF*IDF columns
        now transpose each dfs use .T - they are now in feature vector form
        concatenate the dfs, use .fillna(0)
        now the vectors are combined into 1 df
        

        send that 2-d df to corpus_cluster method which will use KMeans
    
    '''
    id_list = df_sample['id'].to_list()
    string_dict = {}
    
    # pass the files in the id list 1 at a time to the reader functions:
    for i in range(len(df_sample)):
        if df_sample['subtype'].iloc[i] == 'msword':
            pass
        if df_sample['subtype'].iloc[i] == 'pdf':
            string_dict[df_sample['id'].iloc[i]] = pdf_reader(df_sample['id'].iloc[i])
        if df_sample['subtype'].iloc[i] == 'jpeg':
            pass
        if df_sample['subtype'].iloc[i] == 'vnd.ms-excel':
            pass
        if df_sample['subtype'].iloc[i] == 'vnd.openxmlformats-officedocument.wordprocessingml.document':
            pass
        if df_sample['subtype'].iloc[i] == 'vnd.ms-powerpoint':
            pass
        else:
            pass
    key1, val1 = next(iter(string_dict.items()))
    print(key1,val1)
    # now the dictionary is {google_id: raw_string}
    # pass the raw_strings to the word_cleaner function
    # word cleaner uses pandas: removes fillers, calculates NF, TF return df
    # re-define dictionary as {google_id: clean_df} pairs    
    # pass that dictionary to the corpus_builder function
    # corpus used to calculate IDF
    # add IDF column to {google_id: clean_df} pairs
    # reduce clean_dfs to 2 columns: word, IDF*NF
    # concat to 1 df, transpose, run KMeans algo
    


    return string_dict


def main():

    filename = "subtype pdf sample#342783.csv"  
    df_sample = pd.read_csv(filename)

    df_corpus = sample_corpus(df_sample)
    print(df_corpus)
    
main()
    
