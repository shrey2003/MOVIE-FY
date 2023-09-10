from flask import Flask, request, render_template,request,jsonify
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
    url="https://api.themoviedb.org/3/movie/{}?api_key=906b44d502c9c4a91034067e114671a3".format(movie_id)
    data=requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    if poster_path:
        full_path="https://image.tmdb.org/t/p/w500/"+ poster_path
    else:
        # Return a default image URL or handle it in the frontend
        full_path = "URL_TO_DEFAULT_IMAGE"
    return full_path


def recommended(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similar[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_moviename=[]
    recommended_movieposter=[]
    recommended_movieid=[]
    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movieid.append(movie_id)
        recommended_movieposter.append(poster(movie_id))
        recommended_moviename.append(movies.iloc[i[0]].title)

    return recommended_moviename,recommended_movieposter,recommended_movieid

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    movie_list = movies['title'].values
    status = False

    if request.method == "POST":
        try:
            selected_movie = request.form.get('movies')
            recommended_movies = recommended(selected_movie)
            x,y,movieid=recommended(selected_movie)
            status = True
            # Zip the three lists together and pass as a single list of dictionaries
           
            

            return render_template("recommend.html", movie_list=movie_list,poster=y, status=status,movieid=movieid,movie_name=x)
        except Exception as e:
            error = {'error': e}
            return render_template("recommend.html", error=error, movie_list=movie_list, status=status)
    else:
        return render_template("recommend.html", movie_list=movie_list, status=status)



@app.route('/movie_details', methods=['POST'])
def movie_details():
    api_key = '906b44d502c9c4a91034067e114671a3'# Replace with your actual TMDb API key
    base_url = 'https://api.themoviedb.org/3/'

    # Get the movie ID or movie title from the frontend
    movie_id_or_title = request.form['movie_id_or_title']  # Make sure to pass this from the frontend

    # Make a request to TMDb API to get movie details
    response = requests.get(f'{base_url}movie/{movie_id_or_title}', params={'api_key': api_key})
    if response.status_code == 200:
        movie_data = response.json()
        
        # Extract movie details from the response
        movie_title = movie_data['title']
        movie_description = movie_data['overview']

        # Fetch cast for the movie using TMDb API
        cast_response = requests.get(f'{base_url}movie/{movie_id_or_title}/credits', params={'api_key': api_key})
        if cast_response.status_code == 200:
            cast_data = cast_response.json()
            cast = [actor['name'] for actor in cast_data['cast'][:5]]  # Get the top 5 cast members

        # Fetch top 5 reviews for the movie using TMDb API
        reviews_response = requests.get(f'{base_url}movie/{movie_id_or_title}/reviews', params={'api_key': api_key})
        if reviews_response.status_code == 200:
            reviews_data = reviews_response.json()
            reviews = [review['content'] for review in reviews_data['results'][:5]]  # Get the top 5 reviews

        # Prepare the response JSON
        movie_details = {
            'title': movie_title,
            'description': movie_description,
            'cast': cast,
            'reviews': reviews
        }

        return jsonify(movie_details)
    
    return jsonify({'error': 'Movie details not found.'}), 404


if __name__ == '__main__':
    app.debug = True
    app.run()
     