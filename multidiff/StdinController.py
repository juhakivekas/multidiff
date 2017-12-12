import sys
import binascii

class StdinController:
	def __init__(self, model, mode):
		self.model = model
		self.mode = mode

	def read_lines(self):
		for num, line in enumerate(sys.stdin):
			#XXX maybe not always bytes?
			if self.mode == 'line':
				data = bytes(line[:-1], 'utf8')
			elif self.mode == 'hex':
				data = binascii.unhexlify(line[:-1])
			#self.model.add(data)
			self.model.add(data, name='{}'.format(num))
