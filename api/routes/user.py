# User Resource
from config import *

users_db = api_db.users

class UserList(Resource):

    def get(self):
        data = users_db.find()
        result = [i for i in data]
        return make_response(result), 200

    def post(self):
        payload = request.get_json()
        result = users_db.insert_one(payload)
        return f"New user added - {result.inserted_id}", 200


class User(Resource):

    def get(self, user_id):
        criteria = {'user_id': user_id}
        result = users_db.find_one(criteria)

        if result == None:
            return "No User Found!", 405
        else:
            return make_response(result), 200

    def put(self, user_id):
        criteria = {'user_id': user_id}
        new_update = { '$set': request.get_json() }

        result = users_db.update_one(
            criteria,
            new_update,
            upsert=True
        ).modified_count
        return f"{result} User Updated", 200

    def delete(self, user_id):
        criteria = {'user_id': user_id}

        result = users_db.delete_one(criteria).deleted_count
        return f"{result} User Deleted", 200