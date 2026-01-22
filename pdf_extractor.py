import fitz
import re

from pdf_contents import Page, Block, Line, Content, PDFContents


class PDFExtractor:
    def __init__(self, pdf_file_path: str):
        """
        Open the PDF and initialize caches.

        Args:
            file_path (str): Path to the PDF file.
        """

        self.__pdf_file_path = pdf_file_path
        self.__doc: fitz.Document = self._extract_pdf_doc()

        self.__texts_cache: list[str] | None = None

    @property
    def pdf_file_path(self) -> str:
        """
        Return the PDF file path.

        Returns:
            str: PDF file path.
        """

        return self.__pdf_file_path
    
    def extract_contents(self):
        doc = self.__doc

        contents = []

        block_id = 0
        line_id = 0
        span_id = 0

        for number, fitz_page in enumerate(doc):
            page_width  = fitz_page.rect.width
            page_height = fitz_page.rect.height

            page = Page(fitz_page, number, page_width, page_height)

            page_dict = dict(fitz_page.get_text("dict"))

            page_blocks = page_dict.get("blocks")
            if not page_blocks:
                continue

            for block_dict in page_blocks:
                block_number = block_dict.get("number")
                block_bbox = block_dict.get("bbox")
                block = Block(page, block_id, block_number, block_bbox)

                block_lines = block_dict.get("lines")
                if not block_lines:
                    continue

                for line_number, line_dict in enumerate(block_lines):
                    line_bbox = line_dict.get("bbox")
                    line = Line(block, line_id, line_number, line_bbox)

                    spans = line_dict.get("spans")
                    if not spans:
                        continue

                    for span_number, span in enumerate(spans):
                        span_text = self._format_text(span.get("text"))
                        if not span_text:
                            continue
                        
                        span_bbox = span.get("bbox")
                        span_origin = span.get("origin")
                        span_ascender = span.get("ascender")
                        span_descender = span.get("descender")
                        span_size = span.get("size")
                        span_font = span.get("font")
                        span_flags = span.get("flags")
                        span_char_flags = span.get("char_flags")
                        span_bidi = span.get("bidi")
                        span_alpha = span.get("alpha")
                        span_color = span.get("color")
                        content = Content(
                            line, 
                            span_id, 
                            span_number, 
                            span_text, 
                            span_bbox, 
                            span_origin, 
                            span_ascender, 
                            span_descender, 
                            span_size, 
                            span_font, 
                            span_flags, 
                            span_char_flags, 
                            span_bidi, 
                            span_alpha, 
                            span_color
                        )

                        contents.append(content)

                        span_id += 1

                    line_id += 1

                block_id += 1

        return PDFContents(contents)
    
    def extract_texts(
        self, 
        use_cache: bool = True
    ) -> list[str]:
        """
        Extract raw text lines from the PDF.

        Args:
            use_cache (bool): Whether to reuse cached results.

        Returns:
            list[str]: Text lines.
        """

        if use_cache and self.__texts_cache:
            return self.__texts_cache
        
        doc = self.__doc

        texts = []

        for fitz_page in doc:
            page_texts = fitz_page.get_text("text")
            splited_texts = page_texts.split("\n")
            for text in splited_texts:
                stripped_text = text.strip()
                if stripped_text:
                    texts.append(stripped_text)

        self.__texts_cache = texts

        return texts
    
    def _extract_pdf_doc(self) -> fitz.Document:
        """
        Open the PDF document and authenticate if needed.

        Returns:
            fitz.Document: Opened PDF document.
        """

        file_path = self.__pdf_file_path

        if not file_path.lower().endswith(".pdf"):
            raise Exception("Unsupported file extension.")

        doc = fitz.open(file_path)
        if doc.needs_pass:
            doc = self._authenticate_doc(doc)
        
        return doc
    
    def _authenticate_doc(self, doc: fitz.Document) -> fitz.Document:
        """
        Authenticate a password-protected PDF.

        Args:
            doc (fitz.Document): PDF document.

        Returns:
            fitz.Document: Authenticated PDF document.
        """

        password_match = re.search(r"#([^#]+)#(?=[^#]*$)", self.__pdf_file_path)
        if not password_match:
            raise ValueError("No password found between '#' in the filename.")

        file_password = password_match.group(1)
        authentication_succeeded = doc.authenticate(file_password)
        if not authentication_succeeded:
            raise ValueError("Wrong password parsed from filename.")
        
        return doc
    
    @staticmethod
    def _format_text(text: str) -> str | None:
        """
        Normalize text by stripping whitespace and control characters.

        Args:
            text (str): Text to normalize.

        Returns:
            str: Normalized text.
        """

        if not text:
            return None

        text = text.strip()
        text = text.replace("\u2060", " ")
        text = text.replace("\n", " ")
        text = text.replace("\xa0", " ")
        text = text.replace("\t", " ")
        text = re.sub(r" {2,}", " ", text)

        return text
