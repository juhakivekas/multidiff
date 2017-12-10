import difflib

"""A diff result of a diff of two objects"""
class Diff():
	def __init__(self, source, target, opcodes):
		self.source = source
		self.target = target
		self.opcodes = opcodes

"""A diffable object. Raw byte data and some metadata."""
class DiffObject():
	def __init__(self, data, name='', identifier=0):
		self.data = data
		self.name = name

class MultidiffModel():

	"""Create a MultiDiffModel for a set of objects"""
	def __init__(self, datas = []):
		self.clear()
		self.add_all(datas)
		self.listeners = []

	"""Adds an object that listens to events. Views add themselves."""
	def add_listener(self, listener):
		self.listeners.append(listener)

	"""Add a single data object to the model"""
	def add(self, data, name=''):
		obj = DiffObject(data, name=name)
		self.objects.append(obj)
		for listener in self.listeners:
			listener.object_added(len(self.objects) - 1)

	"""Add a list of byte datas"""
	def add_all(self, datas, name=''):
		for data in datas:
			self.add(data)
		
	"""Clears all object and diff data"""
	def clear(self):
		#the objects being analyzed:
		#files, packets, lines, etc. backed by bytes or bytearrays
		self.objects = []
		#a list of diffs between objects
		self.diffs = []

	"""Diff all objects to the next one in the list"""
	def diff_sequence(self):
		for i in range(len(self.objects[:-1])):
			self.diff(i, i+1)

	"""Diff all objects against a common baseline"""
	def diff_baseline(self, baseline=0):
		for i in range(len(self.objects)):
			if i is baseline:
				pass
			self.diff(baseline, i)

	"""Diff two objects of the model and store the result"""
	def diff(self, source, target):
		sm = difflib.SequenceMatcher()
		sm.set_seqs(self.objects[source].data, self.objects[target].data)
		diff = Diff(source, target, sm.get_opcodes())
		self.diffs.append(diff)
		for listener in self.listeners:
			listener.diff_added(diff)
		return self.diffs[-1]

