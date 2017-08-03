import binascii
from termcolor import colored

class AnsiView():
	def __init__(self):
		pass

	def dump(self, model, reference=0, printmode = 'utf8'):
		print(self.dumps(model, reference=reference, printmode = printmode), end='')

	def dumps(self, model, reference=0, printmode = 'utf8'):
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
				if   op[0] == 'equal':
					bgcolor = ''
				elif op[0] == 'replace':
					bgcolor = 'on_blue'
				elif op[0] == 'insert':
					bgcolor = 'on_green'
				elif op[0] == 'delete':
					bgcolor = 'on_red'
				
				string = obj[op[3]:op[4]]
				if printmode == 'hex':
					string = str(binascii.hexlify(bytes(string,"utf8")),'utf8')
				if bgcolor is not '':
					dump += colored(string, 'white', bgcolor)
				else:
					dump += string
			dump += "\n"
		return dump
