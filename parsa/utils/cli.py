"""utils/cli.py - Command-line utilities for parsa

Classes:
    _SmartFormatter - allows formatting in the CLI help menu

Functions:
    parse_arguments - parse CLI arguments
    _set_arguments - set CLI description and arguments
"""

import argparse

class _SmartFormatter(argparse.HelpFormatter): # pragma: no cover
    # Reason for no coverage: cannot be tested, as it's only used internally by argparse
    # (passed in as a formatter_class in _set_arguments)
    """Allows formatting in the CLI help menu.
    Called by beginning a string with R| in _set_arguments().
    https://stackoverflow.com/a/22157136
    """
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()  
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)

def parse_arguments():
    """Parse command-line arguments, and return a Namespace object containing them."""
    argparser = _set_arguments()
    # Parse arguments into Namespace
    args = argparser.parse_args()
    return args

def _set_arguments():
    """Set CLI description and arguments."""
    argparser = argparse.ArgumentParser(description=('Textract-based text parser that supports most text file extensions. '
    'Parsa can parse multiple formats at once, ' 
    'writing them to .txt files in the directory of choice.'), formatter_class=_SmartFormatter)

    argparser.add_argument('--noprompt', '-n', action='store_true', help=('ignore files without an extension and '
    'don\'t prompt the user to input their extension'))

    argparser.add_argument('input', help=('input file or folder; if a folder is passed as input, '
    'parsa will scan every file inside it recursively (scanning subfolders as well)'))

    argparser.add_argument('--output', '-o', nargs='?', default=None, help=('R|folder where the output files '
    'will be stored. The default folder is: \n'
    '(a) the input file\'s parent folder, if the input is a file, or \n'
    '(b) a folder named \'parsaoutput\' located in the input folder, if the input is a folder.'))
    return argparser