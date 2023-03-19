from flask import Flask, request, render_template,request
import pickle
import requests
import pandas as pd
from patsy import dmatrices

movies=pickle.load(open('model/movies.pkl','rb'))
def poster(movie_id):
    url="https://api.themoviedb.org/3/movie/{}?api_key=906b44d502c9c4a91034067e114671a3",format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    full_path="https://image.tmdb.org/t/p/w500/"+ poster_path
    return full_path

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

     