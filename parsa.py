import argparse
import os
import textract


argparser = argparse.ArgumentParser(description='Textract-based text parser that supports most text file extensions. Writes the output for each file to [filename].txt.')

# TODO - improve argument descriptions, break strings into shorter codelines
argparser.add_argument('input', help='input file or folder; if a folder is passed as input, parsa will scan every file inside it recursively (scanning subfolders as well)')
argparser.add_argument('--stats', '-s', nargs='?', help='output stats file')
argparser.add_argument('--output', '-o', nargs='?', default=None, help='output folder where the output files will be stored. If the input is a file, the default output directory is the input file\'s directory; otherwise, it\'s a folder named \'parsaoutput\' in the input folder.')

# Parse arguments into NameSpace objects
args = argparser.parse_args()


# If input is a file
if os.path.isfile(args.input):

    infile = args.input

    # If output directory wasn't provided, set it to the input directory
    # TODO - maybe make  set_outdir(args.output) folder
    if args.output == None:
        outdir = os.path.dirname(infile)
    else:
        outdir = args.output

    filename_noextension = os.path.basename(os.path.normpath(os.path.splitext(args.input)[0]))

    # os.path.join creates paths that work in multiple OSes
    outfile = os.path.join(outdir, filename_noextension) + '.txt'
 
    # Extract text
    # TODO - maybe need to decode instead of typecast to str
    text = str(textract.process(infile))

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
    # If output directory wasn't provided, set it to the input directory
    if args.output == None:
        args.output = args.input

    # Create output folder
    args.output = os.path.join(args.output, 'parsaoutput')
    os.makedirs(args.output, exist_ok=True)
    
    # Cycle through all files in the directory recursively
    # https://stackoverflow.com/a/36898903
    for root, dirs, files in os.walk(args.input):
        for filename in files:
            text = str(textract.process(filename))
            # TODO - Must change this; currently splitext does this: /home/postrick/Documents/Programming/testdocs/test.txt; i want to strip the extension and remove the directory, then join it to parsaoutput and add .txt
            # Get input filename without extension
            infile = os.path.basename(os.path.normpath(os.path.splitext(args.input)[0]))
            # Make output filename by joining the filename with the output path and suffix .txt to it
            outfile = os.path.join(args.output, infile) + '.txt'
            try:
                with open(outfile, "x") as fout:
                    fout.write(text)
            except FileExistsError:
                outfile = outfile + '.txt'
                with open(outfile, "x") as fout:
                   fout.write(text)

            print(filename)
else:
    exit("Error: input must be an existing file or directory")