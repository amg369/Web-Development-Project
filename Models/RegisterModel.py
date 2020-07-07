import pymongo
from pymongo import MongoClient
import bcrypt


class RegisterModel:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.bonesfan
        self.Users = self.db.users

    def add_user(self, data):
        hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt())
        uid = self.Users.insert({"username": data.username, "name": data.name, "password": data.password})
        myuser = self.Users.find_one({"username": data.username})
        print("uid is", uid)
        if bcrypt.checkpw("avocado1".encode(), myuser["password"]):
            print("this matches")
