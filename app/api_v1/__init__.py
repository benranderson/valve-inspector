from flask import Blueprint
from ..auth import auth

api = Blueprint('api', __name__)

@api.before_request
@auth.login_required
def before_request():
    """All routes in this blueprint require authentication."""
    pass

from . import valves, logs, errors
