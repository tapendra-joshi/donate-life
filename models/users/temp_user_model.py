import datetime
from sqlalchemy_utils import ChoiceType
from models.database import IndexedTimestampModel,db,Column
from constants.user_constants import UserSex,BloodGroup
from flask_login import UserMixin


class TempUserModel(UserMixin,IndexedTimestampModel):
    __tablename__ = "temp_life_users"

    id = Column(db.BigInteger, primary_key=True, autoincrement=True, nullable=False)
    blood_group = db.Column(ChoiceType(BloodGroup),nullable=False)
    first_name = db.Column(db.String(255),nullable=False)
    last_name = db.Column(db.String(255),nullable=False)
    phone_number = db.Column(db.String(15),nullable=False)
    sex = db.Column(ChoiceType(UserSex),nullable=False,default=UserSex.UNSPECIFIED)
    birth_date = db.Column(db.Date,nullable=False)
    city = db.Column(db.String(65),nullable=False,index=True)
    state = db.Column(db.String(65), nullable=False,index=True)
    country = db.Column(db.String(65),nullable=False,default="India",index=True)
    email = db.Column(db.String(255),unique=False, nullable=False)
    


    def to_json(self):

        
        
        blood_group_value = None
        if self.blood_group:
            blood_group_value = self.blood_group.value
        
        sex_value = None
        if self.sex:
            sex_value = self.sex.value
        
        
        return{
            "id":self.id,
            "first_name":self.first_name,
            "last_name":self.last_name,
            "blood_group":blood_group_value,
            "sex":sex_value,
            "city":self.city,
            "state":self.state,
            "email":self.email,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "last_updated_at": self.last_updated_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
