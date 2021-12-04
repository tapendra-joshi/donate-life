import datetime
from sqlalchemy_utils import ChoiceType
from models.database import IndexedTimestampModel,db,Column
from constants.user_constants import UserStatus,UserVerificationStatus
from constants.hashing_constants import HashMethod
from helpers.hash_helper import get_hash_string
import jwt
from flask import current_app


class OrganiserModel(IndexedTimestampModel):
    __tablename__ = "organiser"

    id = Column(db.BigInteger, primary_key=True, autoincrement=True, nullable=False,index=True)
    organiser_name = db.Column(db.String(255),unique=True, nullable=False)
    email = db.Column(db.String(255),unique=True, nullable=False)
    password_hash = db.Column(db.String(65),nullable=False)
    reset_password_code = db.Column(db.String(255), nullable=True, default=None, index=True)
    reset_password_expiry = db.Column(db.DateTime, nullable=True,default=(datetime.datetime.utcnow() + datetime.timedelta(hours=2)))
    phone_number = db.Column(db.String(15),nullable=False)
    street1 = db.Column(db.String(65),nullable=True,index=True)
    street2 = db.Column(db.String(65),nullable=True,index=True)
    city = db.Column(db.String(65),nullable=False,index=True)
    state = db.Column(db.String(65), nullable=False,index=True)
    country = db.Column(db.String(65),nullable=False,default="India",index=True)
    verification_status = db.Column(ChoiceType(UserVerificationStatus), nullable=False, default=UserVerificationStatus.UNVERIFIED)
    verification_code = db.Column(db.String(255), nullable=True, default=None, index=True)
    status = db.Column(ChoiceType(UserStatus),nullable=False, default= UserStatus.ACTIVE)

    organiser = db.relationship('EventModel', backref='organiser', lazy=True,uselist=False)

    def to_json(self):

        status_value = None
        if self.status:
            status_value = self.status.value

        verification_status_value = None
        if self.verification_status:
            verification_status_value = self.verification_status.value


        return{
            "id":self.id,
            "organiser_name":self.organiser_name,
            "status":status_value,
            "street1":self.street1,
            "street1":self.street1,
            "city":self.city,
            "phone_number":self.phone_number,
            "state":self.state,
            "verification_status":verification_status_value,
            "email":self.email,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "last_updated_at": self.last_updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            
            payload = {
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=20, seconds=5),
                "iat": datetime.datetime.utcnow(),
                "sub": {
                    "id": self.id,
                    "phone_number": self.phone_number,
                    "status": self.status.value,
                    "verification_status": self.verification_status.value,
                }
            }
            return jwt.encode(
                payload,
                current_app.config.get("APP_SECRET"),
                algorithm="HS256"
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get("APP_SECRET"), algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

