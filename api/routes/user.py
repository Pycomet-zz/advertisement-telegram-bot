# User Resource
from config import *

users_db = api_db.users

class UserList(Resource):

    def get(self):
        result = users_db.find()
        return make_response(result)

    def post(self):
        payload = request.get_json()
        result = users_db.insert_one(payload)
        return f"New user added - {result.inserted_id}"


class User(Resource):

    def get(self, user_id):
        criteria = {'user_id': user_id}
        result = users_db.find_one(criteria)

        if result == None:
            return "No User Found!"
        else:
            return make_response(result)

    def put(self, user_id):
        criteria = {'user_id': user_id}
        new_update = { '$set': request.get_json() }

        result = users_db.update_one(
            criteria,
            new_update,
            upsert=True
        ).modified_count
        return f"{result} User Updated"

    def delete(self, user_id):
        criteria = {'user_id': user_id}

        result = users_db.delete_one(criteria).deleted_count
        return f"{result} User Deleted"