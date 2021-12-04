from models.events.event import EventModel
from models.users.user_model import UserModel
from extentions.extentions import db
from flask import request
from helpers.pagination_helpers import get_url

class EventRepository:

    @staticmethod
    def create_event(event_data=None):
        if event_data:
            event = EventModel(
                event_name = event_data.get("event_name"),
                organiser_id = event_data.get("organiser_id"),
                event_date = event_data.get("event_date"),
                event_city = event_data.get("event_city"),
                event_state = event_data.get("event_state"),
                event_country = event_data.get("event_country")
            )
            event.save()
            return event
        return None

    @staticmethod
    def update_event(event_object,event_data=None):
        if event_data:
            event_object_attrs = list(event_object.__dict__.keys())
            for event_data_key,event_data_value in event_data.items():
                if event_data_key in event_object_attrs:
                    setattr(event_object,event_data_key,event_data_value)
            event_object.save()
            return event_object
        return None

    @staticmethod
    def get_all_events(formatted=False):
        events = EventModel.query.all()
        if events:    
            if not formatted:
                return events
            events_data = {}
            for event in events:
                events_data[event.id]=event.to_json()
            return events_data
        return None

    @staticmethod
    def find_by_id(id=None):
        if not id:
            return None
        event = EventModel.query.filter_by(id=id).first()
        if event:
            return event

        return None

    @staticmethod
    def find_by_organiser_id(organiser_id=None,formatted=False):
        if not organiser_id:
            return None
        events = EventModel.query.filter_by(organiser_id=organiser_id).all()
        if not formatted:
            return events
        events_data = {}
        for event in events:
            events_data[event.id]=event.to_json()
        return events_data

    @staticmethod
    def find_by_registration_no(registration_no = None):
        if not registration_no:
            return None
        event = EventModel.query.filter_by(event_registration_no=registration_no).first()
        if event:
            return event
        return None
    

    @staticmethod
    def find_by_city(city=None,formatted=False):
        if not city:
            return None
        events = EventModel.query.filter_by(city=city).all()
        if events:
            if not formatted:
                return events

            events_data = {}
            for event in events:
                events_data[event.id] = event.to_json()
            return events_data    

        return None

    @staticmethod
    def delete_event_by_id(id=None):
        if not id:
            return None

        event = EventModel.query.filter_by(id=id).first()
        if event:
            event.delete()
            return True

        return False

    @staticmethod
    def find_by_date(date=None,formatted=False):
        if not date:
            return None
        events = EventModel.query.filter_by(event_date=date).all()
        if events:
            if formatted:
                events_data={}
                for event in events:
                    events_data[event.id] = event.to_json()
                return events_data
            return events
        return None

    @staticmethod
    def get_paginated_events(formatted=False,per_page=50,page=1):
        all_events = EventModel.query.paginate(per_page=per_page,page=page)
        
        page_metadata = {}
        if all_events.has_next: 
            page_metadata["next_page"] = all_events.next_num
            page_metadata['next_url'] = get_url(request.base_url,all_events.next_num)
            
        else:
            page_metadata["next_page"] = None
            page_metadata['next_url'] = None

        if all_events.has_prev:
            page_metadata['prev_page'] = all_events.prev_num
            page_metadata['prev_url'] = get_url(request.base_url,all_events.prev_num)
        else:
            page_metadata['prev_page'] = None
            page_metadata['prev_url'] = None

        
        page_metadata['total_pages'] = all_events.pages
        
        
        
        page_metadata['next_url']

        if all_events:
            print(all_events)
            data = {}
            data['page_metadata'] = page_metadata
            
            if not formatted:
                data['events_data'] = all_events
                return data
            all_events_data = {}
            for event in all_events.items:
                all_events_data[event.id] = event.to_json()

            data['event_data'] = all_events_data
            return data
        return None





            

    
