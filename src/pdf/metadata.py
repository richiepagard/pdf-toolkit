"""
Metadata module of the PDF toolkit.
Hanldes the whole metadata content and metadata manipulation,
also processing the file with validations and handling the exceptions.
"""

import logging
import pprint
from datetime import datetime
from dataclasses import dataclass

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PyPdfError

from src.utils import base_logger


# Config logging
logger = logging.getLogger("METADATA")
base_logger(logger)


@dataclass
class AddMetadataInstances:
    """
    The default instance attributes for adding metadata to a PDF document.
    Uses for modifying and adding new metadata, only preparing the instances.
    """
    author: str = "Unknown"
    producer: str = "Undefined"
    title: str = "-"
    subject: str = "-"
    creator: str = "Undefined"
    creation_date: str = "-"
    creation_time: str = "-"


class Metadata:
    """
    Managing the PDF document metadata.
    Only handles the file metadata such as retrieving and manipulating.

    Attributes:
        reader (PdfReader obj): Defining an object of PdfReader.
        writer (PdfWriter obj): Defining an object of PdfWriter.
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

    def file_metadata(self) -> dict:
        """
        Getting the file metadata and format its keys by ignoring
        the '/' before each key. Handles the PyPdfError and logs it,
        returns the final 'data' result.
        """
        data = {}

        try:
            logger.debug("PDF file %s opened successfully.", self.file_path)

            for key, value in self.reader.metadata.items():
                # Filter the keys to ignore the '/',
                # '/Title' becomes 'Title' etc
                key = str(key).strip("/")

                # Filter the creation datetime to show more human readable
                if key == "CreationDate":
                    _datetime = str(value).replace("'", "")
                    _datetime = datetime.strptime(_datetime, "D:%Y%m%d%H%M%S%z")
                    value = _datetime.strftime("%Y-%m-%d %H:%M:%S")

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
        metadata: AddMetadataInstances
    ):
        """
        Adding metadata to the file if it does not contain any metadata.
        It only checks whether the file contains metadata or not, and
        if not, it adds new metadata to it. In other words, it modify
        the file metadata by adding some to it.
        """
        final_data = {}

        _basic_metadata = {
            "/Author": metadata.author,
            "/Producer": metadata.producer,
            "/Title": metadata.title,
            "/Subject": metadata.subject,
        }
        _might_default = {
            "/CreationDate": self._creation_datetime_format(
                metadata.creation_date, metadata.creation_time
            ),
            "/Creator": self.reader.metadata.creator or metadata.creator,
            "/Producer": self.reader.metadata.producer or metadata.producer,
        }
        final_data = {**_basic_metadata, **_might_default}

        # Override the document's metadata by the 'final_data'
        self.writer.metadata = {}

        self.writer.metadata = final_data
        self.writer.write(self.file_path)
        # Recreating the Reader instance to reload the file info
        self.reader = PdfReader(self.file_path)

    def _creation_datetime_format(
        self,
        creation_date: str,
        creation_time: str
    ) -> str:
        """
        Helper function to format the PDF document's creation datetime metadata.
        If the document has a Creation Date, the formatted datetime keeps
        in the current datetime of document. But if does not contain any,
        the formatted datetime set to the sent date from the client
        which provided by the function arguments.

        Arguments:
            creation_date (str): The creation date client sent to set
                as document's metadata. It's format: "<year>-<month>-<day>".
            creation_time (str): The creation time client sent to set
                as document's metadata. It's format: "<hour>:<minute>:<second>".
        """

        # Gets document existed creation date if contain
        existing_date = self.reader.metadata.get("/CreationDate")
        if existing_date:
            return existing_date

        # Format the sent datetime provided by method arguments
        cleaned_datetime = datetime.strptime(
            f"{creation_date} {creation_time}", "%Y-%m-%d %H:%M:%S"
        )

        # Retuens the appropriate datetime format
        # for the PDF document metadata creation date
        return cleaned_datetime.strftime("D:%Y%m%d%H%M%S+00'00'")

    def __str__(self) -> str:
        """
        Format the output string of an object. Returns the retuned data
        from the 'file_metadata' method and format it with 'pprint'
        to print the data in a prettier way like JSON formating.
        """
        printer = pprint.PrettyPrinter(indent=4)
        result = printer.pformat(self.file_metadata())

        return result.replace("{", "{\n ", 1).rsplit("}", 1)[0] + "\n}"
