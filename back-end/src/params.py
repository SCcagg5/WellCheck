from bottle import request

class check:
    def contain(json, array):
        if json is None:
            return [False, "Invalid json received ", 400]
        for i in array:
            try:
                if json[i] is None:
                    return [False, "Null parameter : " + i, 400]
            except:
                return [False, "Missing parameter : " + i, 400]
        return [True, None, 200]

    def json(request):
        try:
            return request.json
        except:
            return None
