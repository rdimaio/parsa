import argparse
import os
import textract

parser = argparse.ArgumentParser(description='Text parser that supports most text file extensions. Writes the output for each file to [filename].txt.')

# TODO - improve argument descriptions
parser.add_argument('input', help='input file or folder; if a folder is passed as input, parsa will scan every file inside it recursively (scanning subfolders as well)')
parser.add_argument('--stats', '-s', nargs='?', help='output stats file')
parser.add_argument('--output', '-o', nargs='?', default=None, help='output folder where the output files will be stored. If the input is a file, the default output directory is the input file\'s directory; otherwise, it\'s a folder named \'parsaoutput\' in the input folder.')

# Parse arguments into NameSpace objects
args = parser.parse_args()

# Check if input is file or dir
if os.path.isfile(args.input):
    # If output directory wasn't provided, set it to the input directory
    if args.output == None:
        args.output = os.path.dirname(args.input)
    # Make output folder
    args.output = os.path.join(args.output, 'parsaoutput')
    print(args.output)

# if outfolder = None set outfolder = infolder


#print(args.accumulate(args.integers))