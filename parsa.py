import argparse
import os
import textract
import time
from cli import *
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
        outfile = compose_unique_filepath(infile, outdir)
        try:
            write_str_to_file(text, outfile) 
        except OSError as e:
            print(e)
    
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
            outfile = compose_unique_filepath(infile, outdir)
            try:
                write_str_to_file(text, outfile) 
            except OSError as e:
                print(e)

            
else:
    exit("Error: input must be an existing file or directory")
