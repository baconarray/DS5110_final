
import pandas as pd
import random


def random_sample(df, subtype, size):
    '''
    input:
        df - pandas df (df of the complete Google Drive index)
        subtype - string ("txt","pdf", etc)
        size - integer (size of sample)
    output:
        df - pandas df 
    '''
    
    df = df[df['subtype'] == subtype].copy() #create df of that subtype
    df.reset_index(drop = True, inplace=True) #reset the index to 0 - n
    if len(df) < size:
        size = len(df)-1 #reduce sample size to all rows, in necessary

    sample_index = [] #create a sample index
    while len(sample_index) < size:
        sample = random.randint(0,size)
        if sample not in sample_index:
            sample_index.append(sample)
    
    df = df.loc[sample_index] #define df based on sample index positions
    df.reset_index(drop = True, inplace=True)
    sample_number = random.randint(0,1000000) #generate identifier for sample
    df.to_csv(f'subtype {subtype} sample#{sample_number}.csv', index = False) #name the sample
    
    return df
    '''
    the random samples can then be subjected to textual analysis
    each sample df can make up a sample corpus for purposes of textual analysis
        question: does each sample corpus exhibit the same clustering?
    
    '''

def main():

    filename = "Spotify_Youtube_Locations.csv"
    df = pd.read_csv(filename)
    subtype = "txt"
    size = 50

    random_sample(df, subtype, size)
    
main()
