import unittest
from tempfile import NamedTemporaryFile

from pypdf.errors import PdfReadError
from reportlab.pdfgen.canvas import Canvas

from src.pdf.reader import Reader


class TestReader(unittest.TestCase):
    def test_file_does_not_exist(self):
        """
        Tests if the file trying to read is exists or not.
        """
        fake_path = "this_file_does_not_exist.pdf"

        with self.assertRaises(FileNotFoundError):
            Reader(fake_path)

    def test_valid_pdf_file(self):
        """
        Ensures the valid PDF file read successfully.
        """
        with NamedTemporaryFile(suffix=".pdf") as file:
            pdf = Canvas(file.name)

            # Writing content on the first page
            pdf.drawString(
                100,
                700,
                "In my opinion, AI cannot replace the enjoy and passion come from coding and solving...",
            )
            pdf.showPage()

            # Writing content on the second page
            pdf.drawString(
                100,
                700,
                "The feeling never gets old."
            )
            pdf.showPage()
            pdf.save()

            reader = Reader(file.name)
            pages = reader.pages
            content = reader.content_reader()

            self.assertEqual(pages, 2)
            self.assertIn("Page 1:", content)
            self.assertIn("The feeling never gets old.", content)


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

    def test_file_multiple_pages(self):
        """
        Tests the read file pages ro ensure all pages are read.
        """
        with NamedTemporaryFile(suffix=".pdf") as file:
            pdf = Canvas(file.name)

            # Preparing page 1
            pdf.drawString(100, 700, "This is a test content for 'PAGE 1'.")
            pdf.showPage()

            # Preparing page 2
            pdf.drawString(100, 700, "This is the content of the 'PAGE 2'.")
            pdf.showPage()

            pdf.save()

            reader = Reader(file.name)
            pages = reader.pages
            content = reader.content_reader()

            self.assertEqual(pages, 2)

            self.assertIn("Page 1:", content)
            self.assertIn("This is a test content for 'PAGE 1'.", content)

            self.assertIn("Page 2:", content)
            self.assertIn("This is the content of the 'PAGE 2'.", content)

    def test_read_file_single_page(self):
        """
        Tests the single page reader.
        """
        with NamedTemporaryFile(suffix=".pdf") as file:
            pdf = Canvas(file.name)

            # Preparing the only page
            pdf.drawString(
                100,
                700,
                "I have just configured the YouCompleteMe for my VIM, it is really good."
            )
            pdf.showPage()
            pdf.save()

            reader = Reader(file.name)
            pages = reader.pages
            content = reader.content_reader()


            self.assertEqual(pages, 1)
            self.assertIn("Page 1:", content)

    def test_empty_pdf_file(self):
        """
        Tests the empty content of a PDF file.
        """
        with NamedTemporaryFile(suffix=".pdf") as file:
            pdf = Canvas(file.name)

            # Writes nothing in the file to check the exceptations
            pdf.drawString(100, 700, "")
            pdf.showPage()
            pdf.save()

            reader = Reader(file.name)
            pages = reader.pages
            content = reader.content_reader()

            self.assertEqual(
                content,
                f"PDF contains nothing, but {pages} pages..."
            )

if __name__ == "__main__":
    unittest.main()
