import unittest
from unittest.mock import patch
from tempfile import NamedTemporaryFile

from reportlab.pdfgen.canvas import Canvas

from src.pdf.metadata import Metadata, AddMetadataInstances


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

    def test_creation_datetime_format_method(self):
        """
        Tests the '_creation_datetime_format' helper function
        to ensure it returns the correct PDF Creation datetime format.
        """
        _correct_date_format = "2026-09-23"
        _correct_time_format = "21:27:34"
        _wrong_date_format = "2026/09/23"
        _wrong_time_format = "21,27,34"
        _pdf_date = "D:20260923212734+00'00'"

        with NamedTemporaryFile(suffix=".pdf") as file:
            pdf = Canvas(file.name)
            pdf.drawString(
                100,
                700,
                "The creation date time is a helper function to clean the date time format of PDF Document."
            )
            pdf._doc.info.creationDate = _pdf_date
            pdf.save()

            metadata = Metadata(file.name)


    def test_add_metadata_method(self):
        """
        Tests the 'add_metadata' method to ensure new metadata added
        in pdf document.
        """
        with NamedTemporaryFile(suffix=".pdf") as file:
            pdf = Canvas(file.name)
            pdf.drawString(100, 700, "Adding new metadata")
            pdf.save()

            metadata = Metadata(file.name)
            metadata.add_metadata(
                AddMetadataInstances(
                    author="Richie",
                    title="Test New Metadata",
                    subject="Ensures the new metadata set to file's metadata",
                )
            )

            self.assertEqual(metadata.reader.metadata.author, "Richie")
            self.assertEqual(
                metadata.reader.metadata.producer,
                "ReportLab PDF Library - (opensource)"
            )
            self.assertEqual(
                metadata.reader.metadata.title,
                "Test New Metadata"
            )
            self.assertEqual(
                metadata.reader.metadata.subject,
                "Ensures the new metadata set to file's metadata"
            )

if __name__ == "__main__":
    unittest.main()
