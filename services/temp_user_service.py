from repositories.users.temp_user_repository import TempUserRepository


class TempUserService:

    @staticmethod
    def create_temp_user(user_data):
        
        user = TempUserRepository.create_user(user_data)
        if user:
            return user.to_json()

        return None

    
