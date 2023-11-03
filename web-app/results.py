from spotify import SpotifyClass
from reddit import RedditClass
from twitter import TwitterClass
from mongoDB import get_reddit_DB, get_spotify_DB, get_twitter_DB
import matplotlib.pyplot as plt
import numpy as np
import base64

class Results:

    def __init__(self, reddit_db, twitter_db, spotify_db):
        self.reddit_db = reddit_db
        self.twitter_db = twitter_db
        self.spotify_db = spotify_db

        self.twitterClass = TwitterClass(self.twitter_db)
        self.redditClass = RedditClass(self.reddit_db)
        self.spotifyClass = SpotifyClass(self.spotify_db)

    def song_sentiments(self, song, playlist):
        reddit_count = self.redditClass.get_reddit_song_sentiment(song)
        twitter_count = self.twitterClass.get_twitter_song_sentiment(song)
        spotify_popularity = self.spotifyClass.get_single_song_pop(song, playlist)

        popularity = spotify_popularity['track']['popularity']

        return {"twitter_count": twitter_count, "reddit_count": reddit_count, "spotify_popularity": popularity}

    def create_song_arr(self, playlist):
        docs = self.spotify_db[playlist].find({})

        return [doc["track"]["name"] for doc in docs]

    def create_colls_arr(self):
        collections = self.spotify_db.list_collection_names()
        
        return collections

    def create_colls_dict(self, arr):
        new = {}
        for ar in arr:
            ant = resultClass.create_song_arr(ar)
            if ar not in new:
                new[ar] = ant

        return new

    def most_tweets_song(self, playlist):
        tweets_arr = self.twitterClass.most_song_comment()
        counter = 0
        comments = []
        song_ar = self.create_song_arr(playlist)

        for i in range(len(tweets_arr)):
            if tweets_arr[i]["song"] in song_ar and counter < 5:
                # print(comments_arr[i])
                comments.append(tweets_arr[i])
                counter += 1

        return comments        

    def most_comments_song(self, playlist):
        comments_arr = self.redditClass.most_song_comment()

        counter = 0
        comments = []
        song_ar = self.create_song_arr(playlist)

        for i in range(len(comments_arr)):
            if comments_arr[i]["song"] in song_ar and counter < 5:
                # print(comments_arr[i])
                comments.append(comments_arr[i])
                counter += 1

        return comments


    def create_worldcloud(self, playlist):
        playlist_coll = self.spotify_db[playlist]
        playlist_cur = playlist_coll.find({}, {"_id":0, "track.artists":1})

        song_count = {}

        for song in playlist_cur:
            # print(song)
            artists = song['track']['artists']
            if (len(artists)) > 1:
                for i in range(len(artists)):
                    if artists[i]['name'] not in song_count:
                        song_count[artists[i]['name']] = 1
                    else:
                        song_count[artists[i]['name']] += 1

            else:
                if artists[0]['name'] not in song_count:
                    song_count[artists[0]['name']] = 1
                else:
                    song_count[artists[0]['name']] += 1

        # print(song_count)

        songs_list = []

        for artist, count in song_count.items():
            songs_list.append({"value":artist, "count":count})

        # print(songs_list)
        return songs_list


    # def chart_create(self, song ,twitter_count, reddit_count, spotify_count):
    #     col_names = ['twitter','reddit', 'spotify']
    #     pops = [twitter_count, reddit_count, spotify_count]
    #     fig = plt.figure(figsize = (5, 5))
    #     plt.bar(col_names, pops, color="maroon", width = 0.5)
    #     plt.title(song)
    #     plt.yticks(np.arange(0, 100, 5))
    #     # plt.savefig(song+".png")

    #     with open("Anti-Hero.png", "rb") as img:
    #         string = base64.b64encode(img.read()).decode("utf-8")
        


# twitter_db = get_twitter_DB()
# reddit_db = get_reddit_DB()
# spotify_db = get_spotify_DB()

# resultClass = Results(reddit_db=reddit_db, twitter_db=twitter_db, spotify_db=spotify_db)

# resultClass.create_worldcloud("tracks_list")

# # resultClass.create_song_arr("tracks_list")

# # arr = resultClass.create_colls_arr()

# # dics = resultClass.create_colls_dict(arr)

# resultClass.most_comments_song("tracks_list")
# redditClass = RedditClass(reddit_db)

# dict_com = redditClass.most_song_comment()


# resultClass.chart_create("Anti-Hero", 5, 6, 7)