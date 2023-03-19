from flask import Flask, request, render_template,request
import pickle
import requests
import pandas as pd
from patsy import dmatrices

movies=pickle.load(open('movies.pkl','rb'))
similar=pickle.load(open('similarity.pkl','rb'))
def poster(movie_id):
    url="https://api.themoviedb.org/3/movie/{}?api_key=906b44d502c9c4a91034067e114671a3",format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    full_path="https://image.tmdb.org/t/p/w500/"+ poster_path
    return full_path

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similar[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_moviename=[]
    recommended_movieposter=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movieposter.append(poster(movie_id))


app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/recommend',methods=['GET','POST'])
def recommend():
    if request.method =="POST":
        try:
            if request.form:
                movies_name=request.form['movies']
                #print(movies_name)
        except Exception as e:
            error={'error':e}
            return render_template("prediction.html")
    else:
        return render_template("recommend.html")


     