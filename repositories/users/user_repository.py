from models.users.user_model import UserModel
from constants.user_constants import UserSex,BloodGroup,UserStatus,UserVerificationStatus
from constants.hashing_constants import HashMethod
from helpers.hash_helper import get_hash_string
from extentions.extentions import login_manager
from config import Config


class UserRepository:

    @staticmethod
    def create_user(user_data=None):
        if user_data:
            password = get_hash_string(str(user_data.get('password'))+ Config.SALT_KEY,HashMethod.SHA256)
            user = UserModel(
                email = user_data.get('email'),
                password_hash = password,
                first_name = user_data.get('first_name'),
                last_name = user_data.get('last_name'),
                sex = user_data.get('sex'),
                blood_group = user_data.get('blood_group'),
                city = user_data.get('city'),
                state = user_data.get('state'),
                country = user_data.get('country',"India"),
                birth_date = user_data.get('birth_date')
            )
            user.verification_code = user_data.get('verification_code',None)
            user.save()
            return user
        return None

    @staticmethod
    def update_user(user, user_data=None):
        if user_data:
            user_attributes = list(user.__dict__.keys())
            for user_data_key, user_data_value in user_data.items():
                if user_data_key in user_attributes:
                    setattr(user, user_data_key, user_data_value)
            user.save()
            return user
        return None
    
    @staticmethod
    def find_by_email(email):
        if not email:
            return None
        user = UserModel.query.filter_by(email=email).first()
        if user:
            return user

        return None

    @staticmethod
    def find_by_id(id):
        user = UserModel.query.filter_by(id=id).first()
        if user:
            return user
        return None

    @staticmethod
    def decode_authentication_token(authentication_token):
        """
                Decodes an Auth Token to get user_identity
                :param authentication_token:
                :return: user_entity
                """
        return UserModel.decode_auth_token(authentication_token)


    @staticmethod
    def find_by_verification_code(verification_code):
        return UserModel.query.filter_by(verification_code=verification_code).first()


