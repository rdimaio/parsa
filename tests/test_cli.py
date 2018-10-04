"""Tests for utils/cli.py.
Tests:
    parse_arguments:
        empty_args
        no_output_arg_passed
        output_arg_passed

    _set_arguments:
        tested implicitly in the parse_arguments test
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
        """When sys.argvs is empty, the function should exit with SystemExit: 2."""                  

        testargs = ['']
        with mock.patch.object(sys, 'argv', testargs):
            # https://stackoverflow.com/a/13491726
            with self.assertRaises(SystemExit) as sys_e:
                cli.parse_arguments()
            self.assertEqual(sys_e.exception.code, 2)

    def test_parse_arguments_no_output_arg_passed(self):
        """Only the input argument is passed."""
        cli_input_arg = 'foo'
        testargs = ['', cli_input_arg]
        with mock.patch.object(sys, 'argv', testargs):
            args = vars(cli.parse_arguments())
            self.assertEqual(args['input'], cli_input_arg)

    def test_parse_arguments_output_arg_passed(self):
        """Both the input and output arguments are passed."""
        cli_input_arg = 'foo'
        cli_output_arg = 'bar'
        testargs = ['', 
                    '-o', cli_output_arg,
                    cli_input_arg]
        with mock.patch.object(sys, 'argv', testargs):
            args = vars(cli.parse_arguments())
            self.assertEqual(args['input'], cli_input_arg)
            self.assertEqual(args['output'], cli_output_arg)