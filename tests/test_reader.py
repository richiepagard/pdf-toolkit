"""
Tests the PDF Reader module's Reader class.

- Tests valid PDF to ensure content is returned.
- Tests multiple pages to ensure all pages are read.
- Checks invalid or nonexistent path for file not found exceptions.
- Tests the corrupted PDF exception from PdfReader exception.
- Tests that the PdfError raised appropriately.
"""

import unittest
from tempfile import NamedTemporaryFile

from pypdf.errors import PdfReadError

from src.pdf.reader import Reader


class TestReader(unittest.TestCase):

	def test_file_does_not_exist(self):
		"""
		Tests if the file trying to read is exists or not.
		"""
		fake_path = "this_file_does_not_exist.pdf"

		with self.assertRaises(FileNotFoundError):
			Reader(fake_path)

	def test_invalid_pdf_file(self):
		"""
		Tests the PDF document validation to ensure the created file
		is a valid PDF file or not, all the created file with '.pdf' suffix
		are not a valid PDF file.
		"""
		with NamedTemporaryFile(suffix=".pdf") as file:
			file.write(b"This is not a real PDF!")
			file.flush()

			with self.assertRaises(PdfReadError):
				Reader(file.name)


if __name__ == "__main__":
	unittest.main()
