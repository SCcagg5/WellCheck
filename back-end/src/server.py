from bottle import Bottle, run, route, response, request, hook, error
from Model.basic import ret, check, callnext
from Controller.routes import *
import json as JSON
import os

app = Bottle()
host = str(os.getenv('API_HOST', '172.0.0.1'))
port = int(os.getenv('API_PORT', 8080))
weba = str(os.getenv('API_WEBA', '*'))

call = lambda x : callnext(request).call(x)

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = weba
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.error()
@app.error(404)
def error(error):
    toret = ret(request.path, check.json(request))
    toret.add_error(error.body, int(error.status.split(" ")[0]))
    response.content_type = 'application/json'
    return JSON.dumps(toret.ret())

if __name__ == '__main__':
    try:
        setuproute(app, call)
        run(app, host=host, port=port, debug=True)
    except:
        os._exit(0)
