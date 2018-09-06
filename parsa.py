import argparse
import os
import textract
from helpers import *

# Get CLI arguments
args = parse_arguments()

# If input is a file
if os.path.isfile(args.input):

    # Set IO variables
    infile = args.input
    outdir = set_outdir(args.output, os.path.dirname(infile))

    # Extract text and write it to the output file
    write_outfile(infile, outdir) 
    
# If input is a folder            
elif os.path.isdir(args.input):

    # Set IO variables
    indir = args.input
    outdir = os.path.join(set_outdir(args.output, indir), 'parsaoutput')

    # Create output folder
    os.makedirs(outdir, exist_ok=True)

    # Cycle through all files in the directory recursively
    # https://stackoverflow.com/a/36898903
    for root, dirs, files in os.walk(indir, topdown=True):
        # Remove the parsaoutput folder from the list of directories to scan
        # (allowed by topdown=True in os.walk's parameters)
        # https://stackoverflow.com/a/19859907
        dirs[:] = [d for d in dirs if d != 'parsaoutput']
        for filename in files:
            infile = os.path.abspath(os.path.join(root, filename))
            write_outfile(infile, outdir)
            

else:
    exit("Error: input must be an existing file or directory")

# TODO - normalize text at the end (unicode char at the end of pdf)