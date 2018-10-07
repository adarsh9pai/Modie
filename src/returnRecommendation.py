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
from io import open
import http
from urlparse import urlparse
import urllib
import http.client
from pprint import pprint

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
    MovieDetails["PosterPath"] = 'http://image.tmdb.org/t/p/w500/'+(response.json()['results'][index]["poster_path"])
    MovieDetails["Title"] = (response.json()['results'][index]["title"])
    MovieDetails["Overview"] = (response.json()['results'][index]["overview"])
    MovieDetails["ReleaseDate"] = (response.json()['results'][index]["release_date"])
    MovieDetails["AverageVote"] = (response.json()['results'][index]["vote_average"])

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
    MovieDetails["Feeling"] = RecognizedMood
    #print MovieDetails
    return render_template("results.html",moviedetails = MovieDetails)
    #return jsonify(MovieDetails)


@app.route('/uploadImage', methods = ['POST'])
def upload():
    subscription_key = '93b53ddd481b41cd99828474e9c1327c'

    f = request.files['file']
    f.save(secure_filename(f.filename))
    face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'

# Set image_url to the URL of an image that you want to analyze.
    image =  open(f.filename, 'rb')
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
        }
    params = urllib.urlencode({
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'emotion'
    })
    response = requests.post(face_api_url, params=params, headers=headers,data = image)
    response = response.json()[0]["faceAttributes"]["emotion"]
    response = dict(response)
    maximumEmotion = max(response, key=response.get)
    print maximumEmotion
    os.system('rm -f '+f.filename)

    return redirect('http://localhost:5000/getValue/'+maximumEmotion)