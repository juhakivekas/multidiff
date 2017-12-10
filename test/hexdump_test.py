from multidiff.render import *
from multidiff import Ansi

def mono(string, color):
	return string

def test_single_line_mono():
	hd = HexdumpEncoder(mono)
	hd.append(bytes("foobar", "utf8"), "mono")
	result = hd.final()
	dump = '000000: 66 6f 6f 62 61 72                               |foobar          |'
	assert(result == dump)

def test_multiple_line_mono():
	hd = HexdumpEncoder(mono)
	hd.append(bytes("0123456789abcdef012345678", "utf8"), "mono")
	result = hd.final()
	dump = '000000: 30 31 32 33 34 35 36 37 38 39 61 62 63 64 65 66 |0123456789abcdef|\n'
	dump+= '000010: 30 31 32 33 34 35 36 37 38                      |012345678       |'
	assert(result == dump)

def test_single_line_insert():
	hd = HexdumpEncoder(ansi_colored)
	hd.append(bytes("foobar", "utf8"), "insert")
	result = hd.final()
	print(result)
	dump = '000000: '
	dump+= Ansi.white + Ansi.on_green + '66 6f 6f 62 61 72' + Ansi.reset
	dump+= '                               |'
	dump+= Ansi.white + Ansi.on_green + 'foobar' + Ansi.reset
	dump+= '          |'
	assert(result == dump)

def test_multiple_line_insert():
	hd = HexdumpEncoder(ansi_colored)
	hd.append(bytes("012345678a", "utf8"), "equal")
	hd.append(bytes("012345678a", "utf8"), "replace")
	result = hd.final()
	#jesus!
	dump = '000000: 30 31 32 33 34 35 36 37 38 61 '
	dump += Ansi.white + Ansi.on_blue + '30 31 32 33 34 35' + Ansi.reset
	dump += ' |012345678a'
	dump += Ansi.white + Ansi.on_blue + '012345' + Ansi.reset
	dump += '|\n000010: '
	dump += Ansi.white + Ansi.on_blue + '36 37 38 61' + Ansi.reset
	dump += '                                     |'
	dump += Ansi.white + Ansi.on_blue + '678a' + Ansi.reset
	dump += '            |'
	assert(result == dump)

def test_empty_data_insert():
	hd = HexdumpEncoder(ansi_colored)
	hd.append(bytes("A", "utf8"), "replace")
	hd.append(bytes("", "utf8"), "delete")
	result = hd.final()
	print(result)
	dump = '000000: '
	dump += Ansi.white + Ansi.on_blue + '41' + Ansi.reset
	dump += Ansi.white + Ansi.on_red + ' ' + Ansi.reset
	dump += '                                             |'
	dump += Ansi.white + Ansi.on_blue + 'A' + Ansi.reset
	dump += '               |'
	assert(result == dump)
