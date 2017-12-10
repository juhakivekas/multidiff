import binascii
import termcolor
import html

class Render():
	'''Configure the output format of this rendering object'''
	def __init__(self, view='hexdump', outformat='ansi'):
		if   outformat == 'ansi':
			self.highligther = ansi_colored
		elif outformat == 'html':
			self.highligther = html_colored

		if   view == 'hexdump':
			self.view = HexdumpView
		elif view == 'hex':
			self.view = HexView
		elif view == 'utf8':
			self.view = Utf8View
		
	'''Render the diff in the given model into a UTF-8 String'''
	def render(self, model, diff):
		result = self.view(self.highligther)
		obj = model.objects[diff.target]
		for op in diff.opcodes:
			data = obj.data[op[3]:op[4]]
			result.append(data, op[0])
		return result.final()

	'''Dump all diffs in a model. Mostly good for debugging'''
	def dumps(self, model):
		dump = ""
		for diff in model.diffs:
			dump += self.render(model, diff) + '\n'
		return dump

'''A string (utf8) view of the data'''
class Utf8View():
	def __init__(self, highligther):
		self.highligther = highligther
		self.output = ''

	def append(self, data, color):
		self.output += self.highligther(str(data, 'utf8'), color)
	
	def final(self):
		return self.output

'''A hex view of the data'''
class HexView():
	def __init__(self, highligther):
		self.highligther = highligther
		self.output = ''

	def append(self, data, color):
		data = str(binascii.hexlify(data),'utf8')
		self.output += self.highligther(data, color)
	
	def final(self):
		return self.output

'''A hexdump view of the data'''
class HexdumpView():
	def __init__(self, highligther):
		self.highligther = highligther
		self.body = ''
		self.addr = 0
		self.rowlen = 0
		self.hexrow = ''
		self.skipspace = False
		self.asciirow = ''

	def append(self, data, color):
		if len(data) == 0:
			self._append(data, color)
		while len(data) > 0:
			if self.rowlen == 16:
				self._newrow()
			consumed = self._append(data[:16 - self.rowlen], color)
			data = data[consumed:]

	def _append(self, data, color):
		if len(data) == 0:
			#in the case of highlightig a deletion in a target or an
			#addition in the source, print a highlighted space and mark
			#it skippanble for the next append
			hexs = ' ' 
			self.skipspace = True
		else:
			self._add_hex_space()
			#encode to hex and add some spaces
			hexs = str(binascii.hexlify(data), 'utf8')
			hexs = ' '.join([hexs[i:i+2] for i in range(0, len(hexs), 2)])
			asciis = ''
			#make the ascii dump
			for byte in data:
				if 0x20 <= byte <= 0x7E:
					asciis += chr(byte)
				else:
					asciis += '.'
			self.asciirow += self.highligther(asciis, color)

		self.hexrow   += self.highligther(hexs, color)
		self.rowlen += len(data)
		return len(data)

	def _newrow(self):
		self._add_hex_space()
		if self.addr != 0:
			self.body += '\n'
		self.body += "{:06x}:{:s}|{:s}|".format(
			self.addr, self.hexrow, self.asciirow);
		self.addr += 16
		self.rowlen = 0
		self.hexrow = ''
		self.asciirow = ''

	def _add_hex_space(self):
		if self.skipspace:
			self.skipspace = False
		else:
			self.hexrow += ' '
		

	def final(self):
		self.hexrow += 3*(16 - self.rowlen) * ' '
		self.asciirow += (16 - self.rowlen) * ' '
		self._newrow()
		return self.body

def ansi_colored(string, op):
	if   op == 'equal':
		return string
	elif op == 'replace':
		color = 'blue'
	elif op == 'insert':
		color = 'green'
	elif op == 'delete':
		color = 'red'
	return termcolor.colored(string, 'white', 'on_{}'.format(color))
	#return termcolor.colored(string, color, None)

def html_colored(string, op):
	if   op == 'equal':
		return string
	return "<span class='" + op + "'>" + html.escape(string) + "</span>"
