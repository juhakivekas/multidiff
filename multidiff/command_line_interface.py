#!/usr/bin/python3
import argparse
from multidiff import MultidiffModel, StreamView, SocketController, FileController, StdinController
import shutil
import sys

def main(args=None):

	if args is None:
		args = sys.argv[1:]
	args = make_parser().parse_args(args)
	m = MultidiffModel()

	if args.bytes != 16:
		args.width = 'max'

	if args.width == 'max':
		args.width = get_max_width(args)

	v = StreamView(m, encoding=args.outformat, mode=args.mode, color=args.color, bytes=args.bytes, width=args.width, diff=args.diff)

	if len(args.file) > 0:
		informat = args.informat if args.informat else 'raw'
		files = FileController(m, informat)
		files.add_paths(args.file)
	if args.stdin:
		informat = args.informat if args.informat else 'utf8'
		stdin = StdinController(m, informat)
		stdin.read_lines()
	if args.port:
		informat = args.informat if args.informat else 'raw'
		server = SocketController(('127.0.0.1', args.port), m, informat)
		server.serve_forever()

def get_max_width(args):
	columns = int(shutil.get_terminal_size((120,30)).columns)
	args.width = columns
	return args.width

def make_parser():
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawTextHelpFormatter,
		description="""
  \x1b[1mN E O N S E N S E\x1b[0m
  augmentations inc
  ┌───────────────┐
  │ \x1b[1mM  U  L  T  I\x1b[0m │
  │ \x1b[1mD   I   F   F\x1b[0m │
  │ sensor module │
  └───────────────┘
""")

	parser.add_argument('file',
		type=str,
		nargs='*',
		help='file or directory to include in multidiff')

	parser.add_argument('-p','--port',
		dest='port',
		type=int,
		help='start a local socket server on the given port')

	parser.add_argument('-s','--stdin',
		dest='stdin',
		action='store_true',
		help='read data from stdin, objects split by newlines')

	parser.add_argument('-m', '--mode',
		dest='mode',
		default='sequence',
		help='mode of operation, either "baseline" or "sequence"')

	parser.add_argument('-i','--informat',
		dest='informat',
		help='input data format:\n' +
			'  utf8 (stdin default)\n' +
			'  raw (file and server default)\n' +
			'  hex\n'+
			'  json')

	parser.add_argument('-o','--outformat',
		dest='outformat',
		default='hexdump',
		help='output data format:\n' +
			'  utf8\n' +
			'  hex\n' +
			'  hexdump (default)')

	parser.add_argument('--html',
		dest='color',
		action='store_const',
		const='html',
		default='ansi',
		help='use html for colors instead of ansi codes')

	parser.add_argument('-w', '--width',
		dest='width',
		default='82',
		help='number of bytes printed per line, either an integer or max(width of console)')

	parser.add_argument('-b', '--bytes',
		dest='bytes',
		default=16,
		help='number of hexs printed per line, either an integer or max(width of console)')

	parser.add_argument('-d', '--diff',
		dest='diff',
		action='store_true',
		help='only show addresses where bytes have changed(only for hexdump outformat)')
	return parser

if __name__ == '__main__':
	main()
