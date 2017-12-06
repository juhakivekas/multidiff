import socketserver
import json
import base64
from multidiff import MultidiffModel, Render

class MyTCPHandler(socketserver.BaseRequestHandler):
	"""Receives one diffable packet from a socket and adds it to the model"""
	def handle(self):
		data = self.request.recv(0x10000)
		msg = json.loads(str(data, 'utf8'))
		m.add(base64.b64decode(msg['data'], altchars="-_"), name=msg['name'])
		nobjs = len(m.objects)
		if nobjs >1:
			d = m.diff(nobjs - 2, nobjs -1)
			print(m.objects[-1].name)
			print(r.render(m, d))

if __name__ == "__main__":
	r = Render(outformat='ansi', view='hexdump')
	m = MultidiffModel() 
	HOST, PORT = "127.0.0.1", 8000

	# Create the server, binding to localhost on port 9999
	server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	server.serve_forever()
