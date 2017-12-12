import sys
import binascii

class StdinController:
	def __init__(self, model, informat):
		self.model = model
		self.informat = informat
		if informat not in ['utf8', 'hex']:
			raise NotImplementedError('"{}" is not a valid input format for this controller'.format(informat))
			
	def read_lines(self):
		for num, line in enumerate(sys.stdin):
			if   self.informat == 'utf8':
				data = bytes(line[:-1], 'utf8')
			elif self.informat == 'hex':
				data = binascii.unhexlify(line[:-1])
			self.model.add(data, name='{}'.format(num))
