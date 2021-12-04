import enum


class HashMethod(enum.Enum):
    MD5 = "MD5"
    SHA256 = "SHA256"

class SaltKey(enum.Enum):
    SALT_KEY = "QAZWSX"