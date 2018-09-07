import argparse
import os
import textract
import time
from helpers import *

# timing tool
# t0 = time.time()
# t1 = time.time()
#     print(t1-t0)

# Get CLI arguments
args = parse_arguments()

# If input is a file
if os.path.isfile(args.input):

    # Set IO variables
    infile = args.input
    indir = os.path.dirname(infile)
    outdir = set_outdir(args.output, indir)

    # Extract text and write it to the output file
    write_outfile(infile, outdir) 
    
# If input is a folder            
elif os.path.isdir(args.input):

    # Set IO variables
    indir = args.input
    outdir = os.path.join(set_outdir(args.output, indir), 'parsaoutput')

    # Create output folder
    os.makedirs(outdir, exist_ok=True)

    filelist = get_filelist(indir)

    for infile in filelist:
        write_outfile(infile, outdir)

            
else:
    exit("Error: input must be an existing file or directory")

# TODO - normalize text at the end (unicode char at the end of pdf)
