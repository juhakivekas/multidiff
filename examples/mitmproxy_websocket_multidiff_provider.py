# Usage:
#   mitmdump -s "mitmproxy_websocket_multidiff_provider.py 8000"
#   multidiff -i json -p 8000
# point your browser to mitmdump and open some websocket application

import binascii
import socket
from base64 import b64encode
import json
import sys

HOST, PORT = "localhost", int(sys.argv[1])

def websocket_message(flow):
	direction = "\u25b6" if flow.messages[-1].from_client else "\u25c0" 
	diffmsg = {
		'data' : str(b64encode(flow.messages[-1].content), 'utf8'),
		'info' : '{} {}'.format(direction, len(flow.messages))
	}
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.connect((HOST, PORT))
		sock.sendall(bytes(json.dumps(diffmsg), "utf-8"))
