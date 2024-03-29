import json, base64, json
from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

LENGTH = 4
IV_LENGTH = int(24 / LENGTH)
KEY_LENGTH = int(44 / LENGTH)

def encrypt(data):
    data = bytes(json.dumps(data),'utf-8')
    key = get_random_bytes(32)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    key = b64encode(key).decode('utf-8')
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')

    result = ""
    for i in range(LENGTH,0, -1):
        iv0 = int(len(iv) * (i - 1)/LENGTH)
        iv1 = int(len(iv) * i/LENGTH)
        key0 = int(len(key) * (i - 1)/LENGTH)
        key1 = int(len(key) * i/LENGTH)
        ct0 = int(len(ct) * (i - 1)/LENGTH)
        ct1 = int(len(ct) * i/LENGTH)
        result += iv[iv0:iv1] + key[key0:key1] + ct[ct0:ct1]
    return result

def decrypt(data):
    ivStr, keyStr, ctStr = "", "", ""
    for i in range(LENGTH,0,-1):
        formIV = int(len(data) * (i - 1) / LENGTH)
        formKey = int(len(data) * (i - 1) / LENGTH) + IV_LENGTH
        formCT1 = int(len(data) * (i - 1) / LENGTH) + IV_LENGTH + KEY_LENGTH
        formCT2 = int(len(data) * i / LENGTH)

        ivStr += data[formIV : formIV + IV_LENGTH]
        keyStr += data[formKey : formKey + KEY_LENGTH]
        ctStr += data[formCT1 : formCT2]

    key = base64.b64decode(keyStr.replace(' ','+'))
    iv = base64.b64decode(ivStr.replace(' ','+'))
    ct = base64.b64decode(ctStr.replace(' ','+'))
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8').replace('"', '')