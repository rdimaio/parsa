import unittest
import os
import sys
import tempfile

sys.path.append(os.path.abspath('..'))
from parsa.utils import filesystem as fs


class FileSystemTestCase(unittest.TestCase):
    def test_compose_unique_filepath(self):
        return True

    def test_get_filelist(self):
        return True

    def test_set_outdir_with_outdir_provided(self):
        outdir = fs.set_outdir('args_outdir', 'indir')
        self.assertEqual(outdir, 'args_outdir')

    def test_set_outdir_no_outdir_provided(self):
        '''If no args_outdir is provided, then the outdir will be set to the indir.'''
        outdir = fs.set_outdir(None, 'indir')
        self.assertEqual(outdir, 'indir')
    
    def test_write_str_to_file(self):
        return True