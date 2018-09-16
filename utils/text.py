import textract

# TODO - maybe reorder functions, seems like it should work either way
# https://stackoverflow.com/questions/758188/make-function-definition-in-a-python-file-order-independent

def _process_text(text, _infile_extension):
    """Process extracted text and return it as a simple string."""
    # utf-8 is used here to handle different languages efficiently (https://stackoverflow.com/a/2438901)
    text = text.decode('utf-8')
    # remove unnecessary trailing space caused by the form feed (\x0c, \f) character at the end of .pdf files
    if _infile_extension == 'pdf' or _infile_extension == '.pdf':
        text = text.strip()
    return text

def get_text(infile, _infile_extension=None):
    """Extract text from the input file using textract, returning an empty string if failing to do so.
    If the infile does not explicitly have an extension (UnicodeDecodeError), 
    the user will be prompted to input the correct extension (either with or without a dot). 
    get_text is then recursively called with _infile_extension set to the input extension.

    The caller should never set _infile_extension to anything in most cases, 
    unless they want to skip the prompt for input extension and the entirety of the input is of the same format.
    """
    # If text is not extracted, the function will just return an empty string
    text = ''   

    try:
        text = textract.process(infile, extension=_infile_extension)
    # File existence gets checked in parsa.py
    except textract.exceptions.ExtensionNotSupported:
        print("Error while parsing file: " + infile)
        print("Extension not supported\n")
    # Skip file if parsing has failed
    except textract.exceptions.ShellError as e:
        print("Error while parsing file: " + infile)
        print(e)
    # If the file has no explicit extension, prompt the user for it
    except UnicodeDecodeError:
        print("Error while parsing file: " + infile)
        print("File has no extension\n")

        # Prompt the user for the input file's extension
        # textract.process adds a dot before the input extension if it's not already present (e.g. txt -> .txt)
        _infile_extension = input("Please input the file's extension (e.g. .pdf or pdf):")
        
        # Call the function again; an exception will be raised on failure
        text = get_text(infile, _infile_extension)
    # If no exceptions happened, format text adeguately
    else:
        text = _process_text(text, _infile_extension)
    return text