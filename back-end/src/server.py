from bottle import Bottle, run, route, get, post, response, request, hook
from returnvalue import ret
from params import check
import os

app = Bottle()

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@app.get('/test/')
@app.post('/test/')
def base():
    try:
        params = check.json(request)
    except:
        params = []
    toret = ret(request.route.rule, params)
    return toret.ret()

if __name__ == '__main__':
        try:
            run(app, host='127.0.0.1', port=8080)
        except:
            os._exit(0)
