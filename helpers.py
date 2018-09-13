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

def get_text(infile):
    """Extract text from the input file using textract, returning an empty string if the extension is not supported."""
    # If text is not extracted, the function will just return an empty string
    text = ''   

    try:
        text = textract.process(infile)
    # The only exception we need to account for is ExtensionNotSupported;
    # the CLI is handled by argparse, and file existence is checked in parsa.py
    except textract.exceptions.ExtensionNotSupported:
        print("Error while parsing file: " + infile)
        print("Extension not supported\n")
    else:
        # utf-8 is used here to handle different languages efficiently (https://stackoverflow.com/a/2438901)
        text = text.decode('utf-8')
        # remove unnecessary space caused by the form feed (\x0c, \f) character at the end of .pdf files
        if infile.endswith('.pdf'):
            text = text.strip()
    return text

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

def write_str_to_file(text, outfile):
    """Write input text string to a file."""
    with open(outfile, "x") as fout:
        fout.write(text)

def get_filelist(indir):
    # TODO - check this with a lot of files, because theoretically you're going through 2 for loops for each file and that might be inefficient (O(n) still)
    """Return list of files in the input directory, including the files in all subdirectories.""" 
    filelist = []
    # Cycle through all files in the directory recursively
    # https://stackoverflow.com/a/36898903
    for root, dirs, files in os.walk(indir, topdown=True):
        # Remove the parsaoutput folder from the list of directories to scan
        # (allowed by topdown=True in os.walk's parameters)
        # https://stackoverflow.com/a/19859907
        dirs[:] = [d for d in dirs if d != 'parsaoutput']
        for filename in files:
            filepath = os.path.join(root, filename)
            filelist.append(filepath)
    return filelist