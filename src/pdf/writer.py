"""
Writer module of the PDF toolkit.
Handles writing a file by writing its metadata.
"""

import logging
from datetime import datetime

from pypdf import PdfWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch

from src.utils import base_logger


# Config logging
logger = logging.getLogger("WRITER")
base_logger(logger)

# Initialize the PdfWriter instance
WRITER = PdfWriter()

# Format the current date and time for the metadata
utc_time = "-05'00'"
time = datetime.now().strftime(f"D\072%Y%m%d%H%M%S{utc_time}")


class Writer:
	"""
	Writer class for creating and writing PDF files with metadata.

	Attributes:
		writer (PdfWriter): An instance of PdfWriter for writing PDF files.
		file_name (str): Name of the PDF file to be created.
		path (str): Path where the PDF file will be saved.
		page_width_inches_size (float): Width of the page in inches.
		page_height_inches_size (float): Height of the page in inches.
		text (str): Text to be written on the PDF page.
	"""
	def __init__(
		self,
		file_name: str = "sample",
		path: str = "examples",
		page_width_inches_size: float = 8.5,
		page_height_inches_size: float = 11.0,
		text: str = "Hello, World!"
	):
		"""
		Initializes the Writer class with the specified parameters.

		Arguments:
			file_name (str): Name of the PDF file to be created. Default is "sample".
			path (str): Path where the PDF file will be saved. Default is "examples".
			page_width_inches_size (float): Width of the page in inches. Default is 8.5 inches.
			page_height_inches_size (float): Height of the page in inches. Default is 11.0 inches.
			text (str): Text to be written on the PDF page. Default is "Hello, World!".
		"""
		self.file_name = file_name
		self.path = path
		self.page_width_inches_size = page_width_inches_size
		self.page_height_inches_size = page_height_inches_size
		self.text = text

		self.writer = PdfWriter()
		self.canvas = Canvas(
			f"{self.path}/{self.file_name}.pdf",
			pagesize=(
				self.page_width_inches_size * inch,
				self.page_height_inches_size * inch
			)
		)


writer = Writer()
