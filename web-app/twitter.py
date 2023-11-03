from mongoDB import get_twitter_DB
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("spacytextblob")


class TwitterClass:
    def __init__(self, twitter_db):
        self.twitter_db = twitter_db

    def get_collection_names(self):
        return self.twitter_db.list_collection_names()

    def get_twitter_song_sentiment(self, song):
        collections = self.get_collection_names()
        if song not in collections:
            return 0

        col = self.twitter_db[song]
        results = col.find({})
        pos_count=0
        neg_count=0
        neu_count=0
        for c in results:
            do = nlp(c['text'])
            if do._.blob.polarity > 0.0:
                pos_count += 1
            elif do._.blob.polarity < 0.0:
                neg_count += 1
            else:
                neu_count += 1
        # print(pos_count, neg_count, neu_count)

        avg_pos = (pos_count / (pos_count+neg_count+neu_count)) * 100
        avg_neg = (neg_count / (pos_count+neg_count+neu_count)) * 100
        avg_neu = (neu_count / (pos_count+neg_count+neu_count)) * 100

    

        #Average positive review
        return {"avg_pos": avg_pos, "avg_neg": avg_neg, "avg_neu": avg_neu}


    def most_song_comment(self):
        collections = self.get_collection_names()

        most_count = []
        for col in collections:
            co = self.twitter_db[col]
            dic_most = {"song": col, "number_of_tweets": co.count_documents({})}
            most_count.append(dic_most)

        # print(sorted(most_count, key=lambda i: (i['number_of_comments']), reverse=True)[:5])

        return sorted(most_count, key=lambda i: (i['number_of_tweets']), reverse=True)

#     # def get_song_twitter_collection(self, song):
#     #     cols = self.get_collection_names()
#     #     return self.twitter_db[song] if song in cols else None

#     # def get_song_tweets(self, coll):
#     #     results = coll.find({})
#     #     return results

#     # def get_tweet_reviews(self, results):
#     #     pos_count=0
#     #     neg_count=0
#     #     neu_count=0
#     #     for c in results:
#     #         do = nlp(c['text'])
#     #         if do._.blob.polarity > 0.0:
#     #             pos_count += 1
#     #         elif do._.blob.polarity < 0.0:
#     #             neg_count += 1
#     #         else:
#     #             neu_count += 1
#     #     print(pos_count, neg_count, neu_count)

#     #     #Average positive review
#     #     if pos_count > neg_count and pos_count > neu_count:
#     #         pos_avg = (pos_count / (pos_count+neg_count+neu_count)) * 100
#     #         print(pos_avg)
#     #         return pos_avg


# twitter_db = get_twitter_DB()
# twitterClass = TwitterClass(twitter_db)
# # colls = twitterClass.get_collection_names()
# # col = twitterClass.get_song_twitter_collection('Anti-Hero')
# # res = twitterClass.get_song_tweets(col)

# # twitterClass.get_tweet_reviews(res)

# print(twitterClass.get_twitter_song_sentiment("Anti-Hero"))