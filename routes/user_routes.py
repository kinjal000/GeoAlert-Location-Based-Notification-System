from flask import Blueprint
from controllers.user_controller import UserController

# Create Blueprint
user_bp = Blueprint("user_bp", __name__)

# -------------------------------
# Register User
# URL : POST /register
# -------------------------------

@user_bp.route("/register", methods=["POST"])
def register():

    return UserController.register()


# -------------------------------
# Login User
# URL : POST /login
# -------------------------------

@user_bp.route("/login", methods=["POST"])
def login():

    return UserController.login()