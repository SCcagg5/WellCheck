import requests
import os
import json as JSON
from requests.auth import HTTPBasicAuth
from sql import sql
import time


login = os.getenv('SIGFOX_LOG', None)
password = os.getenv('SIGFOX_PASS', None)

base = 1558515793000
last = -1


def updateall(number):
    try:
        limit = sql.get("SELECT `date` FROM data ORDER BY `date` DESC", None)[0][0]
    except:
        limit = base
    devices = sql.get("SELECT id_key, id from point", None)
    date = int(round(time.time()) * 1000)
    try:
        for i in devices:
            url = "https://api.sigfox.com/v2/devices/"+str(i[0])+"/messages"
            r = requests.get(url, auth=HTTPBasicAuth(login, password))
            data = JSON.loads(r.text)["data"]
            for j in data:
                trame = str(int(j["data"], 16))[1:-1]
                if len(trame) > 1 and int(j["time"]) > int(limit):
                    datas = loaddata(trame, int(j["time"]))
                    addtodb(datas, i[1])
    except:
        return
    return

def loaddata(trame, date):
    ret = {"type": None, "data": None}
    if len(trame) == 12:
        ret["type"] = "GPS"
        ret["data"] = {
            "lng": int(trame[0: 6]) / 10000,
            "lat": int(trame[6: 12]) / 10000
        }
    elif len(trame) == 29:
        ret["type"] = "DATA"
        ret["data"] = {
            "date": date,
            "humidity": int(trame[0:3]),
            "turbidity": int(trame[3:7]) / 100,
            "conductance": int(trame[7:11]) / 100,
            "ph": int(trame[11:14]) / 100,
            "pression": int(trame[14:22]) / 100,
            "temperature": int(trame[22:25]) / 10,
            "acceleration": (1 if int(trame[25:26]) == 1 else -1) * int(trame[26:29])
        }
    return ret

def addtodb(data, p_id):
    if data["type"] == "DATA":
        sql.input("INSERT INTO `data` (`point_id`, `date`, `humidity`, `turbidity`, `conductance`, `ph`, `pression`, `temperature`, `acceleration`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);" ,
        (p_id, data["data"]["date"], data["data"]["humidity"], data["data"]["turbidity"], data["data"]["conductance"], data["data"]["ph"], data["data"]["pression"], data["data"]["temperature"], data["data"]["acceleration"]))
    elif data["type"] == "GPS":
        sql.input("UPDATE `point` SET `lng` = %s, `lat` = %s WHERE `id` = %s;", \
        (data["data"]["lng"], data["data"]["lat"], p_id))
    return


class points:
    def __init__(self, userid):
        self.userid = userid
        date = int(round(time.time()))
        number = (date - base) % (30 * 60)
        if (last < number):
            updateall(number)

    def getall(self):
        return [True, {"my_points": sql.get("SELECT `id` FROM `point` WHERE `user_id` = %s", (self.userid)), "shared_to_me": sql.get("SELECT `point_id` FROM `share` WHERE `user_id_to` = %s", (self.userid))}]

    def getalldetails(self):
        ret = {"my_points": [], "shared_to_me": []}
        points = self.getall()[1]
        for i in ["my_points", "shared_to_me"]:
            for p in points[i]:
                to_add = point(p[0], self.userid).infos()[1]
                ret[i].append(to_add)
        return [True, ret, None]

class point:
    def __init__(self, db_id, userid, key = None, point_id = None, ):
        self.id = db_id
        self.userask = userid
        self.key = key
        self.sig_id = point_id
        self.err = [True]
        self.lat = None
        self.lng = None
        self.name = None
        self.user = None
        self.surname = None
        self.sharefrom = None
        self.shareto = []
        date = int(round(time.time()))
        number = (date - base) % (30 * 60)
        if (last < number):
            updateall(number)
        self.getinfos()


    def getinfos(self):
        if self.id is None:
            self.err = self.fromapiinfo()
        if self.err[0]:
            self.fromdbinfo()

    def infos(self):
        if not self.err[0]:
            return self.err
        if self.sig_id is None or self.id is None:
            return [False, "Bad Input", 403]
        ret = {
        "id" : self.id,
        "location": {"lat": self.lat, "lng": self.lng},
        "name": self.name,
        "surname": self.surname,
        "data": self.__getdata()[1]
        }
        if self.__user_got_point():
            ret["shareto"] = self.shareto
        else:
            ret["sharefrom"] = sql.get("SELECT `login`, `mail` FROM `user` WHERE `id` = %s", (self.sharefrom))[0]
        return [True, ret, None]

    def fromapiinfo(self):
        authentication = (login, password)
        r = requests.get(
        "https://api.sigfox.com/v2/devices/" + self.sig_id,
         auth=HTTPBasicAuth(login, password))
        try:
            data = JSON.loads(r.text)
            self.lat = data['location']['lat']
            self.lng = data['location']['lng']
            self.name = data['name']
        except:
            return [False, "Invalid sig_id", 500]
        self.surname = self.name
        return self.__input()

    def fromdbinfo(self):
        if self.id is None:
            self.id = sql.get("SELECT `id` FROM `point` WHERE `id_key` = %s", (self.sig_id))[0][0]
        data = sql.get("SELECT * FROM `point` WHERE `id` = %s", (self.id))
        if not data:
            self.err = [False, "Invalid point_id", 400]
            return
        data = data[0]
        if data is None:
            return
        self.lat = data[1]
        self.lng = data[2]
        self.name = data[3]
        self.surname = data[4]
        self.user = data[5]
        self.key = data[6]
        self.sig_id = data[7]
        data = sql.get("SELECT login, mail FROM `user` INNER JOIN `share` ON user.id = share.user_id_to WHERE share.point_id = %s", (self.id))
        self.shareto = data if data is not None else []
        if not self.__user_got_point():
            self.surname = sql.get("SELECT surname FROM `share` WHERE point_id = %s AND user_id_to = %s", (self.id, self.userask))[0][0]
            self.sharefrom = self.user

    def rename(self, surname):
        if surname == "":
            surname = self.name
        self.surname = surname
        self.__update()
        self.fromdbinfo()
        return self.infos()

    def share(self, mail):
        if not self.__user_exist(mail):
            return [False, "user do not exist", 404]
        if not self.__user_got_point():
            return [False, "user do not possess this point", 403]

        idto = self.__user_exist(mail)

        if self.__user_is(idto):
            return [False, "you cannot share to you", 403]
        if self.__share_with(mail):
            return [False, "you're already sharing with this user", 403]

        succes = sql.input("INSERT INTO `share` (`id`, `user_id_from`, `user_id_to`, `point_id`, `surname`) VALUES (NULL, %s, %s, %s, %s)", \
        (self.userask, idto, self.id, self.name))
        if not succes:
            return [False, "input error", 500]
        self.fromdbinfo()
        return self.infos()


    def __input(self):
        if self.__point_exist():
            return [False, "device already registered", 403]
        succes = sql.input("INSERT INTO `point` (`id`, `lng`, `lat`, `name`, `surname`, `user_id`, `key`, `id_key`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s)", \
        (self.lng, self.lat, self.name, self.surname, self.userask, self.key, self.sig_id))
        if succes:
            return [True, None, None]
        return [False, "input error", 500]

    def __getdata(self):
        data = sql.get("SELECT * FROM `data` WHERE `point_id` = %s ORDER BY `id` DESC", (self.id))
        ret = []
        for i in data:
            b = {
                "date": i[2],
                "humidity": i[3],
                "turbidity": i[4],
                "conductance": i[5],
                "ph": i[6],
                "pression": i[7],
                "temperature": i[8],
                "acceleration": i[9]
            }
            ret.append(b)
        return [True, ret, None]

    def __update(self):
        if self.__user_got_point():
            succes = sql.input("UPDATE `point` SET `lng` = %s, `lat` = %s , `name` = %s, `surname` = %s WHERE `id` = %s;", \
            (self.lng, self.lat, self.name, self.surname, self.id))
        else:
            succes = sql.input("UPDATE `share` SET `surname` = %s WHERE `point_id` = %s AND user_id_to = %s;", \
            (self.surname, self.id, self.userask))
        if succes:
            return True
        return False

    def __point_exist(self):
        if self.sig_id != None:
            try:
                point_id = sql.get("SELECT `id` FROM `point` WHERE `id_key` = %s", (self.sig_id))[0][0]
                return True
            except:
                return False
        return False

    def __user_exist(self, mail):
        if mail != None:
            try:
                ret =  sql.get("SELECT `id`, `mail` FROM `user` WHERE `mail` = %s", (mail))[0]
                if ret[1] == mail:
                    return ret[0]
            except:
                return False
        return False

    def __user_is(self, user_id):
        return (int(self.userask) == int(user_id))

    def __share_with(self, mail):
        for i in self.shareto:
            if i[1] == mail:
                return True
        return False

    def __user_got_point(self):
        return (self.user == self.userask)
