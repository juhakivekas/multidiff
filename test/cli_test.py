from multidiff.Render import *
from multidiff import Ansi

import unittest
from pathlib import Path
import subprocess


class MainCLITests(unittest.TestCase):

    def call_run(self, expected_stdout, args):
        got_stdout = '(no stdout)'
        cmd = ['multidiff'] + args
        try:
            got_stdout = subprocess.check_output(cmd, universal_newlines=True)
        except subprocess.CalledProcessError as err:
            print('Got stderr: `{err_message}`'.format(err_message=err))
        finally:
            print('Got stdout: `{stdout}`'.format(stdout=got_stdout))

        self.assertEqual(expected_stdout, got_stdout)

    def test_diff_cli_no_args(self):
        expected_output = ''
        self.call_run(expected_output, [])

    def test_diff_cli_simple(self):
        p = Path(".")
        res = list(p.glob("**/bin_file*"))
        res = [str(x) for x in res]

        dump = Ansi.bold + res[1] + Ansi.reset
        dump += "\n000000: "
        dump += "30 31 32 33 34 35 36 37 38 39 61 62 63 64 65 66"
        dump += Ansi.delete + " " + Ansi.reset
        dump += "|0123456789abcdef|\n"

        expected_output = dump
        self.call_run(expected_output, res)

    def test_diff_cli_with_width_flag(self):
        p = Path('.')
        res = res = list(p.glob('**/bin_file*'))
        res = [str(x) for x in res]
        res += ['--width', '25']

        dump = Ansi.bold + res[1] + Ansi.reset
        dump += "\n000000: "
        dump += "30 31 32 33 34 35 36 37"
        dump += "\n38 39 61 62 63 64 65"
        dump += "\n66"
        dump += Ansi.delete + " " + Ansi.reset
        dump += "|0123456789abcdef|\n"

        expected_output = dump
        self.call_run(expected_output, res)

    def test_diff_cli_with_bytes_flag(self):
        p = Path('.')
        res = res = list(p.glob('**/bin_file*'))
        res = [str(x) for x in res]
        res += ['--bytes', '6']

        dump = Ansi.bold + res[1] + Ansi.reset
        dump += "\n000000: "
        dump += "30 31 32 33 34 35"
        dump += ' |012345|'
        dump += "\n000006: "
        dump += "36 37 38 39 61 62"
        dump += ' |6789ab|'
        dump += "\n00000c: "
        dump += "63 64 65 66"
        dump += Ansi.delete + " " + Ansi.reset
        dump += '  |cdef|'
        dump += '\n\n'
        print(dump)

        expected_output = dump
        self.call_run(expected_output, res)

if __name__ == '__main__':
    unittest.main()
