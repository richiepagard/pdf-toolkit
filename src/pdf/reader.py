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
logger = logging.getLogger(__name__)
base_logger(logger)


def reader(pdf_path: str) -> str:
    """
    Reading the PDF file content from all pages.

    Arguments:
        pdf_path (str): Path to the PDF file.
    """
    read_text = ""

    try:
        reader = PdfReader(pdf_path)

        for page in reader.pages:
            read_text += page.extract_text()

    except PyPdfError as pypdferror:
        logger.error(pypdferror)
        # Re-raise the occured exception
        raise

    except Exception as occured_exception:
        logger.error(occured_exception)
        # Re-raise the occured exception
        raise

    return read_text
