from multidiff.render import *

def mono(string, color):
	return string

def test_single_line_mono():
	hd = HexdumpView(mono)
	hd.append(bytes("foobar", "utf8"), "mono")
	result = hd.final()
	dump = '000000: 666f6f626172                     |foobar          |\n'
	assert(result == dump)

def test_multiple_line_mono():
	hd = HexdumpView(mono)
	hd.append(bytes("0123456789abcdef012345678", "utf8"), "mono")
	result = hd.final()
	dump='000000: 30313233343536373839616263646566 |0123456789abcdef|\n000010: 303132333435363738               |012345678       |\n'
	assert(result == dump)

def test_single_line_insert():
	hd = HexdumpView(ansi_colored)
	hd.append(bytes("foobar", "utf8"), "insert")
	result = hd.final()
	print(result)
	dump = '000000: \x1b[42m\x1b[37m666f6f626172\x1b[0m                     |\x1b[42m\x1b[37mfoobar\x1b[0m          |\n'
	assert(result == dump)

def test_single_line_insert():
	hd = HexdumpView(ansi_colored)
	hd.append(bytes("012345678a", "utf8"), "equal")
	hd.append(bytes("012345678a", "utf8"), "replace")
	result = hd.final()
	#jesus!
	dump = '000000: 30313233343536373861'
	dump += '\x1b[44m\x1b[37m303132333435\x1b[0m'
	dump += ' |012345678a'
	dump += '\x1b[44m\x1b[37m012345\x1b[0m'
	dump += '|\n000010: '
	dump += '\x1b[44m\x1b[37m36373861\x1b[0m'
	dump += '                         |'
	dump += '\x1b[44m\x1b[37m678a\x1b[0m'
	dump += '            |\n'
	assert(result == dump)
