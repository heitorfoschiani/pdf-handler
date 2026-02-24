import fitz
import re
from pathlib import Path

from .contents import (
    Page, 
    Block, 
    Line, 
    Content, 
    PDFContents
)


class PDFExtractor:
    """
    Extract structured texts and content blocks from PDF statement files.
    """

    def __init__(self, pdf_file_path: str | Path) -> None:
        """
        Initialize the instance by assigning the provided values.
        
        Args:
            pdf_file_path (str | Path): Path to the PDF file.
        """

        self.__pdf_file_path = Path(pdf_file_path)
        self.__doc: fitz.Document = self._extract_pdf_doc()

        self.__texts_cache: list[str] | None = None
        self.__contents_cache: PDFContents | None = None
    
    def extract_contents(self, use_cache: bool = True) -> PDFContents | None:
        """
        Extract contents by processing the available inputs.
        
        Args:
            use_cache (bool): Use cache used by the function logic.
        
        Returns:
            PDFContents | None: Result produced by the function logic.
        """

        if use_cache and self.__contents_cache:
            return self.__contents_cache

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

        if contents:
            pdf_contents = PDFContents(contents)
        else:
            pdf_contents = None

        self.__contents_cache = pdf_contents

        return pdf_contents
    
    def extract_texts(
        self, 
        use_cache: bool = True
    ) -> list[str] | None:
        """
        Extract texts by processing the available inputs.
        
        Args:
            use_cache (bool): Use cache used by the function logic.
        
        Returns:
            list[str] | None: Result produced by the function logic.
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

        if not texts:
            texts = None

        self.__texts_cache = texts

        return texts
    
    def _extract_pdf_doc(self) -> fitz.Document:
        """
        Open the PDF document and authenticate if needed.

        Returns:
            fitz.Document: Loaded document object.
        """

        file_path = self.__pdf_file_path
        if file_path.suffix.lower() != ".pdf":
            raise Exception("Unsupported file extension.")

        doc = fitz.open(str(file_path))
        if doc.needs_pass:
            doc = self._authenticate_doc(doc)
        
        return doc
    
    def _authenticate_doc(self, doc: fitz.Document) -> fitz.Document:
        """
        Authenticate doc by applying the function logic.
        
        Args:
            doc (fitz.Document): Doc used by the function logic.
        
        Returns:
            fitz.Document: Result produced by the function logic.
        """

        password_match = re.search(
            r"#([^#]+)#(?=[^#]*$)", 
            self.__pdf_file_path.name
        )
        if not password_match:
            raise ValueError("No password found between '#' in the filename.")

        file_password = password_match.group(1)
        authentication_succeeded = doc.authenticate(file_password)
        if not authentication_succeeded:
            raise ValueError("Wrong password parsed from filename.")
        
        return doc
    
    @staticmethod
    def _format_text(text: str | None) -> str | None:
        """
        Format text by applying the transformation rules.
        
        Args:
            text (str): Text used by the function logic.
        
        Returns:
            str | None: Result produced by the function logic.
        """

        if text is None:
            return None

        text = text.replace("\u2060", " ")
        text = text.replace("\n", " ")
        text = text.replace("\xa0", " ")
        text = text.replace("\t", " ")
        text = re.sub(r" {2,}", " ", text)
        text = text.strip()

        return text
