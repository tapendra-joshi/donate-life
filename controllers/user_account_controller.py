from flask import Blueprint,jsonify,request
from constants.api_response_constants import BaseResponse,ResponseCode
from constants.hashing_constants import HashMethod,SaltKey
from helpers.hash_helper import get_hash_string
from services.user_service import UserService
from flask_login import current_user, login_user, logout_user
from config import Config

blueprint = Blueprint("user_account_controller",__name__,url_prefix="/user")

@blueprint.route("/login",methods=["POST"])
def post_login():
    if current_user.is_authenticated:
        return jsonify(BaseResponse(1, ResponseCode.SUCCESS, "User already logged in", None).to_json()), 200
    post_data = request.get_json()
    if post_data.get("email",None) and post_data.get("password",None):
        print("got email and password")
        user = UserService.find_by_email(post_data.get("email"))
        if user and (user.password_hash == get_hash_string(str(post_data.get("password"))+Config.SALT_KEY,HashMethod.SHA256)):
            print("user authenticated")
            user_data = user.to_json()
            login_user(user)
            return jsonify(BaseResponse(1, ResponseCode.SUCCESS, "User logged in successfully", user_data).to_json()), 200
    return jsonify(BaseResponse(0, ResponseCode.AUTHENTICATION_FAILED, "Authentication Failed", None).to_json()), 401


@blueprint.route("/signup",methods=["POST"])
def post_register():
    post_data = request.get_json()
    if post_data.get("email", None) and post_data.get("password", None):
        user_exists = UserService.find_by_email(post_data.get("email"))
        if user_exists:
            return jsonify(BaseResponse(0, ResponseCode.UNKNOWN_ERROR, "User already exists", None).to_json()), 409

        user = UserService.create_user(post_data)
        if user:
            return jsonify(BaseResponse(1, ResponseCode.SUCCESS, "User created successfully", user).to_json()), 200
    return jsonify(BaseResponse(0, ResponseCode.UNKNOWN_ERROR, "There was some unknown error while creating the user", None).to_json()), 500


@blueprint.route("/logout",methods=["POST"])
def post_logout():
    logout_user()
    return jsonify(BaseResponse(1, ResponseCode.SUCCESS, "User logged out successfully", None).to_json()), 200
