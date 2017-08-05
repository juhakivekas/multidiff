import binascii
import termcolor
import html

class Render():
	def __init__(self, outformat='ansi', outencode='utf8'):
		self.outformat = outformat
		self.outencode = outencode
		pass

	def dump(self, model, reference=0):
		print(self.dumps(model, reference=reference), end='')

	def dumps(self, model, reference=0):
		#print a reference object
		#string = model.objects[reference]
		#if printmode == 'hex':
		#	string = str(binascii.hexlify(bytes(string,"utf8")),'utf8')
		#dump = string + "\n"

		#XXX this assumes that the diffs are somehow cleverly created
		#eg. a sequece or baseline diff
		dump = ""
		for diff in model.diffs:
			obj = model.objects[diff.target]
			for op in diff.opcodes:
				string = obj[op[3]:op[4]]
				if self.outencode == 'hex':
					string = str(binascii.hexlify(bytes(string,"utf8")),'utf8')
				
				if   self.outformat == 'ansi':
					dump += self.ansi_colored(string, op[0])
				elif self.outformat == 'html':
					dump += self.html_colored(string, op[0])
			dump += "\n"
		return dump

	def ansi_colored(self, string, op):
		if   op == 'equal':
			return string
		elif op == 'replace':
			bgcolor = 'on_blue'
		elif op == 'insert':
			bgcolor = 'on_green'
		elif op == 'delete':
			bgcolor = 'on_red'
		return termcolor.colored(string, 'white', bgcolor)

	def html_colored(self, string, op):
		if   op == 'equal':
			return string
		return "<span class='" + op + "'>" + html.escape(string) + "</span>"

