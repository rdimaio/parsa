"""Tests for utils/cli.py.
Tests:
    parse_arguments:
        empty_args
        args_output_not_passed
        with_outdir


    _set_arguments:

"""

import unittest
import os
import sys

if sys.version_info[0] < 3:
    import mock
else:
    from unittest import mock

sys.path.append(os.path.abspath('..'))
from parsa.utils import cli

class CLITest(unittest.TestCase):

    def test_parse_arguments_empty_args(self): 
        """When sys.argvs is empty, the function should exit with SystemExit: 2"""                  

        testargs = ['']
        with mock.patch.object(sys, 'argv', testargs):
            # https://stackoverflow.com/a/13491726
            with self.assertRaises(SystemExit) as sys_e:
                cli.parse_arguments()
            self.assertEqual(sys_e.exception.code, 2)

    def test_parse_arguments_no_output_arg_passed(self):
        cli_input_arg = 'foo'
        testargs = ['', cli_input_arg]
        with mock.patch.object(sys, 'argv', testargs):
            args = vars(cli.parse_arguments())
            self.assertEqual(args['input'], cli_input_arg)

    #def test_parse_arguments_args_output_passed(self):
    #    cli_input = 'foo'
    #    cli_output = 'bar'
    #    sys.argv[1] = cli_input
    #    sys.argv.append(cli_output)
    #    args = vars(cli.parse_arguments())
    #    self.assertEqual(args['input'], cli_input)
    #    self.assertEqual(args['output'], cli_output)

    def test_parse_args(self):
        testargs = ['', 'foo']
        with mock.patch.object(sys, 'argv', testargs):
            
            return True