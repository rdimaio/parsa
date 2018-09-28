"""Tests for utils/filesystem.py.
Tests:
    compose_unique_filepath:
        no_conflicts_in_outdir
        one_conflict_in_outdir
        two_conflicts_in_outdir
        ten_conflicts_in_outdir
    
    get_filelist:
        1_file_in_folder
        2_files_in_folder
        10_files_in_folder
        1000_files_in_folder
        10_files_in_1_layer_of_subfolders
        100_files_in_1_layer_of_subfolders_10_files_each
        10000_files_in_2_layers_of_subfolders_99_files_each
        1000_files_in_10_layers_of_subfolders_10_files_each
        10000_files_in_100_layers_of_subfolders_10_files_each
    
    set_outdir:
        with_outdir_provided
        no_outdir_provided
"""

import unittest
import os
import sys
import tempfile

# Needed for Python 2.x tests to close directories
if sys.version_info[0] < 3:
    import shutil

sys.path.append(os.path.abspath('..'))
from parsa.utils import filesystem as fs


# TODO
# test_compose_unique_filepath_no_conflicts_in_outdir: maybe create a temp dir in which to create the file,
# instead of creating it in the /tmp/ folder (which might already have a file named foo.txt inside, because of other
# programs in the systems)
#
# TODO
# maybe avoid deleting files as a precaution, since folders are deleted recursively - might save some time

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

    def test_get_filelist_empty_folder(self):
        """List the files of an empty directory.
        It is necessary to make a temporary directory inside the folder obtained via tempfile.gettempdir(),
        otherwise files that are already in the temp folder (created by other programs in the system) will pollute
        the test and fill the list.
        Expected output: empty list []
        """
        # Python 2.x
        if sys.version_info[0] < 3:
            # Work in a temporary directory
            indir = tempfile.mkdtemp()
            filelist = fs.get_filelist(indir)
            # Remove the temporary directory (mdktemp must be manually deleted)
            # shutil.rmtree is used instead of os.remove to avoid OSError
            shutil.rmtree(indir, ignore_errors=True)
        # Python 3.x
        else:
            # Work in a temporary directory
            with tempfile.TemporaryDirectory() as indir:
                filelist = fs.get_filelist(indir)
        # Empty lists evaluate to false
        self.assertFalse(filelist)

    def test_get_filelist_1_file_in_folder(self):
        """List the files of a directory with only one file inside it.
        Expected output: list with one string, equal to the filepath of the temporary file created
        """
        files_created = []
        # Python 2.x
        if sys.version_info[0] < 3:
            # Work in a temporary directory
            indir = tempfile.mkdtemp()
            # delete is set to False to avoid OSError at the end of the test
            file1 = tempfile.NamedTemporaryFile(dir=indir, delete=False)
            files_created.append(file1.name)
            filelist = fs.get_filelist(indir)
            # Remove the temporary file manually as a precaution 
            os.remove(file1.name)
            # Remove the temporary directory (mdktemp must be manually deleted)
            # shutil.rmtree is used instead of os.remove to avoid OSError
            shutil.rmtree(indir, ignore_errors=True)
        # Python 3.x
        else:
            # Work in a temporary directory
            with tempfile.TemporaryDirectory() as indir:
                # delete is set to False to avoid FileNotFoundError at the end of the test
                file1 = tempfile.NamedTemporaryFile(dir=indir, delete=False)
                files_created.append(file1.name)
                filelist = fs.get_filelist(indir)
                # Remove the temporary file manually as a precaution 
                # (the with statement automatically deletes the folder)
                os.remove(file1.name)
        self.assertEqual(files_created, filelist)
    
    def test_get_filelist_2_files_in_folder(self):
        """List the files of a directory with two files inside it.
        Expected output: list with two strings, equal to the filepaths of the temporary files created
        """
        files_created = []
        # Python 2.x
        if sys.version_info[0] < 3:
            # Work in a temporary directory
            indir = tempfile.mkdtemp()
            for _ in range(2):
                # delete is set to False to avoid OSError at the end of the test
                file_handler = tempfile.NamedTemporaryFile(dir=indir, delete=False)
                files_created.append(file_handler.name)
            filelist = fs.get_filelist(indir)
            # Remove the temporary files manually as a precaution 
            for filepath in files_created:
                os.remove(filepath)
            # Remove the temporary directory (mdktemp must be manually deleted)
            # shutil.rmtree is used instead of os.remove to avoid OSError
            shutil.rmtree(indir, ignore_errors=True)
        # Python 3.x
        else:
            # Work in a temporary directory
            with tempfile.TemporaryDirectory() as indir:
                for _ in range(2):
                    # delete is set to False to avoid OSError at the end of the test
                    file_handler = tempfile.NamedTemporaryFile(dir=indir, delete=False)
                    files_created.append(file_handler.name)
                filelist = fs.get_filelist(indir)
                # Remove the temporary file manually as a precaution 
                # (the with statement automatically deletes the folder)
                for filepath in files_created:
                    os.remove(filepath)
        # Typecast both lists to sets to make an unordered comparison
        self.assertEqual(set(files_created), set(filelist))

    def test_get_filelist_10_files_in_folder(self):
        """List the files of a directory with 10 files inside it.
        Expected output: list with 10 strings, equal to the filepaths of the temporary files created
        """
        files_created = []
        # Python 2.x
        if sys.version_info[0] < 3:
            # Work in a temporary directory
            indir = tempfile.mkdtemp()
            for _ in range(10):
                # delete is set to False to avoid OSError at the end of the test
                file_handler = tempfile.NamedTemporaryFile(dir=indir, delete=False)
                files_created.append(file_handler.name)
            filelist = fs.get_filelist(indir)
            # Remove the temporary files manually as a precaution 
            for filepath in files_created:
                os.remove(filepath)
            # Remove the temporary directory (mdktemp must be manually deleted)
            # shutil.rmtree is used instead of os.remove to avoid OSError
            shutil.rmtree(indir, ignore_errors=True)
        # Python 3.x
        else:
            # Work in a temporary directory
            with tempfile.TemporaryDirectory() as indir:
                for _ in range(10):
                    # delete is set to False to avoid OSError at the end of the test
                    file_handler = tempfile.NamedTemporaryFile(dir=indir, delete=False)
                    files_created.append(file_handler.name)
                filelist = fs.get_filelist(indir)
                # Remove the temporary file manually as a precaution 
                # (the with statement automatically deletes the folder)
                for filepath in files_created:
                    os.remove(filepath)
        # Typecast both lists to sets to make an unordered comparison
        self.assertEqual(set(files_created), set(filelist))

    def test_get_filelist_1000_files_in_folder(self):
        """List the files of a directory with 1000 files inside it.
        Expected output: list with 1000 strings, equal to the filepaths of the temporary files created
        """
        files_created = []
        # Python 2.x
        if sys.version_info[0] < 3:
            # Work in a temporary directory
            indir = tempfile.mkdtemp()
            for _ in range(1000):
                # delete is set to False to avoid OSError at the end of the test
                file_handler = tempfile.NamedTemporaryFile(dir=indir, delete=False)
                files_created.append(file_handler.name)
            filelist = fs.get_filelist(indir)
            # Remove the temporary files manually as a precaution 
            for filepath in files_created:
                os.remove(filepath)
            # Remove the temporary directory (mdktemp must be manually deleted)
            # shutil.rmtree is used instead of os.remove to avoid OSError
            shutil.rmtree(indir, ignore_errors=True)
        # Python 3.x
        else:
            # Work in a temporary directory
            with tempfile.TemporaryDirectory() as indir:
                for _ in range(1000):
                    # delete is set to False to avoid OSError at the end of the test
                    file_handler = tempfile.NamedTemporaryFile(dir=indir, delete=False)
                    files_created.append(file_handler.name)
                filelist = fs.get_filelist(indir)
                # Remove the temporary file manually as a precaution 
                # (the with statement automatically deletes the folder)
                for filepath in files_created:
                    os.remove(filepath)
        # Typecast both lists to sets to make an unordered comparison
        self.assertEqual(set(files_created), set(filelist))

    def test_get_filelist_10_files_in_1_layer_of_subfolders(self):
        """List the files of a directory with 10 files inside it, spread across one layer of 10 subfolders.
        Expected output: list with 10 strings, equal to the filepaths of the temporary files created
        """
        files_created = []
        # Python 2.x
        if sys.version_info[0] < 3:
            # Work in a temporary directory
            indir = tempfile.mkdtemp()
            for _ in range(10):
                subdir = tempfile.mkdtemp(dir=indir)
                file_handler = tempfile.NamedTemporaryFile(dir=subdir, delete=False)
                files_created.append(file_handler.name)
            filelist = fs.get_filelist(indir)
            # Remove the temporary files manually as a precaution 
            for filepath in files_created:
                os.remove(filepath)
            # Remove the temporary directory (mdktemp must be manually deleted)
            # shutil.rmtree is used instead of os.remove to avoid OSError
            shutil.rmtree(indir, ignore_errors=True)
        # Python 3.x
        else:
            # Work in a temporary directory
            with tempfile.TemporaryDirectory() as indir:
                # Create ten temporary subdirectories inside the temporary directory
                for _ in range(10):
                    subdir = tempfile.mkdtemp(dir=indir)
                    file_handler = tempfile.NamedTemporaryFile(dir=subdir, delete=False)
                    files_created.append(file_handler.name)
                filelist = fs.get_filelist(indir)
                # Remove the temporary file manually as a precaution 
                # (the with statement automatically deletes a TemporaryDirectory type of folder)
                for filepath in files_created:
                    os.remove(filepath)
        # Typecast both lists to sets to make an unordered comparison
        self.assertEqual(set(files_created), set(filelist))
        
    def test_get_filelist_100_files_in_1_layer_of_subfolders_10_files_each(self):
        """List the files of a directory with 100 files inside it, spread across 1 layer of subfolders of 10 files each.
        Expected output: list with 100 strings, equal to the filepaths of the temporary files created
        """
        files_created = []
        # Python 2.x
        if sys.version_info[0] < 3:
            # Work in a temporary directory
            indir = tempfile.mkdtemp()
            # Create ten temporary subdirectories
            for _ in range(10):
                subdir = tempfile.mkdtemp(dir=indir)
                # Create ten temporary files inside each temporary subdirectory
                for _ in range(10):
                    file_handler = tempfile.NamedTemporaryFile(dir=subdir, delete=False)
                    files_created.append(file_handler.name)
            filelist = fs.get_filelist(indir)
            # Remove the temporary files manually as a precaution 
            for filepath in files_created:
                os.remove(filepath)
            # Remove the temporary directory (mdktemp must be manually deleted)
            # shutil.rmtree is used instead of os.remove to avoid OSError
            shutil.rmtree(indir, ignore_errors=True)
        # Python 3.x
        else:
            # Work in a temporary directory
            with tempfile.TemporaryDirectory() as indir:
                # Create ten temporary subdirectories inside the temporary directory
                for _ in range(10):
                    subdir = tempfile.mkdtemp(dir=indir)
                    # Create ten temporary files inside each temporary subdirectory
                    for _ in range(10):
                        file_handler = tempfile.NamedTemporaryFile(dir=subdir, delete=False)
                        files_created.append(file_handler.name)
                filelist = fs.get_filelist(indir)
                # Remove the temporary file manually as a precaution 
                # (the with statement automatically deletes a TemporaryDirectory type of folder)
                for filepath in files_created:
                    os.remove(filepath)
        # Typecast both lists to sets to make an unordered comparison
        self.assertEqual(set(files_created), set(filelist))

    def test_get_filelist_10000_files_in_2_layers_of_subfolders_99_files_each(self):
        """List the files of a directory with 10000 files inside it, spread across 2 layer of subfolders of 99 files each.
        Expected output: list with 10000 strings, equal to the filepaths of the temporary files created
        """
        files_created = []
        # Python 2.x
        if sys.version_info[0] < 3:
            # Work in a temporary directory
            indir = tempfile.mkdtemp()
            # Create ten temporary subdirectories inside the temporary directory
            for _ in range(10):
                subdir = tempfile.mkdtemp(dir=indir)
                # Create ten temporary files inside each temporary subdirectory
                for _ in range(10):
                    file_handler = tempfile.NamedTemporaryFile(dir=subdir, delete=False)
                    files_created.append(file_handler.name)
                # Create ten temporary subsubdirectories
                for _ in range(10):
                    subsubdir = tempfile.mkdtemp(dir=subdir)
                    # Create 99 temporary files inside each temporary subsubdirectory
                    for _ in range(99):
                        file_handler = tempfile.NamedTemporaryFile(dir=subsubdir, delete=False)
                        files_created.append(file_handler.name)
            filelist = fs.get_filelist(indir)
            # Remove the temporary files manually as a precaution 
            for filepath in files_created:
                os.remove(filepath)
            # Remove the temporary directory (mdktemp must be manually deleted)
            # shutil.rmtree is used instead of os.remove to avoid OSError
            shutil.rmtree(indir, ignore_errors=True)
        # Python 3.x
        else:
            # Work in a temporary directory
            with tempfile.TemporaryDirectory() as indir:
                # Create ten temporary subdirectories inside the temporary directory
                for _ in range(10):
                    subdir = tempfile.mkdtemp(dir=indir)
                    # Create ten temporary files inside each temporary subdirectory
                    for _ in range(10):
                        file_handler = tempfile.NamedTemporaryFile(dir=subdir, delete=False)
                        files_created.append(file_handler.name)
                    # Create ten temporary subsubdirectories
                    for _ in range(10):
                        subsubdir = tempfile.mkdtemp(dir=subdir)
                        # Create 99 temporary files inside each temporary subsubdirectory
                        for _ in range(99):
                            file_handler = tempfile.NamedTemporaryFile(dir=subsubdir, delete=False)
                            files_created.append(file_handler.name)
                filelist = fs.get_filelist(indir)
                # Remove the temporary file manually as a precaution 
                # (the with statement automatically deletes a TemporaryDirectory type of folder)
                for filepath in files_created:
                    os.remove(filepath)
        # Typecast both lists to sets to make an unordered comparison
        self.assertEqual(set(files_created), set(filelist))

    def test_get_filelist_10000_files_in_10_layers_of_subfolders_10_files_each(self):
        """List the files of a directory with 10000 files inside it, spread across 10 layer of subfolders of 100 files each.
        Expected output: list with 10000 strings, equal to the filepaths of the temporary files created
        """
        files_created = []
        # Python 2.x
        if sys.version_info[0] < 3:
            # Work in a temporary directory
            indir = tempfile.mkdtemp()
            # Create 10 base subdirectories
            for _ in range(10):
                subdirs = []
                subdir_handler = tempfile.mkdtemp(dir=indir)
                subdirs.append(subdir_handler)
                # Create 100 temporary files inside each base subdirectory
                for _ in range(100):
                    file_handler = tempfile.NamedTemporaryFile(dir=subdir_handler, delete=False)
                    files_created.append(file_handler.name)
                # In each base subdirectory, create 9 layers of subdirectories (10 layers total)
                for i in range(9):
                    # The first subdir is created inside the base subdirectory;
                    # each subsequent subdir is created inside the previous one.
                    # The variable i is equal to the current layer - 1
                    subdir_handler = tempfile.mkdtemp(dir=subdirs[i])
                    subdirs.append(subdir_handler)
                    # Create 100 temporary files inside each layer
                    for _ in range(100):
                        file_handler = tempfile.NamedTemporaryFile(dir=subdir_handler, delete=False)
                        files_created.append(file_handler.name)

            filelist = fs.get_filelist(indir)
            # Remove the temporary files manually as a precaution 
            for filepath in files_created:
                os.remove(filepath)
            # Remove the temporary directory (mdktemp must be manually deleted)
            # shutil.rmtree is used instead of os.remove to avoid OSError
            shutil.rmtree(indir, ignore_errors=True)
        # Python 3.x
        else:
            # Work in a temporary directory
            with tempfile.TemporaryDirectory() as indir:

                # Create 10 base subdirectories
                for _ in range(10):
                    subdirs = []
                    subdir_handler = tempfile.mkdtemp(dir=indir)
                    subdirs.append(subdir_handler)

                    # Create 100 temporary files inside each base subdirectory
                    for _ in range(100):
                        file_handler = tempfile.NamedTemporaryFile(dir=subdir_handler, delete=False)
                        files_created.append(file_handler.name)

                    # In each base subdirectory, create 9 layers of subdirectories (10 layers total)
                    for i in range(9):
                        # The first subdir is created inside the base subdirectory;
                        # each subsequent subdir is created inside the previous one.
                        # The variable i is equal to the current layer - 1
                        subdir_handler = tempfile.mkdtemp(dir=subdirs[i])
                        subdirs.append(subdir_handler)

                        # Create 100 temporary files inside each layer
                        for _ in range(100):
                            file_handler = tempfile.NamedTemporaryFile(dir=subdir_handler, delete=False)
                            files_created.append(file_handler.name)

                filelist = fs.get_filelist(indir)
                # Remove the temporary file manually as a precaution 
                # (the with statement automatically deletes a TemporaryDirectory type of folder)
                for filepath in files_created:
                    os.remove(filepath)
        # Typecast both lists to sets to make an unordered comparison
        self.assertEqual(set(files_created), set(filelist))

    def test_get_filelist_10000_files_in_100_layers_of_subfolders_10_files_each(self):
        """List the files of a directory with 10000 files inside it, spread across 100 layer of subfolders of 10 files each.
        Expected output: list with 10000 strings, equal to the filepaths of the temporary files created
        """
        files_created = []
        # Python 2.x
        if sys.version_info[0] < 3:
            # Work in a temporary directory
            indir = tempfile.mkdtemp()
            # Create 10 base subdirectories
            for _ in range(10):
                subdirs = []
                subdir_handler = tempfile.mkdtemp(dir=indir)
                subdirs.append(subdir_handler)
                # Create ten temporary files inside each base subdirectory
                for _ in range(10):
                    file_handler = tempfile.NamedTemporaryFile(dir=subdir_handler, delete=False)
                    files_created.append(file_handler.name)
                # In each base subdirectory, create 99 layers of subdirectories (10 layers total)
                for i in range(99):
                    # The first subdir is created inside the base subdirectory;
                    # each subsequent subdir is created inside the previous one.
                    # The variable i is equal to the current layer - 1
                    subdir_handler = tempfile.mkdtemp(dir=subdirs[i])
                    subdirs.append(subdir_handler)
                    # Create ten temporary files inside each layer
                    for _ in range(10):
                        file_handler = tempfile.NamedTemporaryFile(dir=subdir_handler, delete=False)
                        files_created.append(file_handler.name)

            filelist = fs.get_filelist(indir)
            # Remove the temporary files manually as a precaution 
            for filepath in files_created:
                os.remove(filepath)
            # Remove the temporary directory (mdktemp must be manually deleted)
            # shutil.rmtree is used instead of os.remove to avoid OSError
            shutil.rmtree(indir, ignore_errors=True)
        # Python 3.x
        else:
            # Work in a temporary directory
            with tempfile.TemporaryDirectory() as indir:

                # Create 10 base subdirectories
                for _ in range(10):
                    subdirs = []
                    subdir_handler = tempfile.mkdtemp(dir=indir)
                    subdirs.append(subdir_handler)

                    # Create ten temporary files inside each base subdirectory
                    for _ in range(10):
                        file_handler = tempfile.NamedTemporaryFile(dir=subdir_handler, delete=False)
                        files_created.append(file_handler.name)

                    # In each base subdirectory, create 99 layers of subdirectories (10 layers total)
                    for i in range(99):
                        # The first subdir is created inside the base subdirectory;
                        # each subsequent subdir is created inside the previous one.
                        # The variable i is equal to the current layer - 1
                        subdir_handler = tempfile.mkdtemp(dir=subdirs[i])
                        subdirs.append(subdir_handler)

                        # Create ten temporary files inside each layer
                        for _ in range(10):
                            file_handler = tempfile.NamedTemporaryFile(dir=subdir_handler, delete=False)
                            files_created.append(file_handler.name)

                filelist = fs.get_filelist(indir)
                # Remove the temporary file manually as a precaution 
                # (the with statement automatically deletes a TemporaryDirectory type of folder)
                for filepath in files_created:
                    os.remove(filepath)
        # Typecast both lists to sets to make an unordered comparison
        self.assertEqual(set(files_created), set(filelist))

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