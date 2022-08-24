import numpy as np
import pandas as pd
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


ratings = pd.read_csv('/Users/jonathanshu/Documents/projects/book-catalogue/account/data/ratings.csv', sep = ';', encoding='latin1', quotechar= '"')
ratings.head()
books = pd.read_csv('/Users/jonathanshu/Documents/projects/book-catalogue/account/data/books.csv', sep = ';', encoding='latin1', quotechar = '"', escapechar='\\' )
books.head()

  
def create_matrix(df):
      
    N = len(df['User-ID'].unique())
    M = len(df['ISBN'].unique())
      
    user_mapper = dict(zip(np.unique(df["User-ID"]), list(range(N))))
    book_mapper = dict(zip(np.unique(df["ISBN"]), list(range(M))))
      
    user_inv_mapper = dict(zip(list(range(N)), np.unique(df["User-ID"])))
    book_inv_mapper = dict(zip(list(range(M)), np.unique(df["ISBN"])))
      
    user_index = [user_mapper[i] for i in df['User-ID']]
    book_index = [book_mapper[i] for i in df['ISBN']]
  
    X = csr_matrix((df["Book-Rating"], (book_index, user_index)), shape=(M, N))
      
    return X, user_mapper, book_mapper, user_inv_mapper, book_inv_mapper
  
X, user_mapper, book_mapper, user_inv_mapper, book_inv_mapper = create_matrix(ratings)
  
def find_similar_ids(book_id, X, k, metric='cosine', show_distance=False):
      
    neighbour_ids = []
      
    book_ind = book_mapper[book_id]
    book_vec = X[book_ind]
    k+=1
    kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
    kNN.fit(X)
    book_vec = book_vec.reshape(1,-1)
    neighbour = kNN.kneighbors(book_vec, return_distance=show_distance)
    for i in range(0,k):
        n = neighbour.item(i)
        neighbour_ids.append(book_inv_mapper[n])
    neighbour_ids.pop(0)
    return neighbour_ids
  
def run (book_name, book_author):
    book_authors = list(zip(books['Book-Title'], books['Book-Author']))
    book_isbn = dict(zip(book_authors, books['ISBN']))
    book_titles = dict(zip(books['ISBN'], books['Book-Title']))


    if (book_name,book_author) in book_isbn:
        book_id = book_isbn[(book_name,book_author)]

        similar_ids = find_similar_ids(book_id, X, k=10)

        similar_books = []
        for i in similar_ids:
            if (i in book_titles):
                similar_books.append(book_titles[i])

        return similar_books
    else:
        return ['No recommmendations available']
