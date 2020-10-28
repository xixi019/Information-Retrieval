import nltk
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from scipy.spatial import distance
from train_model import corpus,titles
from google import google
import re

# get titles of the pages we search from google
def getTitlefromURL(the_url):
    ret=re.sub('%C3%B8','ø',the_url)
    ret=re.sub('%C3%A5','å',ret)
    ret=re.sub('%C3%A6','æ',ret)
    return re.sub('_',' ',ret)

# use google api to get the relevant pages.
# we assume google returns all relevant articles.
# there are two parameter this funtion takes: query to search and number of pages 
# that google returns.
def google_results(query,num_page):
    search_results = google.search(f"{query} site:da.wikipedia.org", num_page)
    return [getTitlefromURL(res.link.split('/')[-1]) for res in search_results]

def eval_matrix(y, y_hat, ks = range(1, 21)):
    TP = len(set(y).intersection(set(y_hat)))
    precision = TP/len(y)
    recall = TP/len(y_hat)
    print(f"Precison is {precision}. \nRecall is {recall}.")
    AP = []
    for k in ks:
        P_at_k = len(set(y[:k]).intersection(set(y_hat)))/k
        print(f"Precision at {k} is {P_at_k}.")
        AP.append(P_at_k)
    Aps = AP
    AP = np.mean(AP)
    print(f"Average Precision is {AP}.")
    return AP, Aps

#process the input query
vectorizer = pickle.load(open('tfidf-model.sav', 'rb'))
fre_matrix = pickle.load(open('fre-max', 'rb'))
queries = ['Udsagn','Beryllium','Gas','Acetylen','Tobak','Stofskifte','Hypotese',
           'Sandhed','Samsø']
MAP = []
precs = []
for q in queries:
    #query = input("what do you want to search?")
    query = nltk.word_tokenize(q)


    query_matrix = vectorizer.transform(query)



    #calculate cosine distance and Euclidean distance
    Cos_distance = cosine_similarity(query_matrix, fre_matrix)[0]
    Euclidean = {}
#    for idx, vec in enumerate(fre_matrix):
#        Eucli_distance = 

#    Eucli_distance = distance.euclidean(a, b)
    bests = np.argsort(Cos_distance)[-30:]
    print(beats)
    y_hat=[title[0] for i,title in enumerate(titles) if i in bests]
    print(y_hat)
    y=google_results(q,3)
    AP, aps = eval_matrix(y_hat,y)
    MAP.append(AP)
    precs.append(aps)


MAP = np.mean(MAP)
print(f"MAP is {MAP}.")
