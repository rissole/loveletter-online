# -*- coding: utf-8 -*-

def log_request(self):
    log = self.server.log
    if log:
        if hasattr(log, 'info'):
            log.info(self.format_request() + '\n')
        else:
            log.write(self.format_request() + '\n')


from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException
# Monkeys are made for freedom.
try:
    import gevent
    from geventwebsocket.gunicorn.workers import GeventWebSocketWorker as Worker
except ImportError:
    pass

if 'gevent' in locals():
    # Freedom-Patch logger for Gunicorn.
    if hasattr(gevent, 'pywsgi'):
        gevent.pywsgi.WSGIHandler.log_request = log_request



class SocketMiddleware(object):

    def __init__(self, wsgi_app, socket):
        self.ws = socket
        self.app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        urls = self.ws.url_map.bind_to_environ(environ)

        try:
            endpoint, arguments = urls.match(path)
            handler = self.ws.mapped_functions[endpoint]
            environment = environ['wsgi.websocket']
            handler(environment, **arguments)
        except HTTPException:
            return self.app(environ, start_response)


class Sockets(object):

    def __init__(self, app=None):
        self.url_map = Map()
        self.mapped_functions = {}
        if app:
            self.init_app(app)

    def init_app(self, app):
        app.wsgi_app = SocketMiddleware(app.wsgi_app, self)

    def route(self, rule, **options):

        def decorator(f):
            endpoint = options.pop('endpoint', f.__name__)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator

    def add_url_rule(self, rule, endpoint, f, **options):
        self.url_map.add(Rule(
            rule,
            endpoint=endpoint,
            **options
        ))
        if f is not None:
            old_func = self.mapped_functions.get(endpoint)
            if old_func is not None and old_func != view_func:
                raise AssertionError('View function mapping is overwriting an '
                                     'existing endpoint function: %s' % endpoint)
            self.mapped_functions[endpoint] = f

# CLI sugar.
if 'Worker' in locals():
    worker = Worker