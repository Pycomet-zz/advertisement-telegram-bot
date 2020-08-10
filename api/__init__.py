from config import *
from .routes import UserList, User, Beat

### API configurations
api_bp = Blueprint('api', __name__)
api = Api(api_bp, prefix='/api/v1')

api.add_resource(Beat, '/')
api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<user_id>')

