from models.events.event import EventModel
from models.users.temp_user_model import TempUserModel
from models.database import IndexedTimestampModel,db,Column
import json
import datetime

class UserEventMap(IndexedTimestampModel):
    __tablename__ = "user_event_map"

    id = Column(db.BigInteger, primary_key=True, autoincrement=True, nullable=False,index=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('temp_life_users.id'))
    event_id = db.Column(db.BigInteger, db.ForeignKey('life_events.id'))

    user = db.relationship(TempUserModel, backref=db.backref("temp_life_users", cascade="all, delete-orphan"))
    event = db.relationship(EventModel, backref=db.backref("life_events", cascade="all, delete-orphan"))