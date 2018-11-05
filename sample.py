from flask import Flask,render_template,request
# from werkzeug.routing import BaseConverter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import jieba
import json
import ast

# class RegexConverter(BaseConverter):
#     def __init__(self,url_map,*items):
#         super(RegexConverter,self).__init__(url_map)
#         self.regex = items[0]

app = Flask(__name__)
# app.url_map.converters['regex'] = RegexConverter
@app.route("/")
def hello():
    return render_template('index.html',title="Hello World!")

# @app.route('/user/<regex("[a-z]{3}"):username>')
# def user(username):
#     return 'User %s' % username
#
# @app.route('/login',methods=['GET','POST'])
# def login():
#     return render_template('login.html',method=request.method)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def readfile(filename):
    with open(filename, 'r') as fp:
        data = json.load(fp, encoding='utf-8')
    return data

@app.route('/process',methods=['POST'])
def process():
    news_set = ast.literal_eval(request.data)

    # return news_set
    with open('./stopWord.txt') as f:
        stoplist = [line.strip().decode('utf-8') for line in f.readlines()]
    f.close()
    list = []
    for i in news_set:
        temp = ""
        body = i['body']
        for word in jieba.cut(body):
            if word not in stoplist:
                temp = temp + word + ' '
        list.append(temp)

    # TF-IDF
    vectorsizer = CountVectorizer()
    transformer = TfidfTransformer()
    x = vectorsizer.fit_transform(list)
    word = vectorsizer.get_feature_names()
    tfidf = transformer.fit_transform(x)
    weight = tfidf.toarray()

    dict2 = {}
    for j in range(len(word)):
        temp = 0
        for i in range(len(weight)):
            temp = temp + weight[i][j]
        dict2[word[j]] = temp

    for i in dict2:
        if is_number(i):
            dict2[i] = 0

    return json.dumps(dict2)


if __name__ == "__main__":
    app.run(debug=True)
