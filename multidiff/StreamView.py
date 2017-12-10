from multidiff import Render

class StreamView():
	def __init__(self, model, encoding='hexdump'):
		self.render = Render(color='ansi', encode=encoding)
		self.model = model
		model.add_listener(self)

	def object_added(self, index):
		if index == 0:
			return
		self.model.diff(index - 1, index)

	def diff_added(self, diff):
		print(self.model.objects[diff.target].name)
		print(self.render.render(self.model, diff))
		#clean up model to not leak memory in long runs
		del(self.model.diffs[0])
		del(self.model.objects[0])
