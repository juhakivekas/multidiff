#!/usr/bin/python3
import argparse

from multidiff import MultidiffModel, StreamView, SocketController
import sys

parser = argparse.ArgumentParser(description='The multidiff tool of the future.')

parser.add_argument('file',
	metavar='file',
	type=str,
	nargs='*',
	help='a file or directory whose content is to be included in the multidiff')

parser.add_argument('-e','--encode',
	dest='encode',
	default='hexdump',
	help='choose encoding of the data. One of "hex", "hexdump", or "utf8"')

parser.add_argument('-p','--port',
	dest='port',
	type=int,
	help='start a local socket server on a port')

if __name__ == '__main__':
	args = parser.parse_args()
	m = MultidiffModel()
	v = StreamView(m, encoding=args.encode)
	#f = FileController(m)
	#f.add_files(args.files)
	s = SocketController(('127.0.0.1', args.port), m)
	s.serve_forever()
