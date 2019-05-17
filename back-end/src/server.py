from bottle import Bottle, run, route, response, request, hook, error
from returnvalue import ret
from params import check
from user import user
from sql import sql
from point import point, points
import os

app = Bottle()
host = os.getenv('API_HOST', '172.0.0.1')
port = os.getenv('API_PORT', 8080)
weba = os.getenv('API_WEBA', '*')

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = weba
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@app.error(404)
def error404(error):
    return '404'

@app.error(500)
def error500(error):
    return  {"status": 500,"error": "Wrong ID"}

@app.route('/test/', method=['OPTIONS', 'POST', 'GET'])
def base():
    if request.method == 'OPTIONS':
        return {}
    try:
        params = check.json(request)
    except:
        params = []
    toret = ret(request.route.rule, params)
    return toret.ret()

@app.route('/register/', method=['OPTIONS', 'POST'])
def base():
    if request.method == 'OPTIONS':
        return {}
    params = check.json(request)
    toret = ret(request.route.rule, params)

    if not toret.err:
        err = check.contain(params, ["mail", "password", "password2"])
        if not err[0]:
            toret.add_error(err[1], err[2])

    if not toret.err:
        use = user(params["mail"], params["password"])
        err = use.register(params["password2"])
        if not err[0]:
            toret.add_error(err[1], err[2])
        else:
            toret.add_data(err[1])
    return toret.ret()

@app.route('/connect/', method=['OPTIONS', 'POST'])
def base():
    if request.method == 'OPTIONS':
        return {}
    params = check.json(request)
    toret = ret(request.route.rule, params)

    if not toret.err:
        err = check.contain(params, ["mail", "password"])
        if not err[0]:
            toret.add_error(err[1], err[2])

    if not toret.err:
        use = user(params["mail"], params["password"])
        err = use.connect()
        if not err[0]:
            toret.add_error(err[1], err[2])
        else:
            toret.add_data(err[1])
    return toret.ret()

@app.route('/addpoint/', method=['OPTIONS', 'POST'])
def base():
    if request.method == 'OPTIONS':
        return {}
    params = check.json(request)
    toret = ret(request.route.rule, params)

    if not toret.err:
        err = check.contain(params, ["mail", "token", "key", "sig_id"])
        if not err[0]:
            toret.add_error(err[1], err[2])

    if not toret.err:
        use = user(params["mail"], None, params["token"])
        err = use.connect()
        if not err[0]:
            toret.add_error(err[1], err[2])
        else:
            toret.add_data(err[1])

    if not toret.err:
        device = point(None, use.id, params["key"], params["sig_id"])
        err = device.infos()
        if not err[0]:
            toret.add_error(err[1], err[2])
        else:
            toret.add_data(err[1])
    return toret.ret()

@app.route('/infos/', method=['OPTIONS', 'POST'])
def base():
    if request.method == 'OPTIONS':
        return {}
    params = check.json(request)
    toret = ret(request.route.rule, params)

    if not toret.err:
        err = check.contain(params, ["mail", "token", "point_id"])
        if not err[0]:
            toret.add_error(err[1], err[2])

    if not toret.err:
        use = user(params["mail"], None, params["token"])
        err = use.connect()
        if not err[0]:
            toret.add_error(err[1], err[2])
        else:
            toret.add_data(err[1])

    if not toret.err:
        device = point(params["point_id"], use.id)
        err = device.infos()
        if not err[0]:
            toret.add_error(err[1], err[2])
        else:
            toret.add_data(err[1])
    return toret.ret()

@app.route('/share/', method=['OPTIONS', 'POST'])
def base():
    if request.method == 'OPTIONS':
        return {}
    params = check.json(request)
    toret = ret(request.route.rule, params)

    if not toret.err:
        err = check.contain(params, ["mail", "token", "mail_to", "point_id"])
        if not err[0]:
            toret.add_error(err[1], err[2])

    if not toret.err:
        use = user(params["mail"], None, params["token"])
        err = use.connect()
        if not err[0]:
            toret.add_error(err[1], err[2])
        else:
            toret.add_data(err[1])

    if not toret.err:
        device = point(params["point_id"], use.id)
        err = device.share(params["mail_to"])
        if not err[0]:
            toret.add_error(err[1], err[2])
        else:
            toret.add_data(err[1])
    return toret.ret()

@app.route('/surname/', method=['OPTIONS', 'POST'])
def base():
    if request.method == 'OPTIONS':
        return {}
    params = check.json(request)
    toret = ret(request.route.rule, params)

    if not toret.err:
        err = check.contain(params, ["mail", "token", "surname", "point_id"])
        if not err[0]:
            toret.add_error(err[1], err[2])

    if not toret.err:
        use = user(params["mail"], None, params["token"])
        err = use.connect()
        if not err[0]:
            toret.add_error(err[1], err[2])
        else:
            toret.add_data(err[1])

    if not toret.err:
        device = point(params["point_id"], use.id)
        err = device.rename(params["surname"])
        if not err[0]:
            toret.add_error(err[1], err[2])
        else:
            toret.add_data(err[1])
    return toret.ret()

if __name__ == '__main__':
        try:
            run(app, host=host, port=port, debug=True)
        except:
            os._exit(0)
