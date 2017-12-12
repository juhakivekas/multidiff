import os
import binascii
import re

class FileController:
	def __init__(self, model, informat):
		if informat not in ['raw', 'utf8', 'hex']:
			raise NotImplementedError('"{}" is not a valid input format for this controller'.format(informat))
		self.informat = informat
		self.model = model
		self.spaceregex = re.compile(r'\s+')

	def add_paths(self, paths):
		for path in paths:
			self.add_path(path)

	def add_path(self, path):
		if os.path.isdir(path):
			for name in os.listdir(path):
				self.add_path(os.path.join(path, name))
		elif os.path.isfile(path):
			if   self.informat == 'raw':
				data = open(path, 'rb').read(-1)
			elif self.informat == 'utf8':
				data = open(path, 'r').read(-1)
			elif self.informat == 'hex':
				hexs = open(path, 'r').read(-1)
				hexs = re.sub(self.spaceregex, '', hexs)
				data = binascii.unhexlify(hexs)
			self.model.add(data, info=path)
		else:
			raise NotImplementedError("A path was given that is neither a file nor a directory {}".format(path))
