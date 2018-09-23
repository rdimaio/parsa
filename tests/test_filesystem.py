import unittest, os, sys
sys.path.append(os.path.abspath('..'))
#from parsa.utils.filesystem import *
#from parsa.utils import filesystem as fs
from parsa.utils import filesystem as fs


class FileSystemTestCase(unittest.TestCase):
    def test_compose_unique_filepath(self):
        return True

    def test_get_filelist(self):
        return True

    def test_set_outdir(self):
        outdir = fs.set_outdir('foo', 'bar')
        self.assertEqual(outdir, 'foo')

    def test_set_outdir_no_outdir_provided(self):
        outdir = fs.set_outdir(None, 'bar')
        self.assertEqual(outdir, 'bar')
    
    def test_write_str_to_file(self):
        return True