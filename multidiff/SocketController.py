import socketserver
import json
import base64

class SocketController(socketserver.TCPServer):
	"""A simple wrapper that provides the handler class with a model"""
	def __init__(self, server_address, model, bind_and_activate=True):
		self.model = model
		socketserver.TCPServer.__init__(self, server_address, MultidiffTCPHandler, bind_and_activate=True)

class MultidiffTCPHandler(socketserver.BaseRequestHandler):
	"""Receives one diffable packet from a socket and adds it to the model"""
	def handle(self):
		data = self.request.recv(0x10000)
		msg  = json.loads(str(data, 'utf8'))
		data = base64.b64decode(msg['data'], altchars="-_")
		name = msg['name']
		self.server.model.add(data, name=name)
