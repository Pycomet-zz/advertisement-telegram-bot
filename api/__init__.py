from flask import Blueprint
from .routes import UserList

### API configurations
api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix='api/v1')

api.add_resource(Beat, '/')
api.add_resource(UserList, '/users')

