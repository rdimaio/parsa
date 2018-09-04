import argparse
import os
import textract

# TODO - see if you can put file writing in a function
# TODO - document functions

def set_outdir(args_outdir, indir):
    """Set output directory based on whether a custom outside directory was provided or not, and return it."""
    # If output directory wasn't provided, set it to the input directory
    if args_outdir == None:
        outdir = indir
    else:
        outdir = args_outdir
    return outdir

def parse_arguments():
    """Parse command-line arguments, and return a Namespace object containing them."""
    # TODO - improve argument descriptions, break strings into shorter codelines
    argparser = argparse.ArgumentParser(description='Textract-based text parser that supports most text file extensions. Writes the output for each file to [filename].txt.')
    argparser.add_argument('input', help='input file or folder; if a folder is passed as input, parsa will scan every file inside it recursively (scanning subfolders as well)')
    argparser.add_argument('--stats', '-s', nargs='?', help='output stats file')
    argparser.add_argument('--output', '-o', nargs='?', default=None, help='output folder where the output files will be stored. If the input is a file, the default output directory is the input file\'s directory; otherwise, it\'s a folder named \'parsaoutput\' in the input folder.')
    # Parse arguments into Namespace
    args = argparser.parse_args()
    return args

# Get CLI arguments
args = parse_arguments()

# If input is a file
if os.path.isfile(args.input):

    # Set IO variables
    infile = args.input
    outdir = set_outdir(args.output, os.path.dirname(infile))

    # Get input's filename with neither its path nor extension
    filename_noextension = os.path.basename(os.path.normpath(os.path.splitext(infile)[0]))

    # Create path for output file
    # os.path.join intelligently creates filepaths that work cross-platform
    outfile = os.path.join(outdir, filename_noextension) + '.txt'

    # Extract text
    # utf-8 is used here as it's able to handle all languages efficiently (https://stackoverflow.com/a/2438901)
    text = textract.process(infile).decode("utf-8")

    # TODO - maybe make a recursive function out of this to improve it;
    # TODO - maybe just needs a while loop
    # If file doesn't exist, write to it; if it exists already, add original file extension previously (e.g. test.pdf.txt)
    try:
        with open(outfile, "x") as fout:
            fout.write(text)
    except FileExistsError:
        outfile = outfile + '.txt'
        with open(outfile, "x") as fout:
            fout.write(text)
# If input is a folder            
elif os.path.isdir(args.input):

    indir = args.input
    outdir = set_outdir(args.output, indir)
    # Create output folder
    # TODO - check that you change what needs to be changed to outdir
    outdir = os.path.join(outdir, 'parsaoutput')
    os.makedirs(outdir, exist_ok=True)

    # Cycle through all files in the directory recursively
    # https://stackoverflow.com/a/36898903
    for root, dirs, files in os.walk(indir):
        for filename in files:
            # TODO - loop works, but textract needs the entire filepath to access the file, so need to pass that
            print(filename)
            text = str(textract.process(filename))
            # TODO - Must change this; currently splitext does this: /home/postrick/Documents/Programming/testdocs/test.txt; i want to strip the extension and remove the directory, then join it to parsaoutput and add .txt
            # Get input filename without extension
            infile = os.path.basename(os.path.normpath(os.path.splitext(args.input)[0]))
            # Make output filename by joining the filename with the output path and suffix .txt to it
            outfile = os.path.join(outdir, infile) + '.txt'
            try:
                with open(outfile, "x") as fout:
                    fout.write(text)
            except FileExistsError:
                outfile = outfile + '.txt'
                with open(outfile, "x") as fout:
                   fout.write(text)

else:
    exit("Error: input must be an existing file or directory")