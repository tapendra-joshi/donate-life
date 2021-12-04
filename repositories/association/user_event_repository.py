from models.association.user_event_map import UserEventMap


class UserEventRepository:

    @staticmethod
    def map_user_to_event(map_data=None):
        if map_data:
            user_event_map = UserEventMap(
                user_id = map_data.get("user_id"),
                event_id = map_data.get("event_id")
            )
            user_event_map.save()
            return user_event_map
        return None

    @staticmethod
    def find_users_by_event(event_id=None):
        if event_id:
            user_event_maps = UserEventMap.query.filter_by(event_id=event_id).all()
            users = [map.user_id for map in user_event_maps]
            return users
        return None

    @staticmethod
    def find_events_by_user(user_id=None):
        if user_id:
            user_event_maps = UserEventMap.query.filter_by(user_id=user_id).all()
            events = [map.events_id for map in user_event_maps]
            return events
        return None

