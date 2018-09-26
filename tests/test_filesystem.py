import unittest
import os
import sys
import tempfile

sys.path.append(os.path.abspath('..'))
from parsa.utils import filesystem as fs

class FilepathCompositionTestCase(unittest.TestCase):
    """Base class for tests regarding compose_unique_filepath."""

    # Test infile name
    infile = 'foo.pdf'

    def generate_conflicts(self, conflicts_count, outdir):
        """Generate conflicting filepaths for compose_unique_filepath.
        conflicts_count specifies the number of conflicting filepaths to create.
        First conflict: foo.txt
        Second conflict: foo.pdf.txt
        Third conflict onwards: foo.pdf2.txt, foo.pdf3.txt, etc.
        """
        if conflicts_count < 1:
            raise ValueError('Number of conflicts to generate must be a positive non-zero integer.')
        elif not isinstance(conflicts_count, int):
            raise TypeError('Input must be an integer.')

        conflicts = []

        conflicts.append(os.path.join(outdir, 'foo.txt'))

        if conflicts_count > 1:
            conflicts.append(os.path.join(outdir, 'foo.pdf.txt'))

        if conflicts_count > 2:
            base_conflict_no_extension = os.path.join(outdir, 'foo')
            for conflicts_counter in range(2, conflicts_count):
                conflicts.append(base_conflict_no_extension + '.pdf' + str(conflicts_counter) + '.txt')
        return(conflicts)


# ===== TESTS =====
class FilepathCompositionTest(FilepathCompositionTestCase):
    """Tests involving compose_unique_filepath.
    No setUp or tearDown functions are present,
    as for most of these tests a different setUp and tearDown
    is required for Python 2.x and Python 3.x.
    Moreover, the tests involve operating
    inside with statements, which need to be 
    inside the test functions themselves.
    """

    def test_compose_unique_filepath_no_conflicts_in_outdir(self):
        """Compose an output filepath for 'foo.pdf', with no file named 'foo.txt' in the output directory.
        Expected output: 'foo.txt'
        """
        # Get directory where temporary files are created
        outdir = tempfile.gettempdir()
        outfile = fs.compose_unique_filepath(self.infile, outdir)
        expected_outfile = os.path.join(outdir, 'foo.txt')
        self.assertEqual(outfile, expected_outfile)

    def test_compose_unique_filepath_one_conflict_in_outdir(self):
        """Compose an output filepath for 'foo.pdf', 
        when a file named 'foo.txt' is already present in the output directory.
        Expected output: 'foo.pdf.txt'
        """
        # Python 2.x
        # Differences with the Python 3.x test:
        #   tempfile.mkdtemp() is used instead of tempfile.TemporaryDirectory()
        #   shutil.rmtree is used instead of os.remove to remove the temporary directory
        if sys.version_info[0] < 3:
            import shutil
            # Work in a temporary directory
            outdir = tempfile.mkdtemp()
            # Create a temporary file named 'foo.txt'
            conflicts = self.generate_conflicts(1, outdir)
            with open(conflicts[0], 'w'):
                outfile = fs.compose_unique_filepath(self.infile, outdir)
            # Remove the temporary file
            os.remove(conflicts[0])
            # Remove the temporary directory (mdktemp must be manually deleted)
            # shutil.rmtree is used instead of os.remove to avoid OSError
            shutil.rmtree(outdir, ignore_errors=True)
        # Python 3.x
        else:
            # Work in a temporary directory
            with tempfile.TemporaryDirectory() as outdir:
                # Create a temporary file named 'foo.txt'
                conflicts = self.generate_conflicts(1, outdir)
                with open(conflicts[0], 'w'):
                    outfile = fs.compose_unique_filepath(self.infile, outdir)
                # Remove the temporary file
                os.remove(conflicts[0])
        expected_outfile = os.path.join(outdir, 'foo.pdf.txt')
        self.assertEqual(outfile, expected_outfile)

    def test_compose_unique_filepath_two_conflicts_in_outdir(self):
        """Compose an output filepath for 'foo.pdf', 
        when two files, named 'foo.txt' and 'foo.pdf.txt' respectively, are already present in the output directory.
        Expected output: 'foo.pdf2.txt'
        """
        # Python 2.x
        if sys.version_info[0] < 3:
            import shutil
            # Work in a temporary directory
            outdir = tempfile.mkdtemp()
            # Create two temporary files named 'foo.txt' and 'foo.pdf.txt'
            conflicts = self.generate_conflicts(2, outdir)
            with open(conflicts[0], 'w'), open (conflicts[1], 'w'):
                outfile = fs.compose_unique_filepath(self.infile, outdir)
            # Remove the temporary files
            for conflict in conflicts:
                os.remove(conflict)
            # Remove the temporary directory (mdktemp must be manually deleted)
            # shutil.rmtree is used instead of os.remove to avoid OSError
            shutil.rmtree(outdir, ignore_errors=True)
        # Python 3.x
        else:
            # Work in a temporary directory
            with tempfile.TemporaryDirectory() as outdir:
                # Create a temporary file named 'foo.txt'
                conflicts = self.generate_conflicts(2, outdir)
                with open(conflicts[0], 'w'), open (conflicts[1], 'w'):
                    outfile = fs.compose_unique_filepath(self.infile, outdir)
                # Remove the temporary files
                for conflict in conflicts:
                    os.remove(conflict)
        expected_outfile = os.path.join(outdir, 'foo.pdf2.txt')
        self.assertEqual(outfile, expected_outfile)

    def test_compose_unique_filepath_ten_conflicts_in_outdir(self):
        """Compose an output filepath for 'foo.pdf', 
        when ten files, named 'foo.txt', 'foo.pdf.txt'
        and 'foo.pdf2.txt' through 'foo.pdf9.txt' are present.
        Expected output: 'foo.pdf10.txt'
        """
        # Python 2.x
        if sys.version_info[0] < 3:
            import shutil
            # Work in a temporary directory
            outdir = tempfile.mkdtemp()
            # Create the temp files
            conflicts = self.generate_conflicts(10, outdir)
            # AFAIK, there is no completely safe way of opening a list of files using a with statement in Python 2.x
            with open(conflicts[0], 'w'), \
                 open (conflicts[1], 'w'), \
                 open (conflicts[2], 'w'), \
                 open (conflicts[3], 'w'), \
                 open (conflicts[4], 'w'), \
                 open (conflicts[5], 'w'), \
                 open (conflicts[6], 'w'), \
                 open (conflicts[7], 'w'), \
                 open (conflicts[8], 'w'), \
                 open (conflicts[9], 'w'):
                outfile = fs.compose_unique_filepath(self.infile, outdir)
            # Remove the temporary files
            for conflict in conflicts:
                os.remove(conflict)
            # Remove the temporary directory (mdktemp must be manually deleted)
            # shutil.rmtree is used instead of os.remove to avoid OSError
            shutil.rmtree(outdir, ignore_errors=True)
        # Python 3.x
        else:
            # Work in a temporary directory
            with tempfile.TemporaryDirectory() as outdir:
                # Create the temp files
                conflicts = self.generate_conflicts(10, outdir)
                # AFAIK, there is no completely safe way of opening a list of files using a with statement in Python 2.x
                with open(conflicts[0], 'w'), \
                     open (conflicts[1], 'w'), \
                     open (conflicts[2], 'w'), \
                     open (conflicts[3], 'w'), \
                     open (conflicts[4], 'w'), \
                     open (conflicts[5], 'w'), \
                     open (conflicts[6], 'w'), \
                     open (conflicts[7], 'w'), \
                     open (conflicts[8], 'w'), \
                     open (conflicts[9], 'w'):
                    outfile = fs.compose_unique_filepath(self.infile, outdir)
                # Remove the temporary files
                for conflict in conflicts:
                    os.remove(conflict)
        expected_outfile = os.path.join(outdir, 'foo.pdf10.txt')
        self.assertEqual(outfile, expected_outfile)
    


class FileSystemTest(unittest.TestCase):

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