from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from secret import APIKeyv3Auth, URLByGenre, Filter, APIRequest
import requests
import json, ast
from genreMap import GenreMap, Mood2GenreMap
from random import random, shuffle, randint
from tmdbv3api import TMDb, Movie, Discover

app = Flask(__name__)
api = Api(app)

MovieDetails = {}

def returnMovie(GenreID):
    '''
    tmdb = TMDb()
    tmdb.api_key = APIKeyv3Auth
    discover = Discover()
    movieList = discover.discover_movies({
        'sort_by':'popularity.desc',
        'with_genres':GenreID
    })
    
    for result in movieList:
        print jsonify(result)
    '''
    index = randint(1,10)
    response = requests.get('https://api.themoviedb.org/3/discover/movie?api_key=' +  APIKeyv3Auth + '&primary_release_year=2017&sort_by=revenue.desc&with_genres='+str(GenreID))
    MovieDetails["Poster Path"] = (response.json()['results'][index]["poster_path"])
    MovieDetails["Title"] = (response.json()['results'][index]["title"])
    MovieDetails["Overview"] = (response.json()['results'][index]["overview"])
    MovieDetails["Release Date"] = (response.json()['results'][index]["release_date"])
    MovieDetails["Average Vote"] = (response.json()['results'][index]["vote_average"])
   
@app.route('/getValue/<mood>')
def returnValue(mood):
    RecognizedMood = mood
    GenreList = Mood2GenreMap[RecognizedMood]
    shuffle(GenreList)
    Pick = GenreList[0]
    GenreID = GenreMap[Pick]
    returnMovie(GenreID)
    print MovieDetails
    return jsonify(MovieDetails)
