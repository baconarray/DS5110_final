import pandas as pd
from PyPDF2 import PdfReader
import spacy
import pandas as pd
import io
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import time
import random

time.sleep(random.randint(1, 2))

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
    raw_list = raw_string.split() #get rid off all white space (split returns list)
    if len(raw_list) > 0:
        raw_string = raw_list[0]
        for l in raw_list[1:]:
            raw_string = raw_string + ' ' + l #concat back to 1 string
    else:
        raw_string = ''


    print(raw_string)
    return raw_string

def word_cleaner(raw_string, stops_df):
    nlp = spacy.load("en_core_web_sm") #load spacy
    tokens = nlp(raw_string) #create lemmas (tokens)

    token_list = []
    for t in tokens: #iterate over tokens
        token_list.append(t.lemma_) #add the lemmas to a list

    clean_words = []
    for l in token_list:
        if l.isalnum() == True: #add only the alpha-numeric strings
            clean_words.append(l)

    clean_df = pd.DataFrame({'clean_words':clean_words}) # put them in a df
    clean_df['stops'] = clean_df['clean_words'].isin(stops_df['words']) # label stopwords
    clean_df = clean_df[clean_df['stops'] == False].copy() # copy non-stopwords
    clean_df = clean_df.drop('stops', axis=1) # drop the boolean column
    counts = clean_df['clean_words'].value_counts() # TF(t) = in-document occurrences
    clean_df['NF'] = clean_df['clean_words'].map(counts/len(clean_df)) # NF = TF(t)/len(d)
    clean_df = clean_df.drop_duplicates() #drop duplicates
    return clean_df

def sample_corpus(df_sample):
    '''
    input:
        random_sample - df output by random_sample()
    output:
        df
            - in feature vector form
            - columns = terms in corpus
            - rows = documents, NF*IDF of each term
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
        time.sleep(random.randint(1,2)) #pause to avoid being flagged by Google

    print(string_dict)

    stops = 'Stopwords.txt'
    with open(stops,'r') as file:
        stops = file.read()
    stops = stops.split() # list of stop words
    stops_df = pd.DataFrame({'words':stops}) # df of stop words

    # use string_dict {google_id:raw_string} to make token_dictionary {google_id: clean_df} pairs
    token_dict = {}
    for k,v in string_dict.items():
        token_dict[k] = word_cleaner(v, stops_df)

    print(token_dict)
        
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

    filename = "subtype pdf sample#661174.csv"  
    df_sample = pd.read_csv(filename)

    df_corpus = sample_corpus(df_sample)

main()
    
