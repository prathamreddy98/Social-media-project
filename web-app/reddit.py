from mongoDB import get_reddit_DB
import pymongo

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("spacytextblob")


class RedditClass:
    def __init__(self, reddit_db):
        self.reddit_db = reddit_db

    def get_collection_names(self):
        return self.reddit_db.list_collection_names()

    def get_reddit_song_sentiment(self, song):
        collections = self.get_collection_names()
        if song not in collections:
            return 0

        col = self.reddit_db[song]
        results = col.find({})
        pos_count=0
        neg_count=0
        neu_count=0
        for c in results:
            do = nlp(c['comment'])
            if do._.blob.polarity > 0.0:
                pos_count += 1
            elif do._.blob.polarity < 0.0:
                neg_count += 1
            else:
                neu_count += 1
        # print(pos_count, neg_count, neu_count)

        #Average positive review
        avg_pos = (pos_count / (pos_count+neg_count+neu_count)) * 100
        avg_neg = (neg_count / (pos_count+neg_count+neu_count)) * 100
        avg_neu = (neu_count / (pos_count+neg_count+neu_count)) * 100


        #Average positive review
        return {"avg_pos": avg_pos, "avg_neg": avg_neg, "avg_neu": avg_neu}

    def most_song_comment(self):
        collections = self.get_collection_names()

        most_count = []
        for col in collections:
            co = self.reddit_db[col]
            dic_most = {"song": col, "number_of_comments": co.count_documents({})}
            most_count.append(dic_most)

        # print(sorted(most_count, key=lambda i: (i['number_of_comments']), reverse=True)[:5])

        return sorted(most_count, key=lambda i: (i['number_of_comments']), reverse=True)
    # def get_song_reddit_collection(self, song):
    #     cols = self.get_collection_names()
    #     if song in cols:
    #         print(True)
    #         return self.reddit_db[song]
    #     else:
    #         print(False)
    #         return None

    # def get_song_comments(self, coll):
    #     results = coll.find({})
    #     return results

    # def get_comment_reviews(self, results):
    #     pos_count=0
    #     neg_count=0
    #     neu_count=0
    #     for c in results:
    #         do = nlp(c['comment'])
    #         if do._.blob.polarity > 0.0:
    #             pos_count += 1
    #         elif do._.blob.polarity < 0.0:
    #             neg_count += 1
    #         else:
    #             neu_count += 1
    #     print(pos_count, neg_count, neu_count)

    #     #Average positive review
    #     if pos_count > neg_count and pos_count > neu_count:
    #         pos_avg = (pos_count / (pos_count+neg_count+neu_count)) * 100

    #         return pos_avg

        # # Average negative review
        # if neg_count > pos_count and neg_count > neu_count:
        #     neg_avg = (neg_count / (pos_count+neg_count+neu_count)) * 100
        #     print(neg_avg)

# red_db = get_reddit_DB()

# redditClass = RedditClass(red_db)

# redditClass.most_song_comment()

# # colls = redditClass.get_collection_names()

# # col = redditClass.get_song_reddit_collection("Anti-Hero")

# # res = redditClass.get_song_comments(col)

# # redditClass.get_comment_reviews(res)

# print(redditClass.get_reddit_song_sentiment("Anti-Hero"))

# # for c in colls:
# #     song = "Africa"
# #     if c == song:
# #         cc = red_db[song]
# #         res = cc.find({})
# #         for j in res:
# #             print(j)
