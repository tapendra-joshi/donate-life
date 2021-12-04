from flask import Blueprint, jsonify, request
from flask.globals import current_app

from constants.api_response_constants import BaseResponse, ResponseCode
from constants.hashing_constants import HashMethod
from constants.user_constants import UserStatus
from exceptions import UserAlreadyExistsError
from helpers.hash_helper import get_hash_string
from services.organiser_service import OrganiserService
from config import Config

blueprint = Blueprint("acount_blueprint", __name__, url_prefix="/account/organiser")

@blueprint.route("/register/", methods=["POST"])
@blueprint.route("/register", methods=["POST"])
def post_register():
    """
    Register a new Organiser Account
    :return: new organiser data
    """
    try:
        post_data = request.get_json()
        if post_data.get("email", None) and post_data.get("password", None):

            organiser = OrganiserService.create_organiser(post_data,formatted=True)
            if organiser:
                return jsonify(BaseResponse(1, ResponseCode.SUCCESS, "Organiser created successfully", organiser).to_json()), 200
            return jsonify(BaseResponse(0, ResponseCode.UNKNOWN_ERROR, "There was some unknown error while creating the organiser", None).to_json()), 500
        return jsonify(BaseResponse(0, ResponseCode.UNKNOWN_ERROR, "Either email or password not provided.", None).to_json()), 500
    except UserAlreadyExistsError as error:
        return jsonify(BaseResponse(0, ResponseCode.INVALID_REQUEST_DATA, error.message, None).to_json()), 500

@blueprint.route("/login/", methods=["POST"])
@blueprint.route("/login", methods=["POST"])
def post_login():
    """
    Login into an existing Organiser Account
    :return: Organiser Account Details along with auth_token
    """
    post_data = request.get_json()
    if post_data.get("email", None) and post_data.get("password", None):
        organiser = OrganiserService.find_by_email(post_data.get("email"))
        if organiser and organiser.password_hash == get_hash_string(str(post_data.get("password")+ current_app.config.get('SALT_KEY')),HashMethod.SHA256) and organiser.status == UserStatus.ACTIVE:
            organiser_data = organiser.to_json()
            organiser_data["auth_token"] = organiser.encode_auth_token()
            return jsonify(BaseResponse(1, ResponseCode.SUCCESS, "Organiser logged in successfully", organiser_data).to_json()), 200
    return jsonify(BaseResponse(0, ResponseCode.AUTHENTICATION_FAILED, "Authentication Failed", None).to_json()), 401


@blueprint.route("/logout/", methods=["GET"])
def post_logout():
    #need to invalidate token before log out

    return jsonify(BaseResponse(1, ResponseCode.SUCCESS, "Organiser logged out successfully", None).to_json()), 200


@blueprint.route("/email-verification/", methods=["POST"])
def post_email_verification():
    post_content = request.get_json()
    verification_code = post_content.get("verification_code", None)

    if verification_code:
        verification_result = OrganiserService.verify_email(verification_code)
        if verification_result:
            return jsonify(
                BaseResponse(1, ResponseCode.SUCCESS, "Email has been verified successfully.", None).to_json()), 200

    return jsonify(
        BaseResponse(0, ResponseCode.EMAIL_VERIFICATION_FAILED, "Email Verification failed.", None).to_json()), 500


@blueprint.route("/forget-password/", methods=["POST"])
def post_forget_password():
    post_content = request.get_json()
    email = post_content.get("email")
    send_email = post_content.get("send_email", False)
    reset_password_code = OrganiserService.initiate_forget_password(email, send_email)
    if reset_password_code:
        return jsonify(BaseResponse(1, ResponseCode.SUCCESS, "Forget Password formalitites initiated successfully", {
            "reset_password_code": reset_password_code,
        }).to_json()), 200
    return jsonify(
        BaseResponse(0, ResponseCode.UNKNOWN_ERROR, "Cannot initiate forget password formalities", None).to_json()), 500


@blueprint.route("/reset-password/", methods=["POST"])
def post_reset_password():
    post_content = request.get_json()
    email = post_content.get("email")
    new_password = post_content.get("password")
    reset_password_code = post_content.get("reset_password_code")
    reset_password_status = OrganiserService.reset_password(email, reset_password_code, new_password)
    if reset_password_status:
        return jsonify(BaseResponse(1, ResponseCode.SUCCESS, "Password has been reset successfully", None).to_json()), 200
    return jsonify(BaseResponse(0, ResponseCode.UNKNOWN_ERROR, "Cannot reset password with provided credentials", None).to_json()), 500

