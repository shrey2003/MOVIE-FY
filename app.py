from flask import Flask, request, render_template,request
import bz2
import pickle
import compress_pickle
from compress_pickle import dump, load
import requests
import pandas as pd
from patsy import dmatrices


movies=compress_pickle.load(open('movies.pkl','rb'))
similar=compress_pickle.load(open('similarity.pkl','rb'))
def poster(movie_id):
    url="https://api.themoviedb.org/3/movie/{}?api_key=906b44d502c9c4a91034067e114671a3",format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    full_path="https://image.tmdb.org/t/p/w500/"+ poster_path
    return full_path

def recommended(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similar[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_moviename=[]
    recommended_movieposter=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movieposter.append(poster(movie_id))
        recommended_moviename.append(movies.iloc[i[0]].title)

        return recommended_moviename,recommended_movieposter

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/recommendation',methods=['GET','POST'])
def recommendation():
    movie_list=movies['title'].values
    if request.method =="POST":
        try:
            if request.form:
                movies_name=request.form['movies']
                print(movies_name)
                recommended_moviename,recommended_movieposter=recommended(movies_name)
                return render_template("recommend.html",movies_name=recommended_moviename,poster=recommended_movieposter,movie_list=movie_list)
        except Exception as e:
            error={'error':e}
            return render_template("recommend.html",error=error,movie_list=movie_list)
    else:
        return render_template("recommend.html",movie_list=movie_list)




if __name__ == '__main__':
    app.debug = True
    app.run()
     