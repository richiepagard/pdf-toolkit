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
        logger.debug(f"PDF file {pdf_path} opened successfully.")

        for page in reader.pages:
            logger.debug(f"Extracting text from page {page.page_number + 1}")
            read_text += f"\nPage {page.page_number + 1}:\n-------\n{page.extract_text()}\n"

    except PyPdfError as pypdferror:
        logger.error(pypdferror)
        # Re-raise the occured exception
        raise

    except Exception as occured_exception:
        logger.error(occured_exception)
        # Re-raise the occured exception
        raise

    logger.debug(f"PDF file {pdf_path} read successfully.")
    return read_text


print(reader("examples/college_management_system.pdf"))
