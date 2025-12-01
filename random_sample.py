
import pandas as pd
import random



def random_sample(df, extension, size):
    '''
    input:
        df - pandas df (df of the Google Drive files index)
        extension - string ("doc", "docx", "pdf", etc)
        size - integer (size of sample)
    output:
        df - pandas df 
    '''
    
    df = df[df['extension'] == extension].copy() #create df of that file extension
    df.reset_index(drop = True, inplace=True) #reset the index to 0 - n
    if len(df) < size:
        size = len(df)-1 #reduce sample size to all rows, if necessary

    sample_index = [] #create a sample index
    while len(sample_index) < size:
        sample = random.randint(0,size)
        if sample not in sample_index:
            sample_index.append(sample)
    
    df = df.loc[sample_index] #define df based on sample index positions
    df.reset_index(drop = True, inplace=True)
    sample_number = random.randint(0,1000000) #generate identifier for sample
    df.to_csv(f'extension {extension} sample#{sample_number}.csv', index = False) #name the sample
    
    return df
    '''
    the random samples can then be subjected to textual analysis
    each sample df can make up a sample corpus for purposes of textual analysis
        question: does each sample corpus exhibit the same clustering?
        next step: can all files' clusters be labelled?
    
    '''

def main():

    filename = "unique_files.csv"  
    unique_files = pd.read_csv(filename)
    df_sample = random_sample(unique_files,'docx',5)
    df_sample = random_sample(unique_files,'doc',5)
    df_sample = random_sample(unique_files,'pdf',5)
    
main()


