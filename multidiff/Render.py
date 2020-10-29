from multidiff.Ansi import Ansi
import binascii
import html
import textwrap
import re

class Render():
	def __init__(self, encoder='hexdump', color='ansi', bytes=16, width=None):
		'''Configure the output encoding and coloring method of this rendering object'''
		if   color == 'ansi':
			self.highligther = ansi_colored
		elif color == 'html':
			self.highligther = html_colored

		if   encoder == 'hexdump':
			self.encoder = HexdumpEncoder
		elif encoder == 'hex':
			self.encoder = HexEncoder
		elif encoder == 'utf8':
			self.encoder = Utf8Encoder

		self.width = width
		self.bytes = bytes
		self.stats = []

	def render(self, model, diff):
		'''Render the diff in the given model into a UTF-8 String'''
		result = self.encoder(self.highligther)
		obj = model.objects[diff.target]
		for op in diff.opcodes:
			data = obj.data[op[3]:op[4]]
			data2 = ""
			if type(data) == bytes:
				result.append(data, op[0], self.width, self.bytes, data2)
			elif type(data) == str:
				result.append(bytes(data, "utf8"), op[0], self.width, self.bytes, bytes(data2, "utf8"))
		if result.additions or result.deletions:
			self.stats = [result.additions, result.deletions]
		if self.bytes != 16:
			return result.reformat(result.final(data2), int(self.bytes))
		return result.final(data2)

	def diff_render(self, model, diff):
		'''Render the smaller diff in the given model into a UTF-8 String '''
		result = self.encoder(self.highligther)
		obj1 = model.objects[diff.target-1]
		obj2 = model.objects[diff.target]
		for op in diff.opcodes:
			data1 = obj1.data[op[1]:op[2]]
			data2 = obj2.data[op[3]:op[4]]
			if type(data2) == bytes:
				result.append(data1, op[0], self.width, self.bytes, data2)
			elif type(data2) == str:
				result.append(bytes(data1, "utf8"), op[0], self.width, self.bytes, bytes(data2, "utf8"))
		if result.additions or result.deletions:
			self.stats = [result.additions, result.deletions]
		if self.bytes != 16:
			return result.reformat(result.final(data2), int(self.bytes))
		return result.final(data2).rstrip()

	def dumps(self, model):
		'''Dump all diffs in a model. Mostly good for debugging'''
		dump = ""
		for diff in model.diffs:
			dump += self.render(model, diff) + '\n'
		return dump

class Utf8Encoder():
	'''A string (utf8) encoder for the data'''
	def __init__(self, highligther):
		self.highligther = highligther
		self.output = ''
		self.additions = 0
		self.deletions = 0

	def append(self, data, color, width=None, bytes=16, data2=""):
		self.output += self.highligther(str(data, 'utf8'), color)
		if width:
			if len(self.output) > int(width):
				self.output = textwrap.fill(self.output, int(width))

	def final(self, data):
		return self.output

class HexEncoder():
	'''A hex encoder for the data'''
	def __init__(self, highligther):
		self.highligther = highligther
		self.output = ''
		self.additions = 0
		self.deletions = 0

	def append(self, data, color, width=None, bytes=16, data2=""):
		data = str(binascii.hexlify(data),'utf8')
		self.output += self.highligther(data, color)
		if width:
			if len(self.output) > int(width):
				self.output = textwrap.fill(self.output, int(width))

	def final(self, data):
		return self.output

class HexdumpEncoder():
	'''A hexdump encoder for the data'''
	def __init__(self, highligther):
		self.highligther = highligther
		self.body = ''
		self.addr = 0
		self.rowlen = 0
		self.hexrow = ''
		self.skipspace = False
		self.asciirow = ''
		self.additions = 0
		self.deletions = 0

	def append(self, data, color, width=None, bytes=16, data2=""):
		if data2 == "":
			if len(data) == 0:
				self._append(data, color, width, data2)
			while len(data) > 0:
				if self.rowlen == 16:
					self._newrow(data2)
				consumed = self._append(data[:16 - self.rowlen], color, width, data2)
				data = data[consumed:]
		else:
			data1 = data
			if len(data2) == 0:
				self._append(data1, color, width, data2)
			while len(data2) > 0:
				if self.rowlen == 16:
					self._newrow(data2)
				consumed = self._append(data1[:16 - self.rowlen], color, width, data2[:16 - self.rowlen],)
				data2 = data2[consumed:]

	def stats(self, string, op, string2):
		if op == 'insert':
			self.additions += len(string.split())
		if op == 'delete':
			self.deletions += len(string.split())
		if op == 'replace':
			self.additions += len(string.split())
			self.deletions += len(string2.split())

	def _append(self, data, color, width, data2):
		if data2 == "":
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

			self.hexrow += self.highligther(hexs, color)
			if width:
				if len(self.hexrow) > int(width):
					self.hexrow = textwrap.fill(self.hexrow, int(width))
			self.rowlen += len(data)
			return len(data)
		else:
			data1 = data
			# <deletion>
			if len(data2) == 0:
				hexs = str(binascii.hexlify(data1), 'utf8')
				hexs = ' '.join([hexs[i:i+2] for i in range(0, len(hexs), 2)])
				hexs2 = str(binascii.hexlify(data2), 'utf8')
				hexs2 = ' '.join([hexs[i:i+2] for i in range(0, len(hexs), 2)])
			else:
				self._add_hex_space()
				#encode to hex and add some spaces
				hexs = str(binascii.hexlify(data2), 'utf8')
				hexs = ' '.join([hexs[i:i+2] for i in range(0, len(hexs), 2)])
				hexs2 = str(binascii.hexlify(data), 'utf8')
				hexs2 = ' '.join([hexs[i:i+2] for i in range(0, len(hexs), 2)])

			self.hexrow += self.highligther(hexs, color)
			self.stats(hexs, color, hexs2)
			if width:
				if len(self.hexrow) > int(width):
					self.hexrow = textwrap.fill(self.hexrow, int(width))
			self.rowlen += len(data2)
			return len(data2)

	def _newrow(self, data):
		self._add_hex_space()
		ops = ['insert', 'delete', 'replace', Ansi.delete, Ansi.replace, Ansi.insert]
		if data == "":
			if self.addr != 0:
				self.body += '\n'
			self.body += "{:06x}:{:s}|{:s}|".format(
				self.addr, self.hexrow, self.asciirow);
		else:
			if self.addr != 0:
				self.body = self.body
			if any(ext in self.hexrow for ext in ops):
				self.body += "{:06x}:{:s}\n".format(
				self.addr, self.hexrow);
		self.addr += 16
		self.rowlen = 0
		self.hexrow = ''
		self.asciirow = ''

	def _add_hex_space(self):
		if self.skipspace:
			self.skipspace = False
		else:
			self.hexrow += ' '


	def final(self, data=""):
		self.hexrow += 3*(16 - self.rowlen) * ' '
		self.asciirow += (16 - self.rowlen) * ' '
		self._newrow(data)
		return self.body

	def reformat(self, body, n=16):
		asciis = ''
		instring = ''
		foo = body.split('\n')
		for line in foo:
			line.rstrip()
			line = line[line.find(':')+1:line.find('|')]
			instring += line
			instring += '\n'
		outstring = ''
		# Remove line numbers and newlines.
		clean_string = instring.replace(r'\d+:|\n', '')
		# Split on spaces that are not in tags.
		elements = re.split(r'\s+(?![^<]+>)', clean_string)
		# Omit first tag so that everything else can be chunked by n.
		clean_elements = elements[1:]
		# Chunk by n.
		chunks = [' '.join(clean_elements[i:i+n])
         	for i in range(0, len(clean_elements), n)]
		# Concatenate the chunks as a line in outstring, with a line number.
		for i, chunk in enumerate(chunks):
			asciis = ''
			ansi = [Ansi.reset, Ansi.delete, Ansi.replace, Ansi.insert]
			html = ["<span class='delete'>", "<span class='insert'>", "<span class='replace'>", "</span>"]
			res = chunk
			if self.highligther == html_colored:
				ops = html
			else:
				ops = ansi
			for op in ops:
				res = res.replace(op, "")
			res = res.replace(" ", "").strip()
			res = str(binascii.unhexlify(res), 'utf8')
			res = res.encode('utf-8')
			#make the ascii dump
			for byte in res:
				if 0x20 <= byte <= 0x7E:
					asciis += chr(byte)
				else:
					asciis += '.'
			addr = '{:06x}'.format(i*n)
			if i == 0:
				outstring += '{}:{} {} |{}|\n'.format(addr, elements[0], chunk, asciis)
			else:
				outstring += '{}: {} |{}|\n'.format(addr, chunk, asciis)
		return outstring

def ansi_colored(string, op):
	if   op == 'equal':
		return string
	elif op == 'replace':
		color = Ansi.replace
	elif op == 'insert':
		color = Ansi.insert
	elif op == 'delete':
		color = Ansi.delete
	return color + string + Ansi.reset

def html_colored(string, op):
	if   op == 'equal':
		return string
	return "<span class='" + op + "'>" + html.escape(string) + "</span>"
