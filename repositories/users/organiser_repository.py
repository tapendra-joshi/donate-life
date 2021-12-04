from operator import setitem
from pdb import set_trace
from models.users.organiser_model import OrganiserModel
from helpers.hash_helper import get_hash_string
from config import Config
from constants.hashing_constants import HashMethod

class OrganiserRepository:

    @staticmethod
    def create_organiser(organiser_data=None):
        # import pdb;pdb.set_trace();
        if organiser_data:
            password_hash = get_hash_string(str(organiser_data.get('password'))+ Config.SALT_KEY,HashMethod.SHA256)
            organiser = OrganiserModel(
                email=organiser_data.get("email"),
                password_hash = password_hash,
                organiser_name = organiser_data.get("organiser_name"),
                phone_number = organiser_data.get("phone_number",None),
                street1 = organiser_data.get("street1",None),
                street2 = organiser_data.get("street2",None),
                city = organiser_data.get("city"),
                state = organiser_data.get("state"),
                country = organiser_data.get("country","India")
            )
            organiser.save()
            return organiser
        return None

    @staticmethod
    def update_organiser(organiser,organiser_data=None):
        if organiser_data:
            organiser_attributes = list(organiser.__dict__.keys())
            for organiser_data_key, organiser_data_value in organiser_data.items():
                if organiser_data_key in organiser_attributes:
                    setattr(organiser, organiser_data_key, organiser_data_value)
            organiser.save()
            return organiser
        return None

    @staticmethod
    def find_by_id(id=None):
        if not id:
            return None
        organiser = OrganiserModel.query.filter_by(id=id).first()
        if organiser:
            return organiser
        return None

    
    @staticmethod
    def find_by_name(name=None):
        if not name:
            return None
        organiser = OrganiserModel.query.filter_by(organiser_name=name).first()
        print(organiser)
        if organiser:
            return organiser
        return None


    @staticmethod
    def get_all_organisers(formatted=False):
        organisers = OrganiserModel.query.all()
        if organisers:
            if not formatted:
                return organisers
            organisers_data={}
            for organiser in organisers:
                organisers_data[organiser.id]=organiser.to_json()
            return organisers_data
        return None

    @staticmethod
    def find_by_email(email=None):
        # import pdb;pdb.set_trace()
        if not email:
            return None
        organiser = OrganiserModel.query.filter_by(email=email).first()
        if organiser:
            return organiser
        return None

    @staticmethod
    def decode_authentication_token(authentication_token):
        """
                Decodes an Auth Token to get user_identity
                :param authentication_token:
                :return: user_entity
                """
        return OrganiserModel.decode_auth_token(authentication_token)


    @staticmethod
    def find_by_verification_code(verification_code):
        return OrganiserModel.query.filter_by(verification_code=verification_code).first()


    


            


    



