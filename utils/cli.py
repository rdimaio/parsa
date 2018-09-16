import argparse


class _SmartFormatter(argparse.HelpFormatter):
    """Allows formatting in the CLI help menu.
    Called by beginning a string with R| in _set_arguments().
    https://stackoverflow.com/a/22157136
    """
    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()  
        # this is the RawTextHelpFormatter._split_lines
        return argparse.HelpFormatter._split_lines(self, text, width)

def _set_arguments():
    """Set CLI description and arguments."""
    argparser = argparse.ArgumentParser(description=('Textract-based text parser that supports most text file extensions. '
    'Parsa can parse multiple formats at once, ' 
    'writing them to .txt files in the directory of choice.'), formatter_class=_SmartFormatter)

    argparser.add_argument('input', help=('input file or folder; if a folder is passed as input, '
    'parsa will scan every file inside it recursively (scanning subfolders as well)'))

    # TODO - describe what the stats file will include
    argparser.add_argument('--stats', '-s', nargs='?', help='output stats file')

    argparser.add_argument('--output', '-o', nargs='?', default=None, help=('R|folder where the output files '
    'will be stored. The default folder is: \n'
    '(a) the input file\'s parent folder, if the input is a file, or \n'
    '(b) a folder named \'parsaoutput\' located in the input folder, if the input is a folder.'))
    return argparser

def parse_arguments():
    """Parse command-line arguments, and return a Namespace object containing them."""
    argparser = _set_arguments()
    # Parse arguments into Namespace
    args = argparser.parse_args()
    return args