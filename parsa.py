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
    text = get_text(infile)
    
    # Write to outfile if text has been extracted successfully
    if text:
        write_outfile(infile, outdir, text) 
    
# If input is a folder            
elif os.path.isdir(args.input):

    # Set IO variables
    indir = args.input
    outdir = os.path.join(set_outdir(args.output, indir), 'parsaoutput')

    # Create output folder
    os.makedirs(outdir, exist_ok=True)

    filelist = get_filelist(indir)

    for infile in filelist:
        text = get_text(infile)
        if text:
            write_outfile(infile, outdir, text)

            
else:
    exit("Error: input must be an existing file or directory")
