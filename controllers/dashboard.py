# from flask import Blueprint, jsonify
# from repositories.blood_banks.blood_bank_repository import BloodBankRepository
# from data_process.upload_blood_bank_data import upload_blood_bank_data

# blueprint = Blueprint("dashboard_blueprint", __name__, url_prefix="")

# @blueprint.route('/home',methods=["GET"])
# def home():
#     try:
#         states = BloodBankRepository.get_cities_by_state("Andaman And Nicobar Islands")
#         print(states)
#         # upload_blood_bank_data()
#         # print(blood_banks)
#         # blood_bank_data = {}
#         # for blood_bank in blood_banks:
#         #     blood_bank_data[blood_bank.id] = blood_bank.to_json()
#         #     print(blood_bank)
#         # print(blood_bank_data)
#         # a=[]
#         # for row in result:
#         #     a.append(row)
#         # print(type(result))
#         # if len(a)>0:
#         return {"done":True,"states":states}
#     except Exception as exe:
#         print(exe)
#         return {}
