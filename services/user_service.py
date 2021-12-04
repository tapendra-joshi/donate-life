from repositories.users.user_repository import UserRepository
from constants.user_constants import UserStatus 
from constants.hashing_constants import HashMethod
import uuid
from helpers.hash_helper import get_hash_string
from datetime import datetime,timedelta


class UserService:

    @staticmethod
    def create_user(user_data):
        
        existing_user = UserService.find_by_email(user_data.get('email'))
        if existing_user:
            return None

        user_data["verification_code"] = str(uuid.uuid4())
        user = UserRepository.create_user(user_data)
        if user:
            return user.to_json()

        return None


    @staticmethod
    def find_by_email(email=None,formatted=False):

        if not email:
            return None

        user = UserRepository.find_by_email(email)
        
        if not user:
            return None
        
        if formatted:
            return user.to_json()

        return user


    @staticmethod
    def update_user(user, user_data=None):
        """
        Updates a user
        :param user: User object
        :param user_data: dict of fields to be updated
        :return: upated user object if the update is successful; else None
        """
        return UserRepository.update_user(user, user_data)

    @staticmethod
    def verify_email(verification_code):
        """
        Verifies a User by its verification code sent over the email
        :param verification_code:
        :return: boolean if the user has been verified or not
        """
        user = UserRepository.find_by_verification_code(verification_code)
        if user:
            UserService.update_user(user, {
                "status": UserStatus.ACTIVE,
                "verification_code": None,
            })
            return True
        return False

    @staticmethod
    def initiate_forget_password(email, send_email=False):
        """
        Initiates forget password formalities
        :param email: the registered email of the user
        :param send_email: bool ; if the forget password email is to be sent
        :return: reset_password_code if successful; else None
        """
        if email:
            user = UserService.find_by_email(email)
            reset_password_code = None
            if user.reset_password_code and user.reset_password_code_expiry > datetime.now():
                reset_password_code = user.reset_password_code
            else:
                reset_password_code = str(uuid.uuid4())
            UserService.update_user(user, {
                "reset_password_code": reset_password_code,
                "reset_password_code_expiry": datetime.now() + timedelta(hours=2)
            })
            if send_email:
                UserService.__send_forget_password_email__(user)
            return reset_password_code
        return False
    

    @staticmethod
    def __send_registration_verification_email__(user):
        to_data = [
            {
                "email": user.email,
            }
        ]
        return None
        # template_data = {
        #     "confirmation_link": (current_app.config.get("WEB_APP_URL") + UserService.WEB_APP_EMAIL_VERIFICATION_PATH + user.verification_code + "/"),
        # }
        # return NotificationService.send_email(to_data=to_data, template_id=UserService.SENDGRID_EMAIL_VERIFICATION_TEMPLATE_ID, template_data=template_data)

    @staticmethod
    def __send_forget_password_email__(user):
        to_data = [
            {
                "email": user.email,
            }
        ]
        return None
        # template_data = {
        #     "reset_password_link": (current_app.config.get("WEB_APP_URL") + UserService.WEB_APP_RESET_PASSWORD_PATH + "?reset_password_code=" + getattr(user, "reset_password_code", "")),
        # }
        # return NotificationService.send_email(to_data=to_data, template_id=UserService.SENDGRID_RESET_PASSWORD_TEMPLATE_ID, template_data=template_data)

    @staticmethod
    def reset_password(email, reset_password_code, new_password):
        """
        Resets a user password
        :param email: the registered email of the user
        :param reset_password_code: the reset password code associated with the user
        :param new_password: the new password string
        :return: bool ; if the operation was successful or not
        """
        user = UserService.find_by_email(email)
        if user and user.reset_password_code == reset_password_code:
            user_data = {
                "password_hash": get_hash_string(new_password, HashMethod.SHA256),
                "reset_password_code": None,
                "reset_password_code_expiry": None,
            }
            UserService.update_user(user, user_data)
            return True
        return False

    @staticmethod
    def decode_auth_token(authentication_token):
        """
        Decodes an Auth Token to get user_identity
        :param authentication_token:
        :return: user_entity
        """
        return UserRepository.decode_authentication_token(authentication_token)

