from repositories.users.organiser_repository import OrganiserRepository
import uuid
from constants.hashing_constants import HashMethod
from helpers.hash_helper import get_hash_string
from datetime import datetime,timedelta
from exceptions import UserAlreadyExistsError

class OrganiserService:

    @staticmethod
    def create_organiser(organiser_data=None,formatted=False):
        try:
            if organiser_data:
                
                organiser_email_exists = OrganiserRepository.find_by_email(organiser_data.get("email",None))
                organiser_name_exists = OrganiserRepository.find_by_name(organiser_data.get("organiser_name",None))
                
                if (organiser_email_exists is not None):
                    raise UserAlreadyExistsError("Organiser already exists with same email.")

                if  (organiser_name_exists is not None):
                    raise UserAlreadyExistsError("Organiser already exists wiith same name.")

                organiser = OrganiserRepository.create_organiser(organiser_data)
                if organiser:
                    if formatted:
                        organiser_json = organiser.to_json()
                        return organiser_json
                    return organiser
            return None
        except UserAlreadyExistsError as userError:
            #do logging here
            raise userError


    @staticmethod
    def update_organiser(organiser,organiser_data=None):

        return OrganiserRepository.update_organiser(organiser,organiser_data)


    @staticmethod
    def find_by_id(id,formatted=False):
        if id:
            organiser = OrganiserRepository.find_by_id(id)
            if organiser:
                if formatted:
                    organiser_json = organiser.to_json()
                    return organiser_json()
                return organiser
        return None

    @staticmethod
    def get_all_organisers(formatted=False):
        organisers = OrganiserRepository.get_all_organisers(formatted)
        return organisers

    @staticmethod
    def find_by_email(email=None,formatted=False):
        if not email:
            return None
        organiser = OrganiserRepository.find_by_email(email)
        if not organiser:
            return None
        if formatted:
            return organiser.to_json()

        return organiser

    
    @staticmethod
    def initiate_forget_password(email, send_email=False):
        """
        Initiates forget password formalities
        :param email: the registered email of the user
        :param send_email: bool ; if the forget password email is to be sent
        :return: reset_password_code if successful; else None
        """
        if email:
            organiser = OrganiserService.find_by_email(email)
            reset_password_code = None
            if organiser.reset_password_code and organiser.reset_password_code_expiry > datetime.now():
                reset_password_code = organiser.reset_password_code
            else:
                reset_password_code = str(uuid.uuid4())
            OrganiserService.update_user(organiser, {
                "reset_password_code": reset_password_code,
                "reset_password_code_expiry": datetime.now() + timedelta(hours=2)
            })
            if send_email:
                OrganiserService.__send_forget_password_email__(organiser)
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
        organiser = OrganiserService.find_by_email(email)
        if organiser and organiser.reset_password_code == reset_password_code:
            organiser_data = {
                "password_hash": get_hash_string(new_password, HashMethod.SHA256),
                "reset_password_code": None,
                "reset_password_code_expiry": None,
            }
            OrganiserService.update_organiser(organiser, organiser_data)
            return True
        return False

    @staticmethod
    def decode_auth_token(authentication_token):
        """
        Decodes an Auth Token to get user_identity
        :param authentication_token:
        :return: user_entity
        """
        return OrganiserRepository.decode_authentication_token(authentication_token)


    

    


