from models.users.temp_user_model import TempUserModel


class TempUserRepository:


    @staticmethod
    def create_temp_user(user_data=None):
        if user_data:
            user = TempUserModel(
                email = user_data.get('email',None),
                first_name = user_data.get('first_name'),
                last_name = user_data.get('last_name'),
                sex = user_data.get('sex'),
                blood_group = user_data.get('blood_group'),
                city = user_data.get('city'),
                state = user_data.get('state'),
                country = user_data.get('country',"India"),
                birth_date = user_data.get('birth_date'),
                phone_number= user_data.get('phone_number')
            )
            
            user.save()
            return user
        return None 