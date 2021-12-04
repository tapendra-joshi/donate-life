import datetime
from models.database import IndexedTimestampModel,db,Column,Model
from constants.user_constants import IndianStates
from sqlalchemy_utils import ChoiceType
import json

class BloodBankModel(IndexedTimestampModel):
    __tablename__ = "blood_banks"
    
    
    id = Column(db.BigInteger,primary_key=True,autoincrement=True,nullable=False)
    name = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(255),nullable=True)
    address = db.Column(db.String(255),nullable=False)
    city = db.Column(db.String(65),nullable=False,index=True)
    state = db.Column(db.String(255), nullable=False,index=True)
    district = db.Column(db.String(65),index=True)
    pincode = db.Column(db.BigInteger,nullable=True,index=True)
    country = db.Column(db.String(65),nullable=False,default="India",index=True)
    blood_stock_id = db.Column(db.BigInteger,db.ForeignKey('blood_stock.id'),nullable=False)
    latitude = db.Column(db.Numeric(10,8),nullable=True,index=True)
    longitude = db.Column(db.Numeric(11,8),nullable=True,index=True)
    contact_number = db.Column(db.String(65),nullable=True)
    mobile_number = db.Column(db.BigInteger,nullable=True)

    blood_stock_relation = db.relationship(
        "BloodStock", foreign_keys=[blood_stock_id])


    # def __init__(self,name,email,state,country,address,blood_stock_id,city):
        
    #     self.email = email
    #     self.name = name
    #     self.address = address
    #     self.district = district
    #     self.pincode = pincode
    #     self.city = city
    #     self.state = state
    #     self.city = city
    #     self.country = country
    #     self.blood_stock_id = blood_stock_id

    def to_json(self):
        blood_stock_obj = BloodStock.query.filter_by(id=self.blood_stock_id).first()
        return {
            "id" : self.id,
            "name" : self.name,
            "email" : self.email,
            "address" : self.address,
            "city":self.city,
            "state" : self.state,
            "country" : self.country,
            "district" : self.district,
            "latitude" : '{}'.format(self.latitude),
            "longitude" : '{}'.format(self.longitude),
            "pincode" : self.pincode,
            "contact_number" : self.contact_number,
            "mobile_number" : self.mobile_number,
            "blood_stock" : {
                "ab_positive":blood_stock_obj.ab_positive,
                "ab_negative":blood_stock_obj.ab_negative,
                "a_positive":blood_stock_obj.a_positive,
                "a_negative":blood_stock_obj.a_negative,
                "b_positive":blood_stock_obj.b_positive,
                "o_positive":blood_stock_obj.o_positive,
                "o_negative":blood_stock_obj.o_negative
            }
        }


class BloodStock(Model):
    __tablename__="blood_stock"

    id = Column(db.BigInteger,primary_key=True,autoincrement=True,nullable=False)
    ab_positive = db.Column(db.BigInteger,default=0,nullable=False,index=True)
    ab_negative = db.Column(db.BigInteger,default=0,nullable=False,index=True)
    a_positive = db.Column(db.BigInteger,default=0,nullable=False,index=True)
    a_negative = db.Column(db.BigInteger,default=0,nullable=False,index=True)
    b_positive = db.Column(db.BigInteger,default=0,nullable=False,index=True)
    b_negative = db.Column(db.BigInteger,default=0,nullable=False,index=True)
    o_positive = db.Column(db.BigInteger,default=0,nullable=False,index=True)
    o_negative = db.Column(db.BigInteger,default=0,nullable=False,index=True)

    # blood_bank_stock_rel = db.relationship('BloodBankModel',backref='BloodStock')
