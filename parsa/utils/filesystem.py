"""utils/filesystem.py - OS/filesystem utilities for parsa

Functions:
    compose_unique_filepath - compose a filepath to avoid overwriting existing files
    get_filelist - return list of files of a directory and all subdirectories
    set_outdir - set output directory based on the user's choice
    write_str_to_file - write string to file
"""

import os

def compose_unique_filepath(infile, outdir):
    """Compose output filepath to avoid overwriting existing files.

    If a file with the same name as the output file already exists in the output directory, 
    the input file's extension will be included in the output file's name before the .txt extension.
    (e.g. if foo.txt already exists, foo.pdf will be extracted to foo.pdf.txt)

    An incrementing counter will be included before .txt to identify subsequent extractions with the same name.
    (if foo.pdf.txt exists as well, foo.pdf will be extracted to foo.pdf2.txt, with 2 being the incrementing counter)
    """

    # Get input's filename with neither its path nor extension
    # e.g. /home/testdocs/test.pdf -> test
    filename_noextension = os.path.basename(os.path.normpath(os.path.splitext(infile)[0]))
    # Create path for output file
    # os.path.join intelligently creates filepaths that work cross-platform
    # e.g. /home/testdocs/ + test.pdf -> /home/testdocs/test
    outfilepath_noextension = os.path.join(outdir, filename_noextension)
    outfile = outfilepath_noextension + '.txt'

    file_exists_counter = 1

    # This loop is only entered if the outfile already exists
    while os.path.exists(outfile):
        input_extension = os.path.splitext(infile)[1]
        # If it's the first iteration, just add the input extension to the filename
        if file_exists_counter == 1:
            outfile = outfilepath_noextension + input_extension + '.txt'
        # Otherwise, add a counter too
        else:
            outfile = outfilepath_noextension + input_extension + str(file_exists_counter) + '.txt'
        file_exists_counter += 1
    return outfile

def get_filelist(indir):
    """Return list of files in the input directory, including the files in all subdirectories.""" 
    filelist = []
    # Cycle through all files in the directory recursively
    # https://stackoverflow.com/a/36898903
    for root, dirs, files in os.walk(indir, topdown=True):
        # Remove the parsaoutput folder from the list of directories to scan
        # (allowed by topdown=True in os.walk's parameters)
        # https://stackoverflow.com/a/19859907
        # TODO - shouldn't be a problem if custom output folder isn't parsaoutput, but still check if it's problematic
        dirs[:] = [d for d in dirs if d != 'parsaoutput']
        for filename in files:
            filepath = os.path.join(root, filename)
            filelist.append(filepath)
    return filelist

def set_outdir(args_outdir, indir):
    """Set output directory based on whether a custom outside directory was provided or not, and return it."""
    # If output directory wasn't provided, set it to the input directory
    if args_outdir == None:
        outdir = indir
    else:
        outdir = args_outdir
    return outdir

def write_str_to_file(text, outfile):
    """Write input text string to a file."""
    with open(outfile, "w") as fout:
        fout.write(text)