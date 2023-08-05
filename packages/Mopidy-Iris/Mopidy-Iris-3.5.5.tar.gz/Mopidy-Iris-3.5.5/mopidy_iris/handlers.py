
from __future__ import unicode_literals
from datetime import datetime
from tornado.escape import json_encode, json_decode
import tornado.ioloop, tornado.web, tornado.websocket, tornado.template
import random, string, logging, uuid, subprocess, pykka, ast, logging, json, urllib, urllib2, mem, requests

logger = logging.getLogger(__name__)

class WebsocketHandler(tornado.websocket.WebSocketHandler):
    
    # initiate (not the actual object __init__, but run shortly after)
    def initialize(self, core, config):
        self.core = core  
        self.config = config  

    def check_origin(self, origin):
        return True
        
    def select_subprotocol(self, subprotocols):

        # select one of our subprotocol elements and return it. This confirms the connection has been accepted.
        protocols = mem.iris.digest_protocol( subprotocols )

        # if we've auto-generated some ids, the provided subprotocols was a string, so just return it right back
        # this allows a connection to be completed
        if protocols['generated']:
            return subprotocols[0]
            
        # otherwise, just return one of the supplied subprotocols
        else:
            return protocols['clientid']

    def open(self):
    
        # decode our connection protocol value (which is a payload of id/name from javascript)
        protocolElements = mem.iris.digest_protocol(self.request.headers.get('Sec-Websocket-Protocol', []))

        connection_id = protocolElements['connection_id']
        clientid = protocolElements['clientid']
        self.connection_id = connection_id
        username = protocolElements['username']
        created = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

        # get our IP
        # if it's local, then check for proxy origin
        ip = self.request.remote_ip
        if (ip == '127.0.0.1' and hasattr(self.request.headers,'X-Forwarded-For')):
            ip = self.request.headers['X-Forwarded-For']

        # construct our client object, and add to our list of connections
        client = {
            'clientid': clientid,
            'connection_id': connection_id,
            'username': username,
            'ip': ip,
            'created': created
        }

        # add to connections
        mem.iris.add_connection(connection_id=connection_id, connection=self, client=client)
 

    def on_message(self, message):
        
        message = json_decode(message)

        if 'data' in message:
            data = message['data']
        else:
            data = {}

        # Handle hard-coded connection_id in messages
        # Otherwise include the origin connection of this message
        if 'connection_id' not in data:
            data['connection_id'] = self.connection_id

        if 'request_id' in message:
            request_id = message['request_id']
        else:
            request_id = False

        # call the method, as specified in payload
        if 'method' in message:

            # make sure the method exists
            if hasattr(mem.iris, message['method']):
                getattr(mem.iris, message['method'])(data=data, callback=lambda response: self.handle_response(response=response, request_id=request_id))

            else:
                mem.iris.raven_client.captureMessage("Method "+message['method']+" does not exist")
                self.handle_response({
                    'status': 0,
                    'message': 'Method "'+message['method']+'" does not exist',
                    'request_id': request_id
                })
        else:
            mem.iris.raven_client.captureMessage("Method key missing from request")
            self.handle_response({
                'status': 0,
                'message': 'Method key missing from request',
                'request_id': request_id
            })


    def on_close(self):
        mem.iris.remove_connection(connection_id=self.connection_id)

    ##
    # Handle a response from our core
    # This is just our callback from an Async request
    ##
    def handle_response(self, *args, **kwargs):
        response = kwargs.get('response', None)
        request_id = kwargs.get('request_id', False)

        # We've been handed an AsyncHTTPClient callback. This is the case
        # when our request calls subsequent external requests (eg Spotify, Genius)
        if isinstance(response, tornado.httpclient.HTTPResponse):
            response = {
                'response_code': response.code,
                'response_reason': response.reason,
                'response': response.body,
                'request_id': request_id
            }

        # Just a regular json object, so not an external request
        else:
            response['request_id'] = request_id
            mem.iris.send_message(connection_id=self.connection_id, data=response)
        
        mem.iris.send_message(connection_id=self.connection_id, data=response)





        
class HttpHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization, Client-Security-Token, Accept-Encoding")        

    def initialize(self, core, config):
        self.core = core
        self.config = config

    # Options request
    # This is a preflight request for CORS requests
    def options(self, slug=None):
        self.set_status(204)
        self.finish()
    
    @tornado.web.asynchronous
    def get(self, slug=None):

        # make sure the method exists
        if hasattr(mem.iris, slug):
            getattr(mem.iris, slug)(request=self.request, callback=self.handle_response)

        else:
            mem.iris.raven_client.captureMessage("Method "+slug+" does not exist")
            self.write({
                'status': 0,
                'message': 'Method "'+slug+'" does not exist'
            })
            self.finish()

    @tornado.web.asynchronous
    def post(self, slug=None):

        # make sure the method exists
        if hasattr(mem.iris, slug):
            try:
                data = json.loads(self.request.body.decode('utf-8'))
                getattr(mem.iris, slug)(data=data, request=self.request, callback=self.handle_response)

            except urllib2.HTTPError as e:
                self.write({
                    'status': 0,
                    'message': 'Invalid JSON payload'
                })
                self.finish()

        else:
            mem.iris.raven_client.captureMessage("Method "+slug+" does not exist")
            self.write({
                'status': 0,
                'message': 'Method "'+slug+'" does not exist'
            })
            self.finish()

    ##
    # Handle a response from our core
    # This is just our callback from an Async request
    ##
    def handle_response(self, response):

        # We've been handed an AsyncHTTPClient callback. This is the case
        # when our request calls subsequent external requests (eg Spotify, Genius).
        # We don't need to wrap non-HTTPResponse responses as these are dicts
        if isinstance(response, tornado.httpclient.HTTPResponse):

            # Digest JSON resposes into JSON
            content_type = response.headers.get('Content-Type')
            if content_type.startswith('application/json') or content_type.startswith('text/json'):
                body = json.loads(response.body)
            else:
                body = response.body

            response = {
                'response_code': response.code,
                'response_message': response.reason,
                'response': body
            }

        self.write(response)
        self.finish()


        
