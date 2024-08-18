from flask import Flask, request, render_template, jsonify
import compress_pickle
import requests
import pandas as pd
from flask_caching import Cache
from time import sleep

movies = compress_pickle.load(open('models/movies.pkl', 'rb'))
similar = compress_pickle.load(open('models/similarity.pkl', 'rb'))

def make_request_with_retries(url, params=None, retries=5, backoff=2, timeout=10):
    for i in range(retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Attempt {i+1} failed: {e}")
            if i < retries - 1:
                sleep(backoff * (i + 1))
            else:
                raise e

def poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=906b44d502c9c4a91034067e114671a3"
    response = make_request_with_retries(url)
    data = response.json()  # Parse JSON here
    poster_path = data.get('poster_path', None)
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        full_path = "URL_TO_DEFAULT_IMAGE"
    return full_path

def recommended(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similar[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_moviename = []
    recommended_movieposter = []
    recommended_movieid = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movieid.append(movie_id)
        recommended_movieposter.append(poster(movie_id))
        recommended_moviename.append(movies.iloc[i[0]].title)
    return recommended_moviename, recommended_movieposter, recommended_movieid

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/recommendation', methods=['GET', 'POST'])
def recommendation():
    movie_list = movies['title'].values
    selected_movie = None
    status = False

    if request.method == "POST":
        try:
            selected_movie = request.form.get('movies')
            print("Selected Movie:", selected_movie)  # Debugging print
            recommended_movies = recommended(selected_movie)
            x, y, movieid = recommended(selected_movie)
            print("Recommended Movies:", x)  # Debugging print
            status = True
            return render_template("recommend.html", movie_list=movie_list, poster=y, status=status, movieid=movieid, movie_name=x, selected_movie=selected_movie)
        except Exception as e:
            print("Error:", e)  # Debugging print
            error = {'error': e}
            return render_template("recommend.html", error=error, movie_list=movie_list, status=status, selected_movie=selected_movie)
    else:
        return render_template("recommend.html", movie_list=movie_list, status=status, selected_movie=selected_movie)

@cache.cached(timeout=300, key_prefix='movie_details')
@app.route('/movie_details', methods=['POST'])
def movie_details():
    api_key = '906b44d502c9c4a91034067e114671a3'
    base_url = 'https://api.themoviedb.org/3/'
    movie_id_or_title = request.form['movie_id_or_title']

    try:
        # Make request for movie details
        movie_url = f'{base_url}movie/{movie_id_or_title}'
        movie_response = make_request_with_retries(movie_url, params={'api_key': api_key})
        movie_data = movie_response.json()  # Parse JSON here

        movie_title = movie_data['title']
        movie_description = movie_data['overview']

        # Fetch cast for the movie
        cast_url = f'{base_url}movie/{movie_id_or_title}/credits'
        cast_response = make_request_with_retries(cast_url, params={'api_key': api_key})
        cast_data = cast_response.json()  # Parse JSON here
        cast = [actor['name'] for actor in cast_data['cast'][:5]]

        # Fetch reviews for the movie
        reviews_url = f'{base_url}movie/{movie_id_or_title}/reviews'
        reviews_response = make_request_with_retries(reviews_url, params={'api_key': api_key})
        reviews_data = reviews_response.json()  # Parse JSON here
        reviews = [review['content'] for review in reviews_data['results'][:5]]

        movie_details = {
            'title': movie_title,
            'description': movie_description,
            'cast': cast,
            'reviews': reviews
        }

        return jsonify(movie_details)
    except Exception as e:
        print(f"Failed to fetch movie details: {e}")
        return render_template('error_page.html', error_message="Failed to fetch movie details."), 500

@cache.cached(timeout=300, key_prefix='movie_page_<int:movieid>')
@app.route('/movie_page/<int:movieid>', methods=['GET'])
def movie_details_page(movieid):
    api_key = '906b44d502c9c4a91034067e114671a3'
    base_url = 'https://api.themoviedb.org/3/'
    
    try:
        # Fetch movie details
        movie_url = f'{base_url}movie/{movieid}'
        movie_response = make_request_with_retries(movie_url, params={'api_key': api_key})
        
        if movie_response.status_code == 200:
            movie_data = movie_response.json()
            movie_title = movie_data['title']
            movie_description = movie_data['overview']
            poster_path = movie_data.get('poster_path')
            poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "URL_TO_DEFAULT_POSTER"

            # Fetch cast details
            cast_url = f'{base_url}movie/{movieid}/credits'
            cast_response = make_request_with_retries(cast_url, params={'api_key': api_key})
            cast = []
            if cast_response.status_code == 200:
                cast_data = cast_response.json()
                for actor in cast_data['cast'][:5]:
                    cast.append({
                        'name': actor['name'],
                        'character': actor['character'],
                        'profile_path': f"https://image.tmdb.org/t/p/w200{actor['profile_path']}" if actor['profile_path'] else "URL_TO_DEFAULT_PROFILE"
                    })

            # Fetch reviews
            reviews_url = f'{base_url}movie/{movieid}/reviews'
            reviews_response = make_request_with_retries(reviews_url, params={'api_key': api_key})
            reviews = []
            if reviews_response.status_code == 200:
                reviews_data = reviews_response.json()
                reviews = [review['content'] for review in reviews_data['results'][:5]]

            # Render the movie details page
            return render_template('movie_page.html', movie_title=movie_title, movie_description=movie_description, poster_url=poster_url, cast=cast, reviews=reviews)
        else:
            # Movie details not found or bad status code
            return render_template('error_page.html', error_message="Movie details not found."), 404

    except Exception as e:
        # Log the exception and return an error page
        print(f"Error fetching movie details: {e}")
        return render_template('error_page.html', error_message="An error occurred while fetching movie details."), 500

if __name__ == '__main__':
    app.debug = True
    app.run()
