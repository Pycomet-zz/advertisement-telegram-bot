# User Resource
from config import *

users_db = api_db.users

class UserList(Resource):

    def get(self):
        return "It works Bitch!"

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass