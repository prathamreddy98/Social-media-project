from flask import Flask, jsonify, request, make_response, json
from flask_restful import Resource, Api
from mongoDB import get_spotify_DB, get_reddit_DB, get_twitter_DB
from spotify import SpotifyClass
from reddit import RedditClass
from flask_cors import CORS
from results import Results


app = Flask(__name__)
CORS(app)
spotify_db = get_spotify_DB()
spotifyClass = SpotifyClass(spotify_db)
spotifyPlaylists = spotifyClass.get_playlist_names()

songs_playlist = spotifyClass.get_songs_popularity()

spotifyClass.get_single_song_pop("Thinking out Loud", "2010_track_list")

reddit_db = get_reddit_DB()
redditClass = RedditClass(reddit_db)

twitter_db = get_twitter_DB()

results = Results(reddit_db=reddit_db, twitter_db=twitter_db, spotify_db=spotify_db)

@app.route("/playlists", methods=['GET'])
def get_spotify_playlists():
    # playlists = spotifyClass.get_playlist_names()
    songs_playlist = spotifyClass.get_songs_playlists()
    response = jsonify({"songs_playlists": songs_playlist})
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

@app.route("/popularity", methods=['GET'])
def post_songs_popularity():
    songs_pop = spotifyClass.get_songs_popularity()
    response = jsonify({"songs_popularity": songs_pop})
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

@app.route("/singlepop", methods=["POST"])
def post_singlepop():
    data = request.get_json()
    # print(data)
    result = spotifyClass.get_single_song_pop(data["song"], data["playlist"])
    # json.loads(json)
    response = jsonify({"single_song_pop": result})
    response.headers.add('Access-Control-Allow-Origin', "*")
    return response

@app.route("/sentimentchart", methods=["POST"])
def song_senti():
    data = request.get_json()
    # print(data)
    if(data['song'] == "" or data['playlist'] == ""):
        return data
    res = results.song_sentiments(data['song'], data['playlist'])
    resp = jsonify(res)
    resp.headers.add('Access-Control-Allow-Origin', "*")
    return resp

@app.route("/worldcloud", methods=["POST"])
def create_wroldcloud():
    data = request.get_json()
    # print(data)
    res = results.create_worldcloud(data['playlist'])
    resp = jsonify({"artists":res})
    resp.headers.add('Access-Control-Allow-Origin', "*")
    return resp

@app.route("/numcomments", methods=["POST"])
def get_num_comments():
    data = request.get_json()
    res = results.most_comments_song(data["playlist"])
    resp = jsonify({"num_comments":res})
    resp.headers.add('Access-Control-Allow-Origin', "*")
    return resp

@app.route("/numtweets", methods=["POST"])
def get_num_tweets():
    data = request.get_json()
    res = results.most_tweets_song(data["playlist"])
    resp = jsonify({"num_tweets":res})
    resp.headers.add('Access-Control-Allow-Origin', "*")
    return resp

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)