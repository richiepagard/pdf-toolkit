"""
Reader module of the PDF toolkit.
Hanldes reading the whole file content and processing the file
with validations and handling the exceptions.
"""

import logging

from pypdf import PdfReader
from pypdf.errors import PyPdfError

from src.utils import base_logger


# Config logging
logger = logging.getLogger("READER")
base_logger(logger)


class Reader:
    """
    Managing the PDF document retrieving / reading.
    Only handles the file reading, but in different formats
    and approaches of file reading content.

    Attributes:
        reader (PdfReader obj): Defining an object of PdfReader to access the methods
            and manipulating the data or content.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initializing the class and its attributes.
        Defines the important attributes.

        Arguments:
            file_path (str): The actual path of the PDF file.
        """

        self.file_path = file_path
        self.reader = PdfReader(file_path)

    def content_reader(self) -> str:
        """
        Reading the PDF file content from all pages.
        """
        read_text = ""

        try:
            logger.debug(f"PDF file {self.file_path} opened successfully.")

            for page in self.reader.pages:
                page_number = page.page_number + 1
                extracted = page.extract_text()
                read_text += f"\nPage {page_number}:\n-------\n{extracted}\n"

                logger.debug(f"Extracting text from page {page_number}")

        except PyPdfError as pypdferror:
            logger.error(pypdferror)
            # Re-raise the occured exception
            raise

        except Exception as occured_exception:
            logger.error(occured_exception)
            # Re-raise the occured exception
            raise

        logger.debug(f"PDF file {self.file_path} read successfully.")
        return read_text
