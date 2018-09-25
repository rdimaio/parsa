import unittest
import os
import sys
import tempfile

sys.path.append(os.path.abspath('..'))
from parsa.utils import filesystem as fs


class FileSystemTest(unittest.TestCase):
    def test_compose_unique_filepath_with_unique_input(self):
        """Compose a filepath for test.pdf, with no file named 'test.txt' in the output directory"""

        #outfile = fs.compose_unique_filepath()
        #self.assertEqual(outfile, 'outfile.')
        return True

    def test_compose_unique_filepath(self):
        # create temp files for different cases.
        # first case, file is not already present -> outfile.txt
        # second case, file is present -> outfile.pdf.txt
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
        '''If no args_outdir is provided, then the outdir will be set to the indir.'''
        args_outdir = None
        indir = 'bar'
        outdir = fs.set_outdir(args_outdir, indir)
        self.assertEqual(outdir, indir)
    
    def test_write_str_to_file(self):
        return True