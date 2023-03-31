import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

nltk.download("stopwords")
nltk.download("punkt")

def load_data():
    df1 = pd.read_csv('climate.csv')
    df2 = pd.read_csv('sport.csv')
    df3 = pd.read_csv('technology.csv')
    df = pd.concat([df1, df2, df3], axis=0).reset_index(drop=True)
    # return df
    # df=pd.DataFrame("dataset.csv")
    return df

def preprocess_text(text):
    sw = stopwords.words('english')
    ps = PorterStemmer()
    text = re.sub(r'[^\w\s]', '', text) # 去除标点符号
    tokens = word_tokenize(text.lower())
    filtered_tokens = [ps.stem(w) for w in tokens if w not in sw]
    return ' '.join(filtered_tokens)

def preprocess_data(data):
    return [preprocess_text(doc) for doc in data]

def vectorize_data(data):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data)
    return X, vectorizer

def train_model(X, n_clusters=5):
    model = KMeans(n_clusters=n_clusters)
    model.fit(X)
    return model

def visualize_clusters(X, labels):
    pca = PCA(n_components=2)
    X_reduced = pca.fit_transform(np.asarray(X.todense()))
    plt.scatter(X_reduced[:, 0], X_reduced[:, 1], c=labels)
    plt.title("Cluster visualization using PCA")
    plt.show()

def predict_cluster(test_docs, vectorizer, model):
    filtered_test_docs = preprocess_data(test_docs)
    Y = vectorizer.transform(filtered_test_docs)
    predictions = model.predict(Y)
    return predictions

if __name__ == "__main__":
    df = load_data()
    print(df.head())
    print("Number of documents:", len(df))

    filtered_docs = preprocess_data(df['content'])
    X, vectorizer = vectorize_data(filtered_docs)
    print('X.todense()', X.todense())

    model = train_model(X)
    labels = model.labels_
    print("Cluster number of input documents, in the order they received:")
    print(labels)

    visualize_clusters(X, labels)

    test_docs = ["I like football London",
                "Bitcoin is great.",
                "I study at Coventry University",
                "he is my mother,but I love her"
                ]

    predictions = predict_cluster(test_docs, vectorizer, model)
    for i, pred in enumerate(predictions):
        print(f"Test document {i+1} belongs to cluster {pred}")
