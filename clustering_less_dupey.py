import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans

def elbow_graph(vector_csv):
    '''
    find the appropriate number of clusters by using an elbow graph
    '''

    data = pd.read_csv(vector_csv, index_col=0)#reads in the data from a csv as a pandas df
    elbow = []#create an empty list for the (K,SSE) pairs
    K = 1
    for n in range(30):
        points = data #[]#list to hold the (x,y,z) data point locations
        runs = 10 #number of times k-means algo will run in our instance of the KMeans class
        maxruns = 300 #number of iterations on a single k-means run in our instance
        km_obj = KMeans(n_clusters = K, n_init = runs, max_iter = maxruns) #create instance of KMeans class
        index = km_obj.fit_predict(data) #creates an index assignment of each data point to a cluster
        sse = km_obj.inertia_ #rounds sse's to whole numbers
        print("SSE for ",K," clusters = ",sse)#prints the SSE of the model for each K-clusters
        elbow.append((K,sse))#appends the (K,SSE) pairs
        K += 5

    K, sse = zip(*elbow)#divides the list of tuples into 2 arrays for matplotlib
    plt.scatter(K,sse)
    plt.xlabel('K (number of clusters)')
    plt.ylabel('SSE (error)')
    plt.xticks(K)
    plt.title('Elbow Graph for Optimal K')
    plt.show()


def cluster_indexer(vector_csv,K):
    '''
    export new df with cluster ids
    '''

    data = pd.read_csv(vector_csv, index_col=0)#reads in the data from a csv as a pandas df
    runs = 10 #number of times k-means algo will run in our instance of the KMeans class
    maxruns = 300 #number of iterations on a single k-means run in our instance
    km_obj = KMeans(n_clusters = K, n_init = runs, max_iter = maxruns) #create instance of KMeans class
    index = km_obj.fit_predict(data) #creates an index assignment of data point to a cluster
    data.insert(loc=0, column = 'MPA_cluster', value= index)#insert the cluster index to the dataframe
    data.to_csv('clustered docx vectors.csv')#export to a csv to make sure it worked


def main():

    vector_csv = 'vectorized docx corpus less dupey.csv'
    #elbow_graph(vector_csv)
    K = 15
    cluster_indexer(vector_csv,K)

main()
