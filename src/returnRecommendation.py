from flask import Flask, jsonify, redirect, url_for, request
from flask import render_template
from flask_restful import Resource, Api, reqparse
from secret import APIKeyv3Auth, URLByGenre, Filter, APIRequest
import requests
import json, ast
from genreMap import GenreMap, Mood2GenreMap
from random import random, shuffle, randint
from tmdbv3api import TMDb, Movie, Discover
import os
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER = ''
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

MovieDetails = {}

photos = UploadSet('photos', IMAGES)



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
   

@app.route('/')
def home():
    return render_template('index.html')

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


subscription_key = '93b53ddd481b41cd99828474e9c1327c'
assert subscription_key
emotion_recognition_url = "https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize"
headers = {'Ocp-Apim-Subscription-Key': subscription_key }

@app.route('/uploadImage', methods = ['POST'])
def upload():
    f = request.files['file']
    f.save(secure_filename(f.filename))
    #url = '127.0.0.1/uploads/'+f.filename
    image_path = (f.filename)
    image_data = ''
    with open(image_path, 'rb') as f:
        image_data = f.read()
    response = requests.post(emotion_recognition_url, headers=headers, json=image_data)
    analysis = response.json()
    print analysis