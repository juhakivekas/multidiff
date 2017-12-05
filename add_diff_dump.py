from multidiff import MultidiffModel, Render
import os
import sys

def get_object(path):
	return open(path, 'rb').read(-1)#[:0xa0]

r = Render(outformat='ansi', view='hexdump')
m = MultidiffModel()
source = get_object(sys.argv[1])
m.add(source)
targetdir = sys.argv[2]
for index, target in enumerate(os.listdir(targetdir)):
	obj = get_object(targetdir + target)
	m.add(obj)
	d = m.diff(0, index + 1)
	#for easier paging in "less -r"
	print('======== ' + target)
	print(r.render(m, d))
	#print()
