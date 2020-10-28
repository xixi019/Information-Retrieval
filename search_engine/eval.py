'''from google import google
import re'''
from numpy import *
'''
def google_results(query,num_page):
    search_results = google.search(f"{query} site:da.wikipedia.org", num_page)
    return [re.sub('%C3%A6','æ',re.sub('%C3%A5','å',re.sub('%C3%B8','ø',res.link.split('/')[-1]))) for res in search_results]
print(google_results('Oslo',3))
'''
# inputs are two lists, 
# y is our predicted documents' titles, 
# y_hat is the titles of documents given by google
def eval_matrix(y, y_hat, ks = range(1, 21)):
    TP = len(set(y).intersection(set(y_hat)))
    precision = TP/len(y)
    recall = TP/len(y_hat)
    print(f"Precison is {precision}. \nRecall is {recall}.")
    Map = []
    for k in ks:
        P_at_k = len(set(y[:k]).intersection(set(y_hat)))/k
        print(f"Precision at {k} is {P_at_k}.")
        Map.append(P_at_k)

    Map = mean(Map)
    print(f"Map is {Map}.")

a = ["a", "b", "c" , "d"]
b = ['gf',"a","b", "2", "10"]
eval_matrix(a, b)