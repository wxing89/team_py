
class Reco():
    def __init__(self):
        self.rec = {}

    def set_rec(self, user, r):
        self.rec[user] = r

    def set_rec_user_item(self, user, item, score):
        self.rec[user][item] = score


user1|item1|score1
user1|item2|score2