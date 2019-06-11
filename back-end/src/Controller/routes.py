from .routesfunc import *

def setuproute(app, call):
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
