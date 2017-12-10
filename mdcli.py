#!/usr/bin/python3
import argparse
from multidiff import MultidiffModel, StreamView, SocketController, FileController

parser = argparse.ArgumentParser(
	formatter_class=argparse.RawDescriptionHelpFormatter,
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

parser.add_argument('-m', '--mode',
	dest='mode',
	default='sequence',
	help='mode of operation, either "baseline" or "sequence"')

parser.add_argument('-e','--encode',
	dest='encode',
	default='hexdump',
	help='encoding of the output data, one of "hex", "hexdump", or "utf8"')

parser.add_argument('-p','--port',
	dest='port',
	default=0,
	type=int,
	help='start a local socket server on a port')

if __name__ == '__main__':
	args = parser.parse_args()
	m = MultidiffModel()
	v = StreamView(m, encoding=args.encode)
	f = FileController(m)
	f.add_paths(args.file)
	if args.port != 0:
		s = SocketController(('127.0.0.1', args.port), m)
		s.serve_forever()
