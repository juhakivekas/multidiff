from multidiff.Render import *
from multidiff import Ansi
from multidiff.command_line_interface import make_parser, get_max_width

import shutil
from unittest import TestCase
import argparse


class WidthTests(TestCase):

    def setUp(self):
        pass

    def test_parser(self):
        args = make_parser().parse_args([])
        res = argparse.Namespace(
            bytes=16, color='ansi', file=[], informat=None,
            mode='sequence', outformat='hexdump', port=None, stdin=False,
            width='82'
        )
        assert(args == res)

    def test_get_max_width(self):
        args = make_parser().parse_args(['--width', 'max'])
        args.width = get_max_width(args)
        columns = int(shutil.get_terminal_size((120, 30)).columns)
        assert(args.width == columns)

    def test_width_default(self):
        # width = 82(default)
        args = make_parser().parse_args([])
        args.width = get_max_width(args)
        hd = HexdumpEncoder(html_colored)
        hd.append(bytes("012", "utf8"), "replace", args.width)
        hd.append(bytes("3456789ab", "utf8"), "equal", args.width)
        hd.append(bytes("", "utf8"), "delete", args.width)
        hd.append(bytes("cdef", "utf8"), "equal", args.width)
        result = hd.final()

        dump = "000000: "
        dump += "<span class='replace'>30 31 32</span> "
        dump += "33 34 35 36 37 38 39 61 62"
        dump += "<span class='delete'> </span>"
        dump += "63 64 65 66"
        dump += " |"
        dump += "<span "
        dump += "class='replace'>012</span>3456789abcdef|"
        assert(result == dump)

    def test_width(self):
        # width=25
        args = make_parser().parse_args(['--width', '25'])
        hd = HexdumpEncoder(ansi_colored)
        hd.append(bytes("foobar", "utf8"), "insert", args.width)
        result = hd.final()

        dump = '000000: '
        dump += Ansi.insert + '66'
        dump += '\n6f 6f 62 61 72' + Ansi.reset
        dump += '                               |'
        dump += Ansi.insert + 'foobar' + Ansi.reset
        dump += '          |'
        assert(result == dump)

    def test_width_max(self):
        # width=max
        args = make_parser().parse_args([])
        args.width = get_max_width(args)
        hd = HexdumpEncoder(html_colored)
        hd.append(bytes("012", "utf8"), "replace", args.width)
        hd.append(bytes("3456789ab", "utf8"), "equal", args.width)
        hd.append(bytes("", "utf8"), "delete", args.width)
        hd.append(bytes("cdef", "utf8"), "equal", args.width)
        result = hd.final()

        dump = "000000: "
        dump += "<span class='replace'>30 31 32</span> "
        dump += "33 34 35 36 37 38 39 61 62"
        dump += "<span class='delete'> </span>"
        dump += "63 64 65 66"
        dump += " |"
        dump += "<span "
        dump += "class='replace'>012</span>3456789abcdef|"
        assert(result == dump)

if __name__ == '__main__':
    unittest.main()
