"""
Writer module of the PDF toolkit.
Handles writing a file by writing its metadata.
"""

import logging

from pypdf import PdfWriter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch

from src.utils import base_logger



# Config logging
logger = logging.getLogger("WRITER")
base_logger(logger)


class Writer:
	"""
	Writer class for creating and writing PDF files with metadata.

	Attributes:
		writer (PdfWriter): An instance of PdfWriter for writing PDF files.
		file_name (str): Name of the PDF file to be created.
		path (str): Path where the PDF file will be saved.
		page_width_inches_size (float): Width of the page in inches.
		page_height_inches_size (float): Height of the page in inches.
		title (str): Title of the PDF document.
		subtitle (str): Subtitle of the PDF document.
		text (str): Text to be written on the PDF page.
	"""
	def __init__(
		self,
		file_name: str = "sample",
		path: str = "examples",
		page_width_inches_size: float = 11,
		page_height_inches_size: float = 17,
		title: str = "Sample PDF",
		subtitle: str = "This is a sample PDF file created using the PDF toolkit.",
		text: list = [
			"This is a sample PDF file created using the PDF toolkit.",
		]
	):
		"""
		Initializes the Writer class with the specified parameters.

		Arguments:
			file_name (str): Name of the PDF file to be created. Default is "sample".
			path (str): Path where the PDF file will be saved. Default is "examples".
			page_width_inches_size (float): Width of the page in inches. Default is 8.5 inches.
			page_height_inches_size (float): Height of the page in inches. Default is 11.0 inches.
			text (list): List of strings to be written on the PDF page.
		"""
		self.file_name = file_name
		self.path = path
		self.page_width_inches_size = page_width_inches_size
		self.page_height_inches_size = page_height_inches_size
		self.title = title
		self.subtitle = subtitle
		self.text = text

		self.writer = PdfWriter()
		self.canvas = Canvas(
			f"{self.path}/{self.file_name}.pdf",
			pagesize=(
				self.page_width_inches_size * inch,
				self.page_height_inches_size * inch
			)
		)

	def content_writer(self):
		"""
		Creates a PDF file with the defined title, subtitle, and text content.
		The PDF file is saved at the specified path.
		Using various fonts and drawing methods to format the content on the PDF page.
		"""
		logger.debug(f"PDF file {self.file_name}.pdf created successfully at {self.path}.")

		# Set the font and the document title
		self.canvas.setFont("Helvetica-Bold", 36)
		self.canvas.drawCentredString(
			self.page_width_inches_size * inch / 2,
			self.page_height_inches_size * inch - 100,
			self.title
		)

		# Set the font and write the subtitle below the title
		self.canvas.setFont("Times-Bold", 24)
		self.canvas.drawCentredString(
			self.page_width_inches_size * inch / 2,
			(self.page_height_inches_size * inch) - 150,
			self.subtitle
		)

		# Draw a line below the subtitle
		self.canvas.line(
			(self.page_width_inches_size * inch / 2) - 350,
			(self.page_height_inches_size * inch) - 180,
			(self.page_width_inches_size * inch / 2) + 350,
			(self.page_height_inches_size * inch) - 180
		)

		# Set the font and write the main text below the line
		self.canvas.setFont("Times-Roman", 18)
		_text = self.canvas.beginText(
			direction=1,
			x=(self.page_width_inches_size * inch / 2) - 350,
			y=(self.page_height_inches_size * inch) - 220
		)

		# Write the text content line by line
		for line in self.text:
			_text.textLine(line)

		self.canvas.drawText(_text)

		# Save the PDF file
		self.canvas.save()

	def metadata_writer(
		self,
		title: str = "Undefined",
		author: str = "Unknown",
		subject: str = "Undefined",
		creator: str = "PDF Toolkit",
		producer: str = "PDF Toolkit",
	) -> dict:
		"""
		Metadata writer to modify and write new metadata
		for the created PDF document.

		Arguments:
			title (str): The PDF main title.
			author (str): The PDF owner and the actual author.
			subject (str): Represents to the PDF subject.
			creator (str): The application that originally created the PDF file such as Word or LibreOfficeWriter.
			producer (str): The software/library that actually generated or exported the PDF file.
		"""

		# Build absolute path to the PDF file in a platform-independent way
		file_path = f"{self.path}/{self.file_name}.pdf"

		# Add new metadata to the new created PDF document
		self.writer.add_metadata(
			{
				"/Title": title,
				"/Author": author,
				"/Subject": subject,
				"/Creator": creator,
				"/Producer": producer
			}
		)

		# Commit the changes to the target PDF file
		self.writer.write(str(file_path))


writer = Writer(
	text=[
		"A clean, modular toolkit for reading, writing, inspecting",
		"and manipulating PDF documents with Python and pypdf.",
		"The toolkit provides a simple and intuitive interface for working with PDF files,",
		"making it easy to extract text, images, and metadata, as well as to create new PDF documents.",
	]
)

writer.content_writer()
writer.metadata_writer()
