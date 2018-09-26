import unittest
import os
import sys
import tempfile

if sys.version_info[0] < 3:
    from backports import tempfile

sys.path.append(os.path.abspath('..'))
from parsa.utils import filesystem as fs


class FileSystemTest(unittest.TestCase):
    def test_compose_unique_filepath_with_no_outfile_in_outdir(self):
        """Compose an output filepath for 'foo.pdf', with no file named 'foo.txt' in the output directory.
        Expected output: 'foo.txt'
        """
        infile = 'foo.pdf'
        # Get directory where temporary files are created
        outdir = tempfile.gettempdir()
        outfile = fs.compose_unique_filepath(infile, outdir)
        expected_outfile = os.path.join(outdir, 'foo.txt')
        self.assertEqual(outfile, expected_outfile)

    # TODO - maybe create a class and setUp just for these where I'm making a folder with temp files inside
    # teardown too, so that the files don't persist between tests
    def test_compose_unique_filepath_with_existing_outfile_in_outdir(self):
        """Compose an output filepath for 'foo.pdf', with a file named 'foo.txt' in the output directory.
        Expected output: 'foo.pdf.txt'
        """
        infile = 'foo.pdf'
        # Work in a temporary directory
        with tempfile.TemporaryDirectory() as outdir:
            # Create a temporary file named 'foo.txt'
            existing_outfile = os.path.join(outdir, 'foo.txt')
            with open(existing_outfile, 'w'):
                outfile = fs.compose_unique_filepath(infile, outdir)
            # Remove the temporary file
            os.remove(existing_outfile)
            expected_outfile = os.path.join(outdir, 'foo.pdf.txt')
        self.assertEqual(outfile, expected_outfile)

    def test_compose_unique_filepath(self):
        # create temp files for different cases.
        # third case, file is present, outfile.pdf.txt is present -> outfile.pdf2.txt
        return True

    def test_get_filelist(self):
        return True

    def test_set_outdir_with_outdir_provided(self):
        args_outdir = 'foo'
        indir = 'bar'
        outdir = fs.set_outdir(args_outdir, indir)
        self.assertEqual(outdir, args_outdir)

    def test_set_outdir_no_outdir_provided(self):
        '''If no args_outdir is provided, then outdir will be set to the indir.'''
        args_outdir = None
        indir = 'bar'
        outdir = fs.set_outdir(args_outdir, indir)
        self.assertEqual(outdir, indir)
    
    def test_write_str_to_file(self):
        return True