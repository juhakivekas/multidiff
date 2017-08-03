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
	def __init__(self, objects):
		self.objects = objects
		self.diffs = []

	"""
	Diff all objects to the next one in the list
	"""
	def diff_sequence(self):
		for i in range(len(self.objects[:-1])):
			self.diff(i, i+1)

	"""
	Diff all objects against a common baseline
	"""
	def diff_baseline(self, baseline=0):
		for i in range(len(self.objects)):
			if i is baseline:
				pass
			self.diff(baseline, i)

	"""
	Diff two objects of the model and store the result
	"""
	def diff(self, a, b):
		sm = difflib.SequenceMatcher()
		sm.set_seqs(self.objects[a], self.objects[b])
		self.diffs += [Diff(a, b, sm.get_opcodes())]

