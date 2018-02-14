# Example data provider for multidiff, watch the changes of some
# interesting memory or send data to be analyzed before encryption,
# compression, etc.
#
# source gdb_multidiff_provider.py
# break 0xinteresting
# commands
#     silent
#     multidiff [address expression] [length expression]
#     continue
# end
#
# multidiff -i json -p 53759

from base64 import b64encode
import socket
import json

class Multidiff(gdb.Command):
	'''Send data to multidiff server
multidiff ADDRESS LENGTH
  send LENGTH amount of data from ADDRESS to multidiff
  both arguments can be given as a gdb expression
multidiff setup HOST PORT
  set the host and port to where the multidiff server is running'''
	def __init__(self):
		super (Multidiff, self).__init__ ('multidiff', gdb.COMMAND_DATA)
		self.host = 'localhost'
		self.port = 0xd1ff

	def invoke(self, argument, from_tty):
		argv = gdb.string_to_argv(argument)
		if argv[0] == 'setup':
			self.setup(argv[1:])	
		else :
			self.send(argv)

	def setup(self, argv):
		self.host = argv[0]
		self.port = int(argv[1])

	def send(self, argv):
		address = gdb.parse_and_eval(argv[0])
		length  = gdb.parse_and_eval(argv[1])
		inferior = gdb.selected_inferior()
		diffobject = inferior.read_memory(address, length)

		diffmsg = {
			'data' : str(b64encode(diffobject), 'utf8'),
			'info' : 'len:{}'.format(length)
		}
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.connect((self.host, self.port))
			sock.sendall(bytes(json.dumps(diffmsg), 'utf-8'))

Multidiff()
