

from Cryptodome.Cipher import DES3
import base64

class EncryptData:
    def __init__(self, key):
        self.key = key  # 初始化密钥
        self.iv = b'01234567' # 偏移量
        self.length = DES3.block_size  # 初始化数据块大小
        self.des3 = DES3.new(self.key, DES3.MODE_CBC, self.iv)  # 初始化AES,CBC模式的实例
        # 截断函数，去除填充的字符
        self.unpad = lambda date: date[0:-ord(date[-1])]

    def pad(self, text):
        """
        #填充函数，使被加密数据的字节码长度是block_size的整数倍
        """
        count = len(text.encode('utf-8'))
        add = self.length - (count % self.length)
        entext = text + (chr(add) * add)
        return entext

    def encrypt(self, encrData):  # 加密函数

        res = self.des3.encrypt(self.pad(encrData).encode("utf8"))
        msg = str(base64.b64encode(res), encoding="utf8")
        return msg

    def decrypt(self, decrData):  # 解密函数
        res = base64.decodebytes(decrData.encode("utf8"))
        msg = self.des3.decrypt(res).decode("utf8")
        return self.unpad(msg)

def getEntrypyKey():
    num = [87, 85, 89, 79, 85, 76, 85, 83, 72, 73, 71, 79, 78, 71, 74, 85]
    str = ""
    for i in num:
        str += chr(i)
    return str