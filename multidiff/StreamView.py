from multidiff import Render, Ansi
import html

class StreamView():
	'''A class for building UIs. Has some pretty serious side effects.
	Use Render instead if you're not making a long-running UI'''
	def __init__(self, model, encoding='hexdump', mode='sequence', color='ansi'):
		self.color = color
		self.render = Render(color=color, encoder=encoding)
		self.mode = mode
		self.model = model
		model.add_listener(self)

	def object_added(self, index):
		if index > 0:
			self.model.diff(index - 1, index)

	def diff_added(self, diff):
		if  self.model.objects[diff.target].info != '':
			if self.color == 'ansi':
				print(Ansi.bold + self.model.objects[diff.target].info + Ansi.reset)
			elif self.color == 'html':
				print('<span style="font-weight: bold;">' + html.escape(self.model.objects[diff.target].info) + '</span>')
		print(self.render.render(self.model, diff))
		#StreamView is designed to run for long times so we delete
		#old objects and diffs to not leak memory
		del(self.model.diffs[0])
		if   self.mode == 'sequence':
			del(self.model.objects[0])
		elif self.mode == 'baseline':
			del(self.model.objects[1])
