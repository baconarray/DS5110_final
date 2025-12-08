import pandas as pd
import numpy as np

def idf_counter(corpus_df):
    '''
    input: dataframe with columns: 'clean_words', 'NF' for each document, 'id' for each document, 'corpus count' of clean_words
    output: dataframe with new columns calculated for
                    df(t) - number of documents containing the token
                    N - number of documents in corpus
                    N/df(t) - inverse frequency of token in corpus
                    IDF - log base 2 of inverse frequency of token in corpus
                    NF*IDF - normalized frequency of token in document times IDF
    '''
    
    counts_series = corpus_df.groupby('clean_words')['clean_words'].value_counts()
    counts_df = counts_series.reset_index(name='df(t)')
    corpus_df = pd.merge(corpus_df,counts_df, on='clean_words',how='outer')
    n = len(corpus_df['id'].drop_duplicates())
    corpus_df['N'] = n
    corpus_df['N/df(t)'] = corpus_df['N'] / corpus_df['df(t)']
    corpus_df['IDF'] = np.log2(corpus_df['N/df(t)'])
    corpus_df['NF*IDF'] = corpus_df['NF'] * corpus_df['IDF']
    return corpus_df

def vector_lister(corpus_df):

    id_df = corpus_df['id'].copy()
    id_df = id_df.drop_duplicates()
    id_list = id_df.to_list() #list the google ids
    idf_dict = {}
    for i in id_list: #make dictionary of {id: document df} pairs
        idf_dict[i] = corpus_df[corpus_df['id'] == i].copy()[['clean_words','NF*IDF']]
    vector_dict = {}
    for k,v in idf_dict.items(): #rename the 'NF*IDF' column to the google id
        vector_dict[k] = v.rename(columns={'clean_words':'clean_words','NF*IDF':k})
    print(next(iter(vector_dict.items())))
    return vector_dict

def vector_merger(corpus_df,vector_dict):

    vector_df = corpus_df['clean_words'].copy()
    vector_df = vector_df.drop_duplicates() # create df of tokens
    for k,v in vector_dict.items(): # merge ['google id', [NF*IDF]] columns to token df
        vector_df = pd.merge(vector_df,v,on='clean_words',how='left')
        vector_df = vector_df.fillna(0) # replace NaN with 0
    vector_df = vector_df.set_index('clean_words').T #transpose to feature vector form
    return vector_df
    
def main():
    '''
    input: 
    '''
    
    filename = 'tokenized docx corpus.csv'
    corpus_df = pd.read_csv(filename) # load sample corpus
    corpus_df = idf_counter(corpus_df) # calculate corpus stats
    #corpus_df.to_csv('corpus counts df.csv',index=False)
    '''
    save only what will be vectorized
    '''
    corpus_df = corpus_df[['clean_words','id','NF*IDF']]
    #corpus_df.to_csv('corpus NFIDF df.csv',index=False)
    '''
    build dictionary of {id:NFIDF_df}
    '''
    vector_dict = vector_lister(corpus_df)
    '''
    merge dictionary horizontally, then transpose
    '''
    vector_df = vector_merger(corpus_df,vector_dict)
    vector_df.to_csv('vectorized docx corpus.csv')

main()
