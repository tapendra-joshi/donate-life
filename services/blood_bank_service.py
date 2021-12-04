from repositories.blood_banks.blood_bank_repository import BloodBankRepository


class BloodBankService:

    @staticmethod
    def get_all_blood_banks(formatted=False):
        all_blood_bank_data = BloodBankRepository.get_all_blood_banks(formatted)
        if all_blood_bank_data:
            return all_blood_bank_data
        return None

    @staticmethod
    def create_blood_bank(blood_bank_data,formatted=False):
        if blood_bank_data:
            
            existing_blood_bank = BloodBankRepository.find_by_email(blood_bank_data.get("email"))
            if existing_blood_bank:
                return None

            blood_bank = BloodBankRepository.create_blood_bank(blood_bank_data)
            if blood_bank:
                if formatted:
                    blood_bank_json = blood_bank.to_json()
                    return blood_bank_json
                return blood_bank
        return None

    @staticmethod
    def get_blood_bank_avail_btype(blood_type,formatted=False):
        if blood_type:
            blood_banks_data = BloodBankRepository.find_by_available_blood_stock(blood_type,formatted)
            if blood_banks_data:
                return blood_banks_data
            return None


    @staticmethod
    def get_paginated_blood_banks(page,formatted=False):
        all_blood_bank_data = BloodBankRepository.get_paginated_blood_banks(formatted=formatted,page=page)
        if all_blood_bank_data:
            return all_blood_bank_data
        return None


    @staticmethod
    def find_by_state(state,formatted=False):
        if state:
            blood_banks_data = BloodBankRepository.find_by_state(formatted,state=state)
            if blood_banks_data:
                return blood_banks_data
            return None
        return None

    @staticmethod
    def find_by_city(city,formatted=False):
        if city:
            blood_banks_data = BloodBankRepository.find_by_city(formatted,city)
            if blood_banks_data:
                return blood_banks_data
            return None
        return None

    @staticmethod
    def get_all_states():
        states = BloodBankRepository.get_all_states()
        if states:
            return states
        return None

    @staticmethod
    def get_city_by_state(state):
        cities = BloodBankRepository.get_cities_by_state(state)
        if cities:
            return cities
        return None

                
