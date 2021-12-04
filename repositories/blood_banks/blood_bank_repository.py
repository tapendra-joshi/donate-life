from models.blood_banks.blood_bank_model import BloodBankModel,BloodStock
from sqlalchemy import text
from extentions.extentions import db
from helpers.pagination_helpers import get_url
from flask import request

class BloodBankRepository:

    @staticmethod
    def create_blood_bank_stock(blood_stock_data=None):
        if blood_stock_data:
            blood_stock = BloodStock(
                ab_positive = blood_stock_data.get('ab_positive',0),
                ab_negative = blood_stock_data.get('ab_negative',0),
                a_positive = blood_stock_data.get('a_positive',0),
                a_negative = blood_stock_data.get('a_negative',0),
                b_positive = blood_stock_data.get('b_positive',0),
                b_negative = blood_stock_data.get('b_negative',0),
                o_positive = blood_stock_data.get('o_negative',0),
                o_negative = blood_stock_data.get('o_negative',0)
            )
            blood_stock.save()
            return blood_stock
        return None

    @staticmethod
    def update_blood_stock(blood_stock_object,blood_stock_data=None):
        if blood_stock_data:
            blood_stock_object_attrs = list(blood_stock_object.__dict__.keys())
            for blood_stock_data_key,blood_stock_data_value in blood_stock_data.items():
                if blood_stock_data_key in blood_stock_object_attrs:
                    setattr(blood_stock_object,blood_stock_data_key,blood_stock_data_value)
            blood_stock_object.save()
            return blood_stock_object
        return None

    @staticmethod
    def create_blood_bank(blood_bank_data=None):
        if blood_bank_data:
            blood_bank = BloodBankModel(
                name = blood_bank_data.get('name'),
                email = blood_bank_data.get('email'),
                address = blood_bank_data.get('address'),
                city = blood_bank_data.get('city'),
                state = blood_bank_data.get('state'),
                country = blood_bank_data.get('country'),
                blood_stock_id = BloodBankRepository.create_blood_bank_stock(blood_bank_data.get('blood_stock')).id
            )
            
            blood_bank.save()
            return blood_bank
        return None

    @staticmethod
    def get_all_blood_banks(formatted=False):
        
        all_blood_banks = BloodBankModel.query.all()
        if all_blood_banks:
            if not formatted:
                return all_blood_banks
            all_blood_bank_data = {}
            for blood_bank in all_blood_banks:
                all_blood_bank_data[blood_bank.id] = blood_bank.to_json()
            return all_blood_bank_data
        return None

    @staticmethod
    def get_paginated_blood_banks(formatted=False,per_page=50,page=1):
        all_blood_banks = BloodBankModel.query.paginate(per_page=per_page,page=page)
        
        page_metadata = {}
        if all_blood_banks.has_next: 
            page_metadata["next_page"] = all_blood_banks.next_num
            page_metadata['next_url'] = get_url(request.base_url,all_blood_banks.next_num)
            
        else:
            page_metadata["next_page"] = None
            page_metadata['next_url'] = None

        if all_blood_banks.has_prev:
            page_metadata['prev_page'] = all_blood_banks.prev_num
            page_metadata['prev_url'] = get_url(request.base_url,all_blood_banks.prev_num)
        else:
            page_metadata['prev_page'] = None
            page_metadata['prev_url'] = None

        
        page_metadata['total_pages'] = all_blood_banks.pages
        
        
        
        page_metadata['next_url']

        if all_blood_banks:
            print(all_blood_banks)
            data = {}
            data['page_metadata'] = page_metadata
            
            if not formatted:
                data['blood_bank_data'] = all_blood_banks
                return data
            all_blood_bank_data = {}
            for blood_bank in all_blood_banks.items:
                all_blood_bank_data[blood_bank.id] = blood_bank.to_json()

            data['blood_bank_data'] = all_blood_bank_data
            return data
        return None


    @staticmethod
    def find_by_email(email=None):

        if not email:
            return None
        
        blood_bank = BloodBankModel.query.filter_by(email=email).first()
        if blood_bank:
            return blood_bank
        return None

    @staticmethod
    def find_by_id(id=None):
        if not id:
            return None
        blood_bank = BloodBankModel.query.filter_by(id=id).first()
        if blood_bank:
            return blood_bank
        return None

    @staticmethod
    def find_by_city(formatted=False,city=None):
        if not city:
            return None
        
        blood_banks = BloodBankModel.query.filter_by(city=city).all()
        if blood_banks:
            if not formatted:
                return blood_bank
            all_blood_bank_data = {}
            for blood_bank in blood_banks:
                all_blood_bank_data[blood_bank.id] = blood_bank.to_json()
            return all_blood_bank_data
        return None

    @staticmethod
    def find_by_state(formatted=False,state=None):
        if not state:
            return None
        blood_banks = BloodBankModel.query.filter_by(state=state).all()
        if blood_banks:
            if not formatted:
                return blood_bank
            all_blood_bank_data = {}
            for blood_bank in blood_banks:
                all_blood_bank_data[blood_bank.id] = blood_bank.to_json()
            return all_blood_bank_data
        return None

    @staticmethod
    def get_all_states():
        banks = BloodBankModel.query.distinct(BloodBankModel.state)
        if banks:
            all_states = []
            for bank in banks:
                all_states.append(bank.state)
            return all_states
        return None

    @staticmethod
    def get_cities_by_state(state):
        banks = BloodBankModel.query.filter_by(state = state).distinct(BloodBankModel.city)
        if banks:
            cities = []
            for banks in banks:
                cities.append(banks.city)
            return cities
        return None

    @staticmethod
    def find_by_available_blood_stock(blood_type,formatted=False):
        data_dict = {
            'ab_positive':BloodStock.ab_positive,
            'ab_negative':BloodStock.ab_negative,
            'a_positive':BloodStock.a_positive,
            'b_positive':BloodStock.b_positive,
            'a_negative':BloodStock.a_negative,
            'b_negative':BloodStock.b_negative,
            'o_positive':BloodStock.o_positive,
            'o_negative':BloodStock.o_negative
        }
        blood_stocks = BloodStock.query.filter(data_dict[blood_type] > 0).all()
        ids = [blood_stock.id for blood_stock in blood_stocks]

        blood_banks = BloodBankModel.query.filter(BloodBankModel.blood_stock_id.in_(ids)).all()
        if blood_banks:
            if not formatted:
                return blood_banks
            all_blood_bank_data = {}
            for blood_bank in blood_banks:
                all_blood_bank_data[blood_bank.id] = blood_bank.to_json()
            return all_blood_bank_data
        return None
        
        # where_clause_query = ""
        # where_clause_query += (" or ".join("{0} > 0".format(blood_type) for blood_type in blood_types)) 
        
        # sql_text = "select id from blood_stock where {}".format(where_clause_query)
        # sql = text(sql_text)
        # result = db.engine.execute(sql)
        
        # ids = []
        # for row in result:
        #     ids.append(row)
        
        # # blood_banks = BloodBankModel.query.filter(BloodBankModel.blood_stock_id.in_(ids)).all()
        # # blood_bank_data = {}
        # # for blood_bank in blood_banks:
        # #     blood_bank_data[blood_bank.id] = blood_bank.to_json()
        # return blood_bank_data
