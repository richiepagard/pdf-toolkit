import unittest
from unittest.mock import patch
from tempfile import NamedTemporaryFile

from reportlab.pdfgen.canvas import Canvas

from src.pdf.metadata import Metadata


class TestMetadata(unittest.TestCase):
    """
    Test cases for metadata module at `/src/pdf/metadata`.
    """

    def test_file_metadata(self):
        """
        Tests that the PDF file return excepted metadata format.
        """
        with NamedTemporaryFile(suffix=".pdf") as file:
            pdf = Canvas(file.name)

            # Preparing sample content
            pdf.drawString(100, 700, "Software Testing...")
            pdf.showPage()

            pdf.setTitle("Software Testing")
            pdf.setAuthor("Richie")
            pdf.setSubject("Software Testing Importance")
            pdf.save()

            metadata = Metadata(file.name).file_metadata()

            self.assertEqual(
                metadata.get("Title"),
                "Software Testing"
            )
            self.assertEqual(
                metadata.get("Author"),
                "Richie"
            )
            self.assertEqual(
                metadata.get("Subject"),
                "Software Testing Importance"
            )

    def test_metadat_cleaned_keys(self):
        """
        Tests the cleaning keys of file metadata, /Title should be Title etc.
        """
        with NamedTemporaryFile(suffix=".pdf") as file:
            pdf = Canvas(file.name)
            _cleaned_keys = ["Title", "Author", "Subject"]
            _uncleaned_keys = ["/Title", "/Author", "/Subject"]

            pdf.drawString(100, 700, "The C Programming Language book by K&R")
            pdf.showPage()

            pdf.setTitle("K & R Book")
            pdf.setAuthor("Ken Thumbpson")
            pdf.setSubject("Introducing the C programming language book by K&R, the original book.")
            pdf.save()


            metadata = Metadata(file.name).file_metadata()

            for key in _cleaned_keys:
                self.assertIn(key, metadata.keys())

            for key in _uncleaned_keys:
                self.assertNotIn(key, metadata.keys())

    @patch("src.pdf.metadata.PdfReader")
    def test_creation_date_format(self, mock_pdf_reader):
        """
        Tests if the PDF Document's CreationDate formatted as clean as excepted.
        """
        mock_pdf_reader.return_value.metadata = {
            "/CreationDate": "D:20200102123456+00'00'"
        }

        metadata = Metadata("fake.pdf")
        result = metadata.file_metadata()

        self.assertEqual(
            result["CreationDate"],
            "2020-01-02 12:34:56"
        )


if __name__ == "__main__":
    unittest.main()
