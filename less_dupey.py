
import pandas as pd

'''
******* after-the-fact method to eliminated duplicate vectors ******
'''

names = "unique_files.csv"
names = pd.read_csv(names)
names = names[names['extension'] == 'docx'].copy()
names = names[['id','name']].copy()
names = names.rename(columns={'name':'MPA_filename'})
names.to_csv('unique_docx_files.csv', index=False)

vectors = 'vectorized docx corpus.csv'
vectors = pd.read_csv(vectors)
vectors.rename(columns={0:'id'})

vectors = pd.merge(vectors, names[['id','MPA_filename']], on='id',how='left')
vectors = vectors.drop_duplicates(subset = 'MPA_filename')
vectors = vectors.drop('MPA_filename',axis = 1)
vectors.to_csv('vectorized docx corpus less dupey.csv', index=False)
