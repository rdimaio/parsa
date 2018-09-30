"""Tests for utils/text.py.
Tests:
    get_text:
        base cases for each format are not tested here, as they are already tested in textract's library
        (https://github.com/deanmalmgren/textract/tree/master/tests)


    
    _process_text:
        utf8
        pdf
"""

import unittest
import os
import sys
import tempfile

sys.path.append(os.path.abspath('..'))
from parsa.utils import text as txt

class TextTestCase(unittest.TestCase):
    def test_get_text(self):
        """Test that """
        return True
    
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
        
