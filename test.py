# from data_process.upload_blood_bank_data import upload_blood_bank_data
# print(upload_blood_bank_data())

from repositories.blood_banks.blood_bank_repository import BloodBankRepository
BloodBankRepository.get_all_state()