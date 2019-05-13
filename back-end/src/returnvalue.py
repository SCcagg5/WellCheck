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
        for i in ["mail", "password", "password2", "cb", "cb_id", "token"]:
            if self.data["queryInfos"]["params"]:
                if i in self.data["queryInfos"]["params"]:
                    del self.data["queryInfos"]["params"][i]
        if self.data['error'] == None :
            self.data['succes'] = True
            self.data['status'] = 200
        return self.data

    def add_error(self, error = None, code = None):
        self.data['error'] = error
        self.data['status'] = code
        self.data['data'] = None
        if code == None:
            self.add_error("Bad code input", 500)
            return 1
        if error == None:
            self.add_error("Bad error input", 500)
            return 1
        self.err = True
        return 0

    def add_data(self, data = None):
        self.data['data'] = data
        self.set_code(200)
        if data == None:
            self.add_error("Bad data input", 500)
            return 1
        return 0

    def set_code(self, code = None):
        self.data['status'] = code
        if code == None:
            self.add_error("Bad code input", 500)
            return 1
        return 0
