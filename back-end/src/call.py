from bottle import request, response
from returnvalue import ret
from params import check
import json as JSON

class cn:
    def __init__(self, req, resp = None, err = None):
        self.pr = check.json(req)
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
