from repositories.events.event_repository import EventRepository

class EventService:
    
    @staticmethod
    def create_event(event_data=None,formatted=False):
        if event_data:
            event = EventRepository.create_event(event_data)
            if event:
                if formatted:
                    return event.to_json()
                return event
        return None

    @staticmethod
    def update_event(event_object,event_data=None):
        return EventRepository.update_event(event_object,event_data)

    @staticmethod
    def get_all_events(formatted=False):
        return EventRepository.get_all_events(formatted)

    @staticmethod
    def find_by_id(id,formatted=False):
        event = EventRepository.find_by_id(id)
        if event:
            if formatted:
                return event.to_json()
            return event
        return None

    @staticmethod
    def find_by_city(city=None,formatted=False):
        if city:
            return EventRepository.find_by_city(city=None,formatted=False)
        return None

    @staticmethod
    def find_by_date(date=None,formatted=False):
        if date:
            return EventRepository.find_by_date(date,formatted)
        return None

    @staticmethod
    def find_by_registration_no(registration_no=None,formatted=False):
        if registration_no:
            event = EventRepository.find_by_registration_no(registration_no)
            if formatted:
                return event.to_json()
            return event
        return None

    @staticmethod
    def get_paginated_events(page,formatted=True):
        return EventRepository.get_paginated_events(formatted=False,per_page=50,page=1)


    @staticmethod
    def find_by_organiser_id(organiser_id=None):
        if not organiser_id:
            return None
        return EventRepository.find_by_organiser_id(organiser_id,True)