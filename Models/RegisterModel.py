from pymongo import MongoClient


class RegisterModel:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.Bones
        self.Users = self.db.users

    def insert_user(self, data):
        useid = self.Users.insert(
            {"username": data.username, "name": data.name, "password": data.password, "email": data.email})
        print("uid is", useid)
