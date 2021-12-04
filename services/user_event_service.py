from repositories.association.user_event_repository import UserEventRepository


class UserEventService:

    @staticmethod
    def map_user_to_event(map_data,formatted=False):
        user_event_map = UserEventRepository.map_user_to_event(map_data)
        if user_event_map:
            if formatted:
                return user_event_map.to_json()
            return user_event_map
        return None

    @staticmethod
    def find_users_by_event(event_id=None):
        if event_id:
            return UserEventRepository.find_users_by_event(event_id)
        return None

    @staticmethod
    def find_events_by_user(user_id=None):
        if user_id:
            return UserEventRepository.find_events_by_user(user_id)
        return None
    