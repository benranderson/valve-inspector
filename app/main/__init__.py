from flask import Blueprint
# from ..auth import auth_token

main = Blueprint('main', __name__)

# @main.before_request
# @auth_token.login_required
# def before_request():
#     """All routes in this blueprint require authentication."""
#     pass

from . import views
