from bottle import Bottle, run, route, response, request, hook, error
from returnvalue import ret
import json as JSON
import os
from call import cn
from routes import *

app = Bottle()
host = os.getenv('API_HOST', '172.0.0.1')
port = os.getenv('API_PORT', 8080)
weba = os.getenv('API_WEBA', '*')

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = weba
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.error()
@app.error(404)
def error(error):
    params = check.json(request)
    toret = ret(request.path, params)
    toret.add_error(error.body, int(error.status.split(" ")[0]))
    response.content_type = 'application/json'
    return JSON.dumps(toret.ret())

@app.route('/test/', method=['OPTIONS', 'POST', 'GET'])
def base():
    return cn(request).call([])

@app.route('/register/', method=['OPTIONS', 'POST'])
def base():
    return cn(request).call([register])

@app.route('/connect/', method=['OPTIONS', 'POST'])
def base():
    return cn(request).call([connect])

@app.route('/addpoint/', method=['OPTIONS', 'POST'])
def base():
    return cn(request).call([connect, addpoint])

@app.route('/infos/', method=['OPTIONS', 'POST'])
def base():
    return cn(request).call([connect, infos])

@app.route('/share/', method=['OPTIONS', 'POST'])
def base():
    return cn(request).call([connect, share])

@app.route('/surname/', method=['OPTIONS', 'POST'])
def base():
    return cn(request).call([connect, surname])

@app.route('/getall/', method=['OPTIONS', 'POST'])
def base():
    return cn(request).call([connect, getall])

@app.route('/getalldetails/', method=['OPTIONS', 'POST'])
def base():
    return cn(request).call([connect, getalldetails])

if __name__ == '__main__':
        try:
            run(app, host=host, port=port, debug=True)
        except:
            os._exit(0)
