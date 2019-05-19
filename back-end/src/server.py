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

call = lambda x : cn(request).call(x)

@app.route('/test/',        ['OPTIONS', 'POST', 'GET'], lambda x = None: call([])                       )
@app.route('/register/',    ['OPTIONS', 'POST'],        lambda x = None: call([register])               )
@app.route('/connect/',     ['OPTIONS', 'POST'],        lambda x = None: call([connect])                )
@app.route('/addpoint/',    ['OPTIONS', 'POST'],        lambda x = None: call([connect, addpoint])      )
@app.route('/infos/',       ['OPTIONS', 'POST'],        lambda x = None: call([connect, infos])         )
@app.route('/share/',       ['OPTIONS', 'POST'],        lambda x = None: call([connect, share])         )
@app.route('/surname/',     ['OPTIONS', 'POST'],        lambda x = None: call([connect, surname])       )
@app.route('/allid/',       ['OPTIONS', 'POST'],        lambda x = None: call([connect, getall])        )
@app.route('/allinfos/',    ['OPTIONS', 'POST'],        lambda x = None: call([connect, getalldetails]) )
def base():
    return

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



if __name__ == '__main__':
    try:
        run(app, host=host, port=port, debug=True)
    except:
        os._exit(0)
