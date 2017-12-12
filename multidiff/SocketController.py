import socketserver
import json
import base64

class SocketController(socketserver.TCPServer):
	"""A simple wrapper that provides the handler class with a model"""
	def __init__(self, server_address, model, informat, bind_and_activate=True):
		if informat not in ['json']:
			raise NotImplementedError('"{}" is not a valid input format for this controller'.format(informat))
		self.model = model
		self.informat = informat
		socketserver.TCPServer.__init__(self, server_address, MultidiffTCPHandler, bind_and_activate=True)

class MultidiffTCPHandler(socketserver.BaseRequestHandler):
	"""Receives one diffable packet from a socket and adds it to the model"""
	def handle(self):
		data = self.request.recv(0x10000)
		msg  = json.loads(str(data, 'utf8'))
		data = base64.b64decode(msg['data'], altchars="-_")
		name = msg['name']
		self.server.model.add(data, name=name)
