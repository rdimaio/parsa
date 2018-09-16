import os
import time # TODO - remove when done
import utils.cli as cli
import utils.filesystem as fs
import utils.text as txt

# TODO - remove this after testing
# timing tool
# t0 = time.time()
# t1 = time.time()
#     print(t1-t0)

# Get CLI arguments
args = cli.parse_arguments()

# If input is a file
if os.path.isfile(args.input):

    # Set IO variables
    infile = args.input
    indir = os.path.dirname(infile)
    outdir = fs.set_outdir(args.output, indir)

    # Extract text
    text = txt.get_text(infile)
    
    # If text has been extracted successfully (and infile was not empty)
    if text:
        outfile = fs.compose_unique_filepath(infile, outdir)
        try:
            fs.write_str_to_file(text, outfile) 
        except OSError as e:
            print(e)
    
# If input is a folder            
elif os.path.isdir(args.input):

    # Set IO variables
    indir = args.input
    outdir = os.path.join(fs.set_outdir(args.output, indir), 'parsaoutput')

    # Create output folder
    os.makedirs(outdir, exist_ok=True)

    filelist = fs.get_filelist(indir)

    for infile in filelist:
        text = txt.get_text(infile)
        if text:
            outfile = fs.compose_unique_filepath(infile, outdir)
            try:
                fs.write_str_to_file(text, outfile) 
            except OSError as e:
                print(e)

            
else:
    exit("Error: input must be an existing file or directory")
