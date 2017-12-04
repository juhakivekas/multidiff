import difflib

class Diff():
	def __init__(self, source, target, opcodes):
		self.source = source
		self.target = target
		self.opcodes = opcodes

class MultidiffModel():

	"""
	Create a MultiDiffModel for a set of objects
	"""
	def __init__(self, objects = []):
		self.clear()
		self.add_all(objects)

	"""
	Add a single object to the model
	"""
	def add(self, obj):
		self.objects.append(obj)
		self.updated = False

	"""
	Add a list of objects
	"""
	def add_all(self, objects):
		#XXX
		self.objects += objects
		self.updated = False 
		
	"""
	Clears all object and diff data
	"""
	def clear(self):
		self.objects = []		#the objects being analyzed: files, packets, lines, etc. These should be bytes or bytearrays
		self.diffs = []			#a list of diffs between objects
		self.updated = True		#tells whether the current diff is up to date with the current objects

	"""
	Diff all objects to the next one in the list
	"""
	def diff_sequence(self):
		for i in range(len(self.objects[:-1])):
			self.diff(i, i+1)
		self.updated = True

	"""
	Diff all objects against a common baseline
	"""
	def diff_baseline(self, baseline=0):
		for i in range(len(self.objects)):
			if i is baseline:
				pass
			self.diff(baseline, i)
		self.updated = True

	"""
	Diff two objects of the model and store the result
	"""
	def diff(self, source, target):
		sm = difflib.SequenceMatcher()
		sm.set_seqs(self.objects[source], self.objects[target])
		self.diffs += [Diff(source, target, sm.get_opcodes())]
		return self.diffs[-1]

