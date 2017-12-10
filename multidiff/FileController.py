import os

class FileController:
	def __init__(self, model):
		self.model = model

	def add_paths(self, paths):
		for path in paths:
			self.add_path(path)

	def add_path(self, path):
		if os.path.isdir(path):
			for name in os.listdir(path):
				self.add_path(os.path.join(path, name))
		elif os.path.isfile(path):
			data = open(path, 'rb').read(-1)
			self.model.add(data, name=path)
		else:
			raise NotImplemented
