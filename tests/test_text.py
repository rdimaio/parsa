"""Tests for utils/text.py.
Tests:
    get_text:
        base tests for each format are not tested here, as they are already tested in textract's library
        (https://github.com/deanmalmgren/textract/tree/master/tests)
        
        empty_file
        extension_not_supported
        no_extension

    _process_text:
        utf8
        pdf
"""

import unittest
import os
import sys
import tempfile

if sys.version_info[0] < 3:
    import StringIO as io
    import mock
else:
    from unittest import mock
    import io

sys.path.append(os.path.abspath('..'))
from parsa.utils import text as txt

class TextTest(unittest.TestCase):
    def test_get_text_empty_file(self):
        infile = tempfile.NamedTemporaryFile(suffix='.txt')
        text = txt.get_text(infile.name)
        # Empty strings evaluate to false
        self.assertFalse(text)

    def test_get_text_extension_not_supported(self):
        infile = tempfile.NamedTemporaryFile(suffix='.abc')
        
        # Redirect stdout to a StringIO object
        out_stringIO = io.StringIO()
        sys.stdout = out_stringIO

        txt.get_text(infile.name)

        # Reset redirect
        sys.stdout = sys.__stdout__
        out_message = out_stringIO.getvalue()

        self.assertIn('Extension not supported', out_message)
    
    def test_get_text_no_extension(self):
        expected_text = 'test'
        # This file has no file extension
        infile = tempfile.NamedTemporaryFile()
        # Write 'test' to the temporary file
        with open(infile.name, 'wb') as f_in:
            encoded_text = expected_text.encode('utf-8')
            f_in.write(encoded_text)

        # Python 2.x
        if sys.version_info[0] < 3:
            builtin_input = '__builtin__.raw_input'
        # Python 3.x
        else:
            builtin_input = 'builtins.input'

        # Call get_text, mocking the input for _infile_extension as txt when the function prompts for it
        with mock.patch(builtin_input, return_value='txt'):
            extracted_text = txt.get_text(infile.name)
        self.assertEqual(extracted_text, expected_text)
    
    def test__process_text_utf8(self):
        """Test that utf-8 encoded text is successfully decoded."""
        expected_text = 'test'
        encoded_text = expected_text.encode('utf-8')
        decoded_text = txt._process_text(encoded_text, '')
        self.assertEqual(decoded_text, expected_text)
    
    def test__process_text_pdf(self):
        """Test that text extracted from a .pdf file is successfully stripped away of trailing whitespace."""
        extracted_text = 'test          '
        expected_text = 'test'
        encoded_text = extracted_text.encode('utf-8')
        # Test for both 'pdf' and '.pdf' input test cases
        decoded_text1 = txt._process_text(encoded_text, 'pdf')
        decoded_text2 = txt._process_text(encoded_text, '.pdf')
        self.assertEqual(decoded_text1, expected_text)
        self.assertEqual(decoded_text2, expected_text)