import argparse
import os
import textract

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

def write_outfile(infile, outdir):
    """Compose output filepath and write the extracted text to it.
    If a file with the same name as the output file already exists in the output directory, 
    the input file's extension will be included in the output file's name before the .txt extension.
    Any following cases of file already existing will result in the output file being identified by a number."""
    # Get input's filename with neither its path nor extension
    # e.g. /home/testdocs/test.pdf -> test
    filename_noextension = os.path.basename(os.path.normpath(os.path.splitext(infile)[0]))

    # Create path for output file
    # os.path.join intelligently creates filepaths that work cross-platform
    # e.g. /home/testdocs/ + test.pdf -> /home/testdocs/test
    outfilepath_noextension = os.path.join(outdir, filename_noextension)
    outfile = outfilepath_noextension + '.txt'

    # Extract text
    # utf-8 is used here to handle different languages efficiently (https://stackoverflow.com/a/2438901)
    text = textract.process(infile).decode("utf-8")

    # TODO - is it really convenient to make a function out of this? should i define outfile variables inside the function in order to pass less arguments?

    file_exists_counter = 2
    while os.path.exists(outfile):
        input_extension = os.path.splitext(infile)[1]
        if file_exists_counter == 2:
            outfile = outfilepath_noextension + input_extension + '.txt'
        else:
            outfile = outfilepath_noextension + str(file_exists_counter) + '.txt'
        file_exists_counter += 1
    
    print(outfile)   
    with open(outfile, "x") as fout:
            fout.write(text)

# Get CLI arguments
args = parse_arguments()

# If input is a file
if os.path.isfile(args.input):

    # Set IO variables
    infile = args.input
    outdir = set_outdir(args.output, os.path.dirname(infile))

    

    write_outfile(infile, outdir)

    
    
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
            infile = os.path.abspath(os.path.join(root, filename))
            print(infile)
            text = textract.process(infile).decode("utf-8")
            filename_noextension = os.path.basename(os.path.normpath(os.path.splitext(infile)[0]))
            outfilepath_noextension = os.path.join(outdir, filename_noextension)
            outfile = outfilepath_noextension + '.txt'
            try:
                with open(outfile, "x") as fout:
                    fout.write(text)
            except FileExistsError:
                outfile = outfile + '.txt'
                with open(outfile, "x") as fout:
                   fout.write(text)

else:
    exit("Error: input must be an existing file or directory")