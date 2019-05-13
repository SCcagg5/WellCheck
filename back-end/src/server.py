from bottle import Bottle, run, route, get, post, response, request, hook
from returnvalue import ret
from params import check
import os

app = Bottle()
host = os.getenv('API_HOST', '0.0.0.0')
port = os.getenv('API_PORT', 8080)
weba = os.getenv('API_WEBA', '*')

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = weba
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
            run(app, host=host, port=port)
        except:
            os._exit(0)
