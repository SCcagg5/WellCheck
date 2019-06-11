from bottle import request, response
import json as JSON

class ret:
    def __init__(self, route = None, params=None) :

        self.data = {
            'queryInfos' : {
                'route': route,
                'params': params
                },
            'status' :  500,
            'error' :   None,
            'data' :    None,
            'succes':   False

        }
        self.err = False

    def get(self):
        return self.data

    def ret(self):
        for i in []:
            if self.data["queryInfos"]["params"]:
                if i in self.data["queryInfos"]["params"]:
                    del self.data["queryInfos"]["params"][i]
        if self.data['error'] is None :
            self.data['succes'] = True
            self.data['status'] = 200
        return self.data

    def add_error(self, error = None, code = None):
        self.data['error'] = error
        self.data['status'] = code
        self.data['data'] = None
        if code is None:
            self.add_error("Bad code input", 500)
            return 1
        if error is None:
            self.add_error("Bad error input", 500)
            return 1
        self.err = True
        return self.ret()

    def add_data(self, data = None):
        self.data['data'] = data
        self.set_code(200)
        if data is None:
            self.add_error("Bad data input", 500)
            return 1
        return 0

    def set_code(self, code = None):
        self.data['status'] = code
        if code is None:
            self.add_error("Bad code input", 500)
            return 1
        return 0


class check:
    def contain(json, array):
        if json is None:
            return [False, "Invalid json received ", 400]
        for i in array:
            if isinstance(i, list):
                if not check.contain_opt(json, i):
                    return [False, "Missing on of parameters: " + JSON.dumps(i), 400]
                json = check.setnoneopt(json, i)
            elif i not in json:
                return [False, "Missing parameter : " + i, 400]
            elif json[i] is None:
                return [False, "Null parameter : " + i, 400]
        return [True, json, 200]

    def contain_opt(json, arr_opt):
        for i in arr_opt:
            if isinstance(i, list):
                if check.contain(json, i):
                    return True
            elif i in json:
                return True
        return False

    def setnoneopt(json, arr_opt):
        for i in arr_opt:
            if i not in json:
                json[i] = None
        return json

    def json(request):
        try:
            return request.json
        except:
            return []

class callnext:
    def __init__(self, req, resp = None, err = None):
        self.pr = check.json(req)
        self.private = {}
        self.toret = ret(req.path, self.pr)
        self.req = req
        self.resp = resp
        self.err = err

    def call(self, nextc):
        if self.req.method == 'OPTIONS':
            return {}
        if len(nextc) == 0:
            return self.ret()
        return nextc[0](self, nextc)

    def call_next(self, nextc, err = [True]):
        if not err[0]:
            return self.toret.add_error(err[1], err[2])
        nextc.pop(0)
        if len(nextc) == 0:
            self.toret.add_data(err[1])
            return self.ret()
        return nextc[0](self, nextc)

    def ret(self):
        if self.resp is not None:
            self.resp.content_type = 'application/json'
            return JSON.dumps(self.toret.ret())
        return self.toret.ret()
