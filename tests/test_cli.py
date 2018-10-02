"""Tests for utils/cli.py.
Tests:
    parse_arguments:
        test_with_empty_args


    _set_arguments:

"""

import unittest
import os
import sys
import tempfile

sys.path.append(os.path.abspath('..'))
from parsa.utils import cli

class CLITest(unittest.TestCase):

    def test_with_empty_args(self): 
        """When sys.argvs is empty, the function should exit with SystemExit: 2"""                  
        sys.argv = ['']
        with self.assertRaises(SystemExit) as sys_e:
            cli.parse_arguments()
        self.assertEqual(sys_e.exception.code, 2)


    def test_parse_arguments(self):
        return True