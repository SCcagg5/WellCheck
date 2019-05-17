from sql import sql
import hashlib
import time
import os

secret = os.getenv('API_SECRET', '1q2W3e')

class user:
    def __init__(self, mail, password = None, tok = None, role = 0):
        self.mail = mail
        self.password = self.__hash(password)
        self.token = tok
        self.role = role
        self.date = None
        self.id = None
        if password is None:
            user = sql.get("SELECT `role`, `date`  FROM `user` WHERE `mail` = %s", (self.mail))[0]
            self.role = user[0]
            self.date = user[1]

    def register(self, password2 = None):
        if self.__account_exist():
            return [False, "An existing account is using mail", 400]
        if self.password != self.__hash(password2) and password2 != None:
            return [False, "Passwords doesn't match", 400]
        if (len(password2) < 6):
            return [False, "Password is too short", 400]

        date = str(int(round(time.time() * 1000)))

        succes = sql.input("INSERT INTO `user` (`id`, `role`, `login`, `mail`, `phone`, `password`, `date`) VALUES (NULL, %s, %s, %s, %s, %s, %s)", \
        (self.role, self.mail, self.mail, '', self.password, date))

        if succes:
            return self.connect()
        return [False, "Input error", 500]

    def connect(self):
        if not self.__account_exist():
            return [False, "No existing account using this mail", 400]

        user = self.__verify_pass()
        if user is None:
            if self.__verifytoken(self.token):
                user = sql.get("SELECT `login`, `role`, `date`, `id`  FROM `user` WHERE `mail` = %s", (self.mail))[0]
            else:
                return [False, "Wrong Credentials", 400]
        self.login =  user[0]
        self.role = user[1]
        self.date = user[2]
        self.id = user[3]
        self.token = self.__gettoken()
        ret = {
                "login": self.login,
                "role": self.role,
                "mail":  self.mail,
                "token": self.token
                }
        return [True, ret, None]

    def __hash(self, password):
        if password is None:
            return None
        mail = self.mail
        s = len(mail)
        n = s % (len(password) - 1 if len(password) > 1 else 1)
        salted = password[:n] + str(s) + password[n:] + secret
        hashed = hashlib.sha512(salted.encode('utf-8')).hexdigest()
        return hashed

    def __gettoken(self):
        return hashlib.sha512((str(self.date) + str(self.role) + str(secret) + "1Qs3C").encode('utf-8')).hexdigest()

    def __verifytoken(self, token):
        return (token == self.__gettoken())

    def __account_exist(self):
        if self.mail != None:
            try:
                ret =  sql.get("SELECT `mail` FROM `user` WHERE `mail` = %s", (self.mail))[0][0]
                if ret == self.mail:
                    return True
            except:
                return False
        return False

    def __verify_pass(self):
        if self.mail != None and self.password != None:
            try:
                return sql.get("SELECT `login`, `role`, `date`, `id`  FROM `user` WHERE `mail` = %s AND `password` = %s", (self.mail, self.password))[0]
            except:
                return None
        return None
