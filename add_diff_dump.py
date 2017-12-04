from multidiff import MultidiffModel, Render
import os
import sys

def get_object(path):
	return open(path, 'rb').read(-1)[:0x40]

r = Render(outformat='ansi', view='hexdump')
m = MultidiffModel()
source = get_object(sys.argv[1])
m.add(source)
targetdir = sys.argv[2]
for index, target in enumerate(os.listdir(targetdir)):
	obj = get_object(targetdir + target)
	m.add(obj)
	d = m.diff(index, index + 1)
	print(r.render(m, d))
	print()
