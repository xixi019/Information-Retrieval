from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pickle
import re

# creat corpus and titles of the articles of the wikipediadata
def data_process():
    # get the corpus
    file_objet = open("with_titles.txt", "r", encoding="UTF-8")
    articles = file_objet.read()
    raw = articles.split('</article>')
    pattern = '<article name="(.*?)">'
    corpus = [re.split(pattern, article)[-1] for article in raw] 
    titles = [re.findall(pattern, article) for article in raw]

    return corpus, titles

# train the model with tf-idf and save the matrix 

def train(corpus):
    vectorizer = TfidfVectorizer()
    vectorizer.fit(corpus)
    filename = 'tfidf-model.sav'
    pickle.dump(vectorizer, open(filename, 'wb'))
    fre_matrix = vectorizer.transform(corpus)
    pickle.dump(fre_matrix, open('fre-max', 'wb'))

    print(f"save model in {filename}")

corpus,titles = data_process()
if __name__ == '__main__':
    train(corpus)