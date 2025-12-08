
import pandas as pd


def extension_sample(df, extension):
    '''
    input:
        df - pandas df (df of the Google Drive files index)
        extension - string ("doc", "docx", "pdf", etc)
    output:
        csvs of 50-item dataframes for textual analysis
    '''
    
    df = df[df['extension'] == extension].copy() #create df of that file extension
    df.reset_index(drop = True, inplace=True) #reset the index to 0 - n

    beg = 0
    end = 49
    while beg < (len(df) - 50): #break the df into 50 row blocks
        if end > len(df):
            df_new = df.iloc[beg:len(df)]
        else:
            df_new = df.iloc[beg:end]
        df_new.to_csv(f'{extension} {beg} {end}.csv', index=False) #export to csvs
        beg+=50
        end+=50

def main():

    filename = "unique_files.csv"
    unique_files = pd.read_csv(filename)
    df_sample = extension_sample(unique_files,'docx')
    #df_sample = extension_sample(unique_files,'pdf')

    
main()


