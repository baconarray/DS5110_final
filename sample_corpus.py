from dotenv import load_dotenv
from googleapiclient.discovery import build
import pandas as pd
import io
import os
import time
import random
import spacy
from PyPDF2 import PdfReader
import docx2txt

def pdf_reader(google_id, service):

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

    return raw_string


def docx_reader(google_id, service):
        
    file = service.files().get_media(fileId=google_id) #select the file
    buffer = io.BytesIO() #create a memory object
    buffer.write(file.execute()) #write the file into the buffer
    buffer.seek(0) #re-set the buffer to [0]

    raw_string = docx2txt.process(buffer)
    raw_string = raw_string.lower() #lowercase
    raw_list = raw_string.split() #get rid off all white space (split returns list)
    if len(raw_list) > 0:
        raw_string = raw_list[0]
        for l in raw_list[1:]:
            raw_string = raw_string + ' ' + l #concat back to 1 string
    else:
        raw_string = ''

    return raw_string

def word_cleaner(google_id, raw_string, stops_df):
    nlp = spacy.load("en_core_web_sm") #load spacy
    tokens = nlp(raw_string) #create lemmas (tokens)

    token_list = []
    for t in tokens: #iterate over tokens
        token_list.append(t.lemma_) #add the lemmas to a list

    clean_words = []
    for l in token_list:
        if l.isalpha() == True and len(l) > 1: #add only whole words
            clean_words.append(l)

    clean_df = pd.DataFrame({'clean_words':clean_words}) # put them in a df
    clean_df['stops'] = clean_df['clean_words'].isin(stops_df['words']) # label stopwords
    clean_df = clean_df[clean_df['stops'] == False].copy() # copy non-stopwords
    clean_df = clean_df.drop('stops', axis=1) # drop the boolean column
    counts = clean_df['clean_words'].value_counts() # TF(t) = in-document occurrences
    clean_df['NF'] = clean_df['clean_words'].map(counts/len(clean_df)) # NF = TF(t)/len(d)
    clean_df['id'] = [google_id] * len(clean_df)
    clean_df['document count'] = 1
    clean_df = clean_df.drop_duplicates() #drop duplicates
    return clean_df

def tokenizer(filename):
    '''
    input:
        filename - name of file containing df sample
    output:
        dictionary - {google id: tokenized document as df} pairs
    '''
    
    load_dotenv() #Load Google Drive API Key from .env file
    API_KEY = os.getenv('GOOGLE_DRIVE_API_KEY')
    if not API_KEY:
        raise ValueError("Please set GOOGLE_DRIVE_API_KEY")

    service = build('drive', 'v3', developerKey=API_KEY) #create service object

    df_sample = pd.read_csv(filename) #load sample df
    id_list = df_sample['id'].to_list()
    string_dict = {}
    
    # pass the files 1 at a time to the reader functions:
    for i in range(len(df_sample)):
        if df_sample['extension'].iloc[i] == 'pdf':
            string_dict[df_sample['id'].iloc[i]] = pdf_reader(df_sample['id'].iloc[i],service)
        if df_sample['extension'].iloc[i] == 'docx':
            string_dict[df_sample['id'].iloc[i]] = docx_reader(df_sample['id'].iloc[i],service)
        if df_sample['extension'].iloc[i] == 'doc':
            pass
        if df_sample['extension'].iloc[i] == 'ppt':
            pass
        if df_sample['extension'].iloc[i] == 'pptx':
            pass
        else:
            pass
        time.sleep(random.randint(5,10)) #pause to avoid being flagged by Google

    stops = 'Stopwords.txt'
    with open(stops,'r') as file:
        stops = file.read()
    stops = stops.split() # list of stop words
    stops_df = pd.DataFrame({'words':stops}) # df of stop words

    # use word_cleaner use string_dict {google_id:raw_string}
    # to make token_dictionary {google_id: clean_df} pairs
    # word cleaner removes fillers, calculates NF, returns dfs
    token_dict = {}
    for k,v in string_dict.items():
        token_dict[k] = word_cleaner(k, v, stops_df)

    return token_dict


def token_saver(token_dict,filename):
    '''
    input: 
    '''

    tokenized_sample_df = pd.concat(token_dict.values(), ignore_index=True)    
    tokenized_sample_df.to_csv(f'tokenized {filename}', index = False)
    return tokenized_sample_df


def main():

    docx_list = [
        'docx 50 99.csv',
        'docx 100 149.csv',
        'docx 150 199.csv',
        'docx 200 249.csv',  
        'docx 250 299.csv',     
        'docx 300 349.csv',     
        'docx 350 399.csv',
        'docx 400 449.csv'
        ]
        
    for i in docx_list:
        token_dict = tokenizer(i) #returns dictionary of {google id: tokenized document df} pairs
        tokenized_sample_df = token_saver(token_dict,i)
        
main()
    
