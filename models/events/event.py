from models.database import IndexedTimestampModel,db,Column
from models.users.organiser_model import OrganiserModel
import json
import datetime


class EventModel(IndexedTimestampModel):
    __tablename__ = "life_events"

    id = Column(db.BigInteger, primary_key=True, autoincrement=True, nullable=False,index=True)
    event_name = db.Column(db.String(255),nullable=False)
    organiser_id = db.Column(db.BigInteger, db.ForeignKey('organiser.id'))
    event_date = db.Column(db.Date, index=True, nullable=False)
    event_time = db.Column(db.Time,index=True,nullable=False)
    event_city = db.Column(db.String(65),nullable=False,index=True)
    event_state = db.Column(db.String(65), nullable=False,index=True)
    event_country = db.Column(db.String(65),nullable=False,default="India",index=True)
    event_registration_no = db.Column(db.String(65),nullable=False,index=True)

    def to_json(self):


        organiser = OrganiserModel.query.filter(organiser_id=self.organiser_id).first()

        return{
            "id":self.id,
            "event_name":self.event_name,
            "organiser_name":organiser.name,
            "event_date":self.event_date.strftime("%Y-%m-%d %H:%M:%S"),
            "event_city":self.event_city,
            "event_state":self.event_state,
            "event_country":self.event_country,
            "event_registration_no":self.event_registration_no
        }