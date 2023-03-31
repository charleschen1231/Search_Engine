'''

1  当用户输入单个关键词时，我们可以根据余弦相似度返回与该关键词最相关的文章。
如果用户输入的是一个短语或句子，我们可以使用TF-IDF加权平均值来计算输入与所有文章之间的相似度，并返回最相关的文章。

2 索引的排名是根据余弦相似度的值来排名的，值越大，排名越靠前

3 工作流程如下：读取包含论文信息的 CSV 文件，该文件的名字为 "Publication_Info.csv"；
定义一个名为 preprocess_text() 的函数，用于对论文文本进行预处理，包括去除标点符号和数字、分词、去除停用词、词形还原等；
对论文文本进行预处理，将预处理后的文本存储在一个名为 "content" 的列中；
使用 TfidfVectorizer 计算文本的 TF-IDF 值，将结果存储在名为 "tfidf_matrix" 的矩阵中；
创建 Flask 应用程序，定义两个路由："/" 和 "/results"；
当用户访问路由 "/" 时，返回一个包含搜索框和搜索按钮的 HTML 模板；
当用户在搜索框中输入关键字并点击搜索按钮时，提交表单，发送 POST 请求，Flask 会执行路由 "/results" 中的代码；
在路由 "/results" 中，首先获取用户输入的关键字并进行预处理，然后计算用户输入和所有论文之间的余弦相似度；
对余弦相似度进行排序，获取相似度最高的若干篇论文，并将这些论文的信息封装成一个列表；
对于每篇论文，计算其文本中包含的关键字和用户输入中的关键字的交集，将结果存储在列表中；
计算搜索结果的精确率、召回率、F1 值和准确率，并将结果渲染到一个包含搜索结果、评价指标的 HTML 模板中；
运行 Flask 应用程序，启动 Web 服务器。



1  When the user enters a single keyword, we can return the most relevant article for that keyword based on cosine similarity.

If the user enters a phrase or sentence, we can use the TF-IDF weighted average to calculate the similarity between the
input and all articles and return the most relevant articles.

2 Index rankings are based on the value of cosine similarity, the higher the value, the higher the ranking

3 work flow:
1 )Read the CSV file containing publication information named "Publication_Info.csv".
2 ) Define a function named preprocess_text() for preprocessing the publication text, including removing punctuation
and digits, tokenizing, removing stop words, lemmatizing, etc.
3 )  Preprocess the publication text and store the preprocessed text in a column named "content".
4 )Use TfidfVectorizer to calculate the TF-IDF values of the text and store the results in a matrix named "tfidf_matrix".
5 ) Create a Flask application and define two routes: "/" and "/results".
6) When a user visits the "/" route, return an HTML template containing a search box and a search button.
7)When a user enters a keyword in the search box and clicks the search button, Flask will execute the code in the "/results" route after submitting the form with a POST request.
In the "/results" route, first get the user input keyword and preprocess it, then calculate the cosine similarity between the user input and all publications.
Sort the cosine similarity in descending order, get the top similar publications, and package their information into a list.
For each publication, calculate the intersection between the keywords contained in its text and the user input keywords, and store the results in a list.
Calculate the precision, recall, F1 score, and accuracy of the search results, and render the results into an HTML template containing the search results and evaluation metrics.
'''


from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import precision_recall_fscore_support

nltk.download('wordnet')

app = Flask(__name__,template_folder='template',static_folder='static')

# read the dataset
df = pd.read_csv('Publication_Info.csv')


# preprocess the text
def preprocess_text(text):
    # remove punctuation and digits
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    # tokenize
    tokens = nltk.word_tokenize(text.lower())
    # remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [t for t in tokens if not t in stop_words]
    # lemmatize
    lemmatizer = WordNetLemmatizer()
    # my content is the article's abstract or the title,so I could not set >=5.if my content is paper's content this should be set >5
    tokens = [lemmatizer.lemmatize(t) for t in tokens if len(t) >= 2]
    return ' '.join(tokens)


# preprocess the content column
df['content'] = df['content'].apply(preprocess_text)

# create tf-idf matrix
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['content'])


# home page
@app.route('/')
def home():
    return render_template('input.html')


# results page
@app.route('/results', methods=['POST'])
def results():
    # get user input
    user_input = request.form['user_input']
    if not user_input:
        return render_template('input.html', error='Please enter some text.')

    # preprocess user input
    user_input = preprocess_text(user_input)

    # get the set of keywords
    keywords = set(user_input.split())

    # calculate tf-idf for user input
    user_input_tfidf = vectorizer.transform([user_input])

    # calculate cosine similarity between user input and all articles
    cosine_similarities = cosine_similarity(user_input_tfidf, tfidf_matrix).flatten()
    print('cosine_similarities=',cosine_similarities)


    # return all the indices.
    indices = np.argsort(cosine_similarities)[::-1]
    # pr

    # if user_input.count(' ') == 0:  # single-word input
    #     indices = np.argsort(cosine_similarities)[::-1]
    # else:
    #     # get the indices of the most similar articles
    #     indices = np.argsort(cosine_similarities)[-5:][::-1]

    # create a list of all related articles
    related_docs = []
    for index in indices:
        if cosine_similarities[index] > 0:
            article = {
                'title': df.iloc[index]['title'],
                'title_link': df.iloc[index]['title_link'],
                'author': df.iloc[index]['authors'],
                'publication_year': df.iloc[index]['publication_year'],
                'content': df.iloc[index]['content'],
                'cosine_similarity': cosine_similarities[index]
            }

            # get the set of keywords for this article
            article_keywords = set(preprocess_text(article['content']).split())

            # calculate the intersection of the two keyword sets
            common_keywords = keywords.intersection(article_keywords)

            # add the common keywords to the article dictionary
            article['common_keywords'] = common_keywords

            related_docs.append(article)

    # calculate precision, recall, F-measure, and accuracy
    print('related_docs=', related_docs)
    TP = sum([1 for doc in related_docs if user_input in doc['content']])
    print('TP=', TP)
    TN = sum(
        [1 for index, row in df.iterrows() if index not in indices and user_input not in row['content']])
    print('TN=', TN)
    FP = sum([1 for doc in related_docs if user_input not in doc['content']])
    FN = sum([1 for index, row in df.iterrows() if index not in indices and user_input in row['content']])

    precision = TP / (TP + FP) if (TP + FP) > 0 else 0.0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0.0
    f_measure = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    accuracy = (TP + TN) / (TP + TN + FP + FN) if (TP + TN + FP + FN) > 0 else 0.0

    print('precision=', precision)
    print('recall=', recall)
    print('f_measure=', f_measure)
    print('accuracy=', accuracy)



    # render the results page with related articles, cosine similarities, and evaluation metrics
    return render_template('result.html', user_input=user_input, related_docs=related_docs, precision=precision,
                           recall=recall, fscore=f_measure, accuracy=accuracy)


if __name__ == '__main__':
    app.run(debug=True)