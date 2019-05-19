from bottle import request
import json as JSON

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
