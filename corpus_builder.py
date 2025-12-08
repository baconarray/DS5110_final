import pandas as pd

def corpus_builder(tokenized_list):
    '''
    input: list of dfs
    output: single df
    '''
    df_list = [pd.read_csv(i) for i in tokenized_list]#read in the csvs as dfs
    corpus_df = pd.concat(df_list, ignore_index=True)#concatenate vertically
    return corpus_df

def main():
    
    tokenized_list = [
    'tokenized docx 0 49.csv',
    'tokenized docx 50 99.csv',
    'tokenized docx 100 149.csv',
    'tokenized docx 150 199.csv',
    'tokenized docx 200 249.csv',
    'tokenized docx 250 299.csv',
    'tokenized docx 300 349.csv',
    'tokenized docx 350 399.csv',
    'tokenized docx 400 449.csv'
    ]
    
    corpus_df = corpus_builder(tokenized_list)
    corpus_df.to_csv('tokenized docx corpus.csv', index = False) #export to csv
    
main()
