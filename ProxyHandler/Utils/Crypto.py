from Crypto.Cipher import AES as _AES
from Crypto.Cipher import DES as _DES
from Crypto.Cipher import DES3 as _DES3
from Crypto.Util.Padding import pad,unpad
from Crypto.PublicKey import RSA as _RSA
from Crypto.Cipher import PKCS1_v1_5
import base64
import hashlib

# ----------- AES加解密 -----------
class AES:
    CBC = _AES.MODE_CBC
    ECB = _AES.MODE_ECB
    CFB = _AES.MODE_CFB
    OFB = _AES.MODE_OFB
    CTR = _AES.MODE_CTR

    @staticmethod
    def encrypt(data: bytes, mode: int,key: bytes, iv: bytes, style: str="pkcs7") -> bytes:
        cipher = _AES.new(key, mode, iv)
        padded_data = pad(data, _AES.block_size, style)
        return cipher.encrypt(padded_data)
    
    @staticmethod
    def decrypt(data: bytes, mode: int,key: bytes, iv: bytes,style: str="pkcs7") -> bytes:
        cipher = _AES.new(key, mode, iv)
        decrypted = cipher.decrypt(data)
        try:
            decrypted = unpad(decrypted, _AES.block_size, style)
        except:
            return decrypted

# ----------- DES加解密 -----------
class DES:
    CBC = _DES.MODE_CBC
    ECB = _DES.MODE_ECB
    CFB = _DES.MODE_CFB
    OFB = _DES.MODE_OFB
    CTR = _DES.MODE_CTR
    
    @staticmethod
    def encrypt(data: bytes, mode: int,key: bytes, iv: bytes, style: str="pkcs7") -> bytes:
        cipher = _DES.new(key, mode, iv)
        padded_data = pad(data, _DES.block_size, style)
        return cipher.encrypt(padded_data)
    
    @staticmethod
    def decrypt(data: bytes, mode: int,key: bytes, iv: bytes, style: str="pkcs7") -> bytes:
        cipher = _DES.new(key, mode, iv)
        decrypted = cipher.decrypt(data)
        try:
            decrypted = unpad(decrypted, _DES.block_size, style)
        except:
            return decrypted

# ----------- DES3加解密 -----------
class DES3:
    CBC = _DES3.MODE_CBC
    ECB = _DES3.MODE_ECB
    CFB = _DES3.MODE_CFB
    OFB = _DES3.MODE_OFB
    CTR = _DES3.MODE_CTR

    @staticmethod
    def des_encrypt(data: bytes, mode: int,key: bytes, iv: bytes, style: str="pkcs7") -> bytes:
        cipher = _DES3.new(key, mode, iv)
        padded_data = pad(data, _DES3.block_size, style)
        return cipher.encrypt(padded_data)
    
    @staticmethod
    def des_decrypt(data: bytes, mode: int,key: bytes, iv: bytes, style: str="pkcs7") -> bytes:
        cipher = _DES3.new(key, mode, iv)
        decrypted = cipher.decrypt(data)
        try:
            decrypted = unpad(decrypted, _DES3.block_size, style)
        except:
            return decrypted
            
# ----------- RSA加解密 -----------
class RSA:
    @staticmethod
    def encrypt(data: str,publicKey: str,length=117):
        """
        RSA+Base64, 支持分段加密
        """
        pubObj = _RSA.importKey("-----BEGIN PUBLIC KEY-----\n" + publicKey + "\n-----END PUBLIC KEY-----")
        encryptor = PKCS1_v1_5.new(pubObj)
        dataLength = len(data)
        if dataLength < length:
            return base64.b64encode(encryptor.encrypt(data.encode())).decode()
        result = bytes()
        for i in range(0, dataLength, length):
            result += encryptor.encrypt(
                        data.encode(encoding="utf-8")[i:i + length])
        return base64.b64encode(bytes(result)).decode()

    @staticmethod
    def decrypt(data: str,privateKey: str,length=128):
        """
        RSA+Base64, 支持分段解密
        """
        privObj = _RSA.importKey("-----BEGIN PRIVATE KEY-----\n" + privateKey + "\n-----END PRIVATE KEY-----")
        decryptor = PKCS1_v1_5.new(privObj)
        data = base64.b64decode(data)
        dataLength = len(data)
        if dataLength < length:
            return decryptor.decrypt(data)
        result = bytes()
        for i in range(0, dataLength, length):
            result += decryptor.decrypt(
                        data[i:i + length],sentinel=None)
        return result.decode()
    
class Hash:
    @staticmethod
    def md5(data: bytes) -> str:
        return hashlib.md5(data).hexdigest()
