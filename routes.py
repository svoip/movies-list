from flask import Flask, render_template, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import Response
from pprint import pprint

app = Flask(__name__)

# static content
movies_list = [
    {
        'id': "1",
        'title': 'King Kong',
        'year': 1976,
        'description': 'Petroleum exploration expedition comes to an isolated island and encounters a giant gorilla',
        'genres':['Adventure', 'Fantasy']
    },
    {
        'id': "2",
        'title': 'Titanic',
        'year': 1997,
        'description': 'Poor artist and aristocrat girl fall in love',
        'genres':['Drama', 'Romance']
    },
    {
        'id': "3",
        'title': 'The sixth sense',
        'year': 1999,
        'description': 'A boy that communicates with spirits',
        'genres':['Drama', 'Mystery', 'Thriller']
    }
]

# get all movies
@app.route('/movies/api/v1.0/movies', methods=['GET'])
def get_movies():
    return jsonify({'movies': movies_list})


# insert a new or edit an existing movie
@app.route('/movies/api/v1.0/edit', methods=['POST'])
def edit_movie():
    json = request.get_json()
    if not json or not 'title' in json:
        abort(400)

    movie_being_edited = {}
    movie_being_edited['title'] = json['title']
    movie_being_edited['description'] = json['description']
    movie_being_edited['year'] = json['year']
    
    print(json['genres'])

    genres = []
    for g in json['genres']:
        genres.append(str(g))
    movie_being_edited['genres'] = genres
    
    # editing an existing movie
    if json['id']:
        movie_being_edited['id'] = json['id']
        for movie in movies_list:
            if movie['id'] == movie_being_edited['id']:
                movies_list.remove(movie)

        movies_list.append(movie_being_edited)
        return jsonify({'movie': movie_being_edited}), 200
    # creating new movie item
    else:
        movie_being_edited['id'] = next_movie_id()
        movies_list.append(movie_being_edited)
        return jsonify({'movie': movie_being_edited}), 201


# helper
def next_movie_id():
    seq = [m['id'] for m in movies_list]
    max_id = max(seq)
    max_id = int(max_id) + 1
    return str(max_id)

@app.route('/')
def home():
  return render_template('home.html', movies_list = movies_list)


if __name__ == '__main__':
  app.run(debug=True)
