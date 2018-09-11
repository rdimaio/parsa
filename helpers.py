import argparse
import os
import textract

# TODO - maybe split this file in more files (e.g. cli.py, text.py)

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

    # TODO - find preference order of textract for file analysis, and add it in the help description here
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

def set_outdir(args_outdir, indir):
    """Set output directory based on whether a custom outside directory was provided or not, and return it."""
    # If output directory wasn't provided, set it to the input directory
    if args_outdir == None:
        outdir = indir
    else:
        outdir = args_outdir
    return outdir

def get_text(infile):
    """Extract text from the input file using textract, returning an empty string if the extension is not supported."""

    # If text is not extracted, the function will just return an empty string
    text = ''    
    try:
        text = textract.process(infile)
        # utf-8 is used here to handle different languages efficiently (https://stackoverflow.com/a/2438901)
        text = text.decode('utf-8')
        # remove unnecessary space caused by the form feed (\x0c, \f) character at the end of .pdf files
        if infile.endswith('.pdf'):
            text = text.strip()
    # The only exception we need to account for is ExtensionNotSupported;
    # the CLI is handled by argparse, and file existence is checked in parsa.py
    except textract.exceptions.ExtensionNotSupported:
        print("Error while parsing file: " + infile)
        print("Extension not supported\n")
    return text

def name_outfile(infile, outdir):
    # TODO - maybe change name to compose_path or name_file (generalize)
    """Compose output filepath to avoid overwriting existing files.

    If a file with the same name as the output file already exists in the output directory, 
    the input file's extension will be included in the output file's name before the .txt extension.
    (e.g. if foo.txt already exists, foo.pdf will be extracted to foo.pdf.txt)

    An incrementing counter will be included before .txt to identify subsequent extractions with the same name.
    (if foo.pdf.txt exists as well, foo.pdf will be extracted to foo.pdf2.txt, with 2 being the incrementing counter)
    """

    # Get input's filename with neither its path nor extension
    # e.g. /home/testdocs/test.pdf -> test
    filename_noextension = os.path.basename(os.path.normpath(os.path.splitext(infile)[0]))

    # Create path for output file
    # os.path.join intelligently creates filepaths that work cross-platform
    # e.g. /home/testdocs/ + test.pdf -> /home/testdocs/test
    outfilepath_noextension = os.path.join(outdir, filename_noextension)
    outfile = outfilepath_noextension + '.txt'

    file_exists_counter = 1

    while os.path.exists(outfile):
        input_extension = os.path.splitext(infile)[1]
        if file_exists_counter == 1:
            outfile = outfilepath_noextension + input_extension + '.txt'
        else:
            #TODO - see if i can delete this whiteline the one the comment is on rn
            outfile = outfilepath_noextension + input_extension + str(file_exists_counter) + '.txt'
        file_exists_counter += 1
    return outfile

def write_outfile(outfile, text):
    """Write input text string to a file, returning either true or false based on successful writing."""
    # TODO - see if you can add error checking here, otherwise remove this function and put the with statement in the main file
    with open(outfile, "x") as fout:
            fout.write(text)

    try:
        with open(outfile, "x") as fout:
            fout.write(text)
        return True
    # Check for file existence, as we're writing to outfile using the exclusive 'x' option
    except FileExistsError:
        print("Error while writing to file: " + outfile)
        print("File already exists\n")
        return False
    # Check for any possible OS errors
    except OSError:
        print("Error while writing to file: " + outfile)
        print("OSError\n")

        return False

def get_filelist(indir):
    # TODO - check this with a lot of files, because theoretically you're going through 2 for loops for each file and that might be inefficient (O(n) still)
    """Return list of files in the input directory, including the files in all subdirectories.""" 
    filelist = []
    # Cycle through all files in the directory recursively
    # https://stackoverflow.com/a/36898903
    for root, dirs, files in os.walk(indir, topdown=True):
        # Remove the parsaoutput folder from the list of directories to scan
        # (allowed by topdown=True in os.walk's parameters)
        # https://stackoverflow.com/a/19859907
        dirs[:] = [d for d in dirs if d != 'parsaoutput']
        for filename in files:
            filepath = os.path.join(root, filename)
            filelist.append(filepath)
    return filelist