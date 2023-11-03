
class SpotifyClass:
    spotify_db = None

    def __init__(self, spotifyDB) -> None:
        self.spotify_db = spotifyDB

    def get_playlist_names(self) -> list:
        return self.spotify_db.list_collection_names()

    def get_songs_popularity(self) -> dict:
        spotify_cols_names = self.spotify_db.list_collection_names()
        # print(spotify_cols_names)
        spotify_song_popularity = {}
        popularity = []
        for cols in spotify_cols_names:
            colection = self.spotify_db[cols]
            curs = colection.find({}, {'track': 1})
            songs_list = []
            pos_list = []
            for c in curs:
                songs_list.append(c['track']['name'])
                pos_list.append(c['track']['popularity'])
                if c['track']['name'] not in spotify_song_popularity:
                    spotify_song_popularity[c['track']['name']] = c['track']['popularity']   
                    song_popu = {"playlist": cols, "song": c['track']['name'], "popularity": c["track"]["popularity"]}
                    popularity.append(song_popu)

        return popularity

    def get_songs_playlists(self):
        spotify_cols_names = self.spotify_db.list_collection_names()
        # print(spotify_cols_names)
        # print(spotify_cols_names[0])
        # colection = self.spotify_db[spotify_cols_names[0]]
        # curs = colection.distinct('track.name')
        # print(curs)

        spotify_song_playlist = []
        for cols in spotify_cols_names:
            colection = self.spotify_db[cols]
            # curs = colection.find({}, {"_id": 0, "track": {"name": 1}})
            songs_list = colection.distinct('track.name')
            playlist = {"name": cols, "songs": songs_list}
            # if cols not in spotify_song_playlist:
            #     spotify_song_playlist[cols] = songs_list  
            spotify_song_playlist.append(playlist)

        return spotify_song_playlist

    def get_single_song_pop(self, song_name:str, playlist_name:str):
        coll = self.spotify_db[playlist_name]
        # obj = ObjectId("6361b8487d23150c71cae470")
        curs = coll.find({"track.name": song_name}, {"_id":0})
        return curs[0]
