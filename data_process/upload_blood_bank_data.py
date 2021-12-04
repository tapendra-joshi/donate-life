import pandas as pd
from models.blood_banks.blood_bank_model import BloodBankModel


def clean_number(char):
    if char:
        print(char)
        x = char.split(',')[0]
        x = "".join(filter(str.isdigit,str(x)))
        if x == '':
            return None
        return x
    return None


def clean_con_number(char):
    if char:
        x = char.split(',')[0]
        return x.strip()
    return None


def strip_value(val):
    return val.strip()


def clean_pincode(pin):
    x = "".join(filter(str.isdigit,str(pin)))
    if x == '':
        return None
    return x


def upload_blood_bank_data():
    df = pd.read_csv('blood-banks.csv',encoding='ISO-8859-1')
    
    df[" Mobile"] = df[" Mobile"].astype(str)
    df[" Mobile"] = df[" Mobile"].apply(clean_number)

    df[" Contact No"] = df[" Contact No"].astype(str)
    df[" Contact No"] = df[" Contact No"].apply(strip_value)
    df[" Contact No"] = df[" Contact No"].replace('N/A',None)
    df[" Contact No"] = df[" Contact No"].apply(clean_con_number)
    # return df[" Contact No"]
    df[" Latitude"] = df[" Latitude"].astype(str)
    df[" Latitude"] = df[" Latitude"].apply(strip_value)

    df[" Longitude"] = df[" Longitude"].astype(str)
    df[" Longitude"] = df[" Longitude"].apply(strip_value)

    df["Pincode"] = df["Pincode"].astype(str)
    df["Pincode"] = df["Pincode"].apply(strip_value)
    df["Pincode"] = df["Pincode"].apply(clean_pincode)

    df[' Email'] = df[' Email'].astype(str)
    df[' Email'] = df[' Email'].replace('N/A',None)
    df[' Email'] = df[' Email'].apply(clean_con_number)

    df[' City'] = df[' City'].astype(str)
    df[' City'] = df[' City'].apply(strip_value)

    df[' Blood Bank Name'] = df[' Blood Bank Name'].apply(strip_value)

    df[' District'] = df[' District'].astype(str)
    df[' District'] = df[' District'].apply(strip_value)

    df[' Address'] = df[' Address'].astype(str)
    df[' Address'] = df[' Address'].apply(strip_value)


    
    for index,row in df.iterrows():
        blood_bank = BloodBankModel(
            name = row[' Blood Bank Name'],
            email=row[' Email'],
            state=row[' State'],
            district = row[' District'],
            city = row[' City'],
            blood_stock_id = 1,
            address = row[' Address'],
            contact_number = row[' Contact No'],
            mobile_number = row[' Mobile'],
            latitude = row[' Latitude'],
            longitude = row[' Longitude'],
            pincode = row['Pincode']
        )
        blood_bank.blood_stock_id = 0
        blood_bank.save()
    