import argparse
import os
import textract

# Set directory to current working directory
directory = os.getcwd()

parser = argparse.ArgumentParser(description='Text parser that supports most text file extensions. Writes the output for each file to [filename].txt.')

parser.add_argument('input', help='The input can either be a file or a folder; in the latter case, all the supported files located inside the folder will be scanned.')
# TODO - stats
parser.add_argument('--stats', '-s', nargs='?', help='Output stats file.')
parser.add_argument('--outfolder', '-o', nargs='?', default=None, help='Output folder where the output files will be stored. By default, it will be a folder named parsaoutput located in the input folder.')

args = parser.parse_args()

# if outfolder = None set outfolder = infolder


#print(args.accumulate(args.integers))