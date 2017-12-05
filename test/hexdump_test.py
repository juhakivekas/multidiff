from multidiff.render import *

def mono(string, color):
	return string

def test_single_line_mono():
	hd = HexdumpView(mono)
	hd.append(bytes("foobar", "utf8"), "mono")
	result = hd.final()
	dump = '000000: 66 6f 6f 62 61 72                                |foobar          |'
	assert(result == dump)

def test_multiple_line_mono():
	hd = HexdumpView(mono)
	hd.append(bytes("0123456789abcdef012345678", "utf8"), "mono")
	result = hd.final()
	dump='000000: 30 31 32 33 34 35 36 37 38 39 61 62 63 64 65 66  |0123456789abcdef|\n000010: 30 31 32 33 34 35 36 37 38                       |012345678       |'
	assert(result == dump)

def test_single_line_insert():
	hd = HexdumpView(ansi_colored)
	hd.append(bytes("foobar", "utf8"), "insert")
	result = hd.final()
	print(result)
	dump = '000000: \x1b[42m\x1b[37m66 6f 6f 62 61 72 \x1b[0m                               |\x1b[42m\x1b[37mfoobar\x1b[0m          |'
	assert(result == dump)

def test_multiple_line_insert():
	hd = HexdumpView(ansi_colored)
	hd.append(bytes("012345678a", "utf8"), "equal")
	hd.append(bytes("012345678a", "utf8"), "replace")
	result = hd.final()
	#jesus!
	dump = '000000: 30 31 32 33 34 35 36 37 38 61 '
	dump += '\x1b[44m\x1b[37m30 31 32 33 34 35 \x1b[0m'
	dump += ' |012345678a'
	dump += '\x1b[44m\x1b[37m012345\x1b[0m'
	dump += '|\n000010: '
	dump += '\x1b[44m\x1b[37m36 37 38 61 \x1b[0m'
	dump += '                                     |'
	dump += '\x1b[44m\x1b[37m678a\x1b[0m'
	dump += '            |'
	assert(result == dump)
