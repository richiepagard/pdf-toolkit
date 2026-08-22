"""
Metadata module of the PDF toolkit.
Hanldes the whole metadata content and metadata manipulation,
also processing the file with validations and handling the exceptions.
"""

import logging
import pprint
from datetime import date

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PyPdfError

from src.utils import base_logger


# Config logging
logger = logging.getLogger("METADATA")
base_logger(logger)


class Metadata:
    """
    Managing the PDF document metadata.
    Only handles the file metadata such as retrieving and manipulating.

    Attributes:
        reader (PdfReader obj): Defining an object of PdfReader to first read the file.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initializing the class and its attributes.
        Defines the important attributes.

        Arguments:
            file_path (str): The actual path of the PDF file will manage its metadata.
        """

        self.file_path = file_path
        self.reader = PdfReader(file_path)
        self.writer = PdfWriter()

    def file_metadata(self):
        """
        Getting the file metadata and format its keys by ignoring
        the '/' before each key. Handles the PyPdfError and logs it,
        returns the final 'data' result.
        """
        data = {}

        try:
            logger.debug(f"PDF file {self.file_path} opened successfully.")

            for key, value in self.reader.metadata.items():
                # Filter the keys to ignore the '/' (e.g. '/Title' becomes 'Title')
                key = str(key).strip('/')
                data[key] = value

        except PyPdfError as pypdferror:
            logger.error(pypdferror)
            # Re-raise the occured exception
            raise

        except Exception as occured_exception:
            logger.error(occured_exception)
            # Re-raise the occured exception
            raise

        return data

    def add_metadata(
        self,
        author: str = None,
        producer: str = None,
        title: str = None,
        subject: str = None,
        creator: str = None
    ):
        """
        Adding metadata to the file if it does not contain any metadata.
        It only checks whether the file contains metadata or not, and
        if not, it adds new metadata to it. In other words, it modify
        the file metadata by adding some to it.
        """
        final_data = {}

        _basic_metadata = {
            "/Author": author,
            "/Producer": producer,
            "/Title": title,
            "/Subject": subject,
        }
        _might_default = {
            "/Creator": self.reader.metadata.creator or creator,
            "/Producer": self.reader.metadata.producer or producer
        }
        final_data = {**_basic_metadata, **_might_default}

        # Override the document's metadata by the 'final_data'
        self.writer.metadata = {}
        logger.debug(self.writer.metadata)

        self.writer.metadata = final_data
        self.writer.write(self.file_path)

    def _creation_date_format(self, creation_date: str) -> str:
        """
        Helper function to format the creation date metadata
        of the PDF document.
        If the document has a Creation Date, the formatted date keeps
        in the current date of document. But if does not contain any,
        the formatted date set to the sent date from the client which provided
        by the function arguments.

        Arguments:
            creation_date (str): The creation date client sent to set as document's metadata.
                                It's format: "<year>-<month>-<day>".
        """
        creation_date = str(creation_date)
        _formatted_date = None

        if self.reader.metadata.creation_date:
            _formatted_date = self.reader.metadata.creation_date
        else:
            _formatted_date = date.fromisoformat(creation_date)

        return _formatted_date

    def __str__(self) -> str:
        """
        Format the output string of an object. Returns the retuned data
        from the 'file_metadata' method and format it with 'pprint'
        to print the data in a prettier way like JSON formating.
        """
        printer = pprint.PrettyPrinter(indent=4)
        result = printer.pformat(self.file_metadata())

        return result.replace("{", "{\n ", 1).rsplit("}", 1)[0] + "\n}"


meta = Metadata("examples/forfun.pdf")
meta.add_metadata(
    author="Dennis",
    title="Just For Fun",
    subject="Just For Fun...",
)

print(str(meta))
