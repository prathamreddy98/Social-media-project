from pymongo import MongoClient

class MongoCLI:
    MONGO_URL=None
    cluster=None
    database=None
    def __init__(self, URL):
        self.MONGO_URL=URL
        self.cluster = MongoClient(self.MONGO_URL)
    
    def get_database(self,db_name):
        db = self.cluster[db_name]
        self.database=db
        return self.database


MONGO_URL="mongodb+srv://anis_agwan:8879Anish@cluster0.nholiv8.mongodb.net/?retryWrites=true&w=majority"
mongoClient = MongoCLI(MONGO_URL)
spotify_db = mongoClient.get_database('spotify_data')
reddit_db = mongoClient.get_database('final_reddit_data')
twitter_db = mongoClient.get_database('final_twitter_data')

def get_spotify_DB():
    return spotify_db

def get_reddit_DB():
    return reddit_db

def get_twitter_DB():
    return twitter_db