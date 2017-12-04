#!/usr/bin/python3
import argparse

from multidiff import MultidiffModel, Render, BaselineView
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QTextDocument
import sys


parser = argparse.ArgumentParser(description='The multidiff tool of the future.')
parser.add_argument('file',
	metavar='file',
	type=str,
	nargs='+',
	help='a file to include in the diff')

parser.add_argument('-x','--hexdump',
	dest='view',
	action='store_const',
	const='hexdump',
	default='utf8',
	help='hex encode output')

parser.add_argument('--qt',
	dest='qt',
	action='store_const',
	const=True,
	default=False,
	help='view resilts in Qt user interface')

args = parser.parse_args()


style = open("multidiff/baselineview.css").read(-1)

if __name__ == '__main__':
	
	objs = open(args.file[0]).read(-1).split('\n')[:-1]
	objs = [bytes(x,'utf8') for x in objs]
	m = MultidiffModel(objs)
	m.diff_baseline()

	if args.qt:
		res = Render(outformat='html', view=args.view).dumps(m)
		app = QApplication(sys.argv)
		view = BaselineView()
		doku = QTextDocument("", None)
		doku.setDefaultStyleSheet(style)
		doku.setHtml("<pre>" + res + "</pre>")
		view.setDocument(doku)
		sys.exit(app.exec_())
	else:
		res = Render(outformat='ansi', view=args.view).dumps(m)
		print(res)
