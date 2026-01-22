from dataclasses import dataclass

import fitz
from typing import Any
from operator import attrgetter


@dataclass(slots=True)
class Page:
    """
    Store basic page data from the source document.

    Attributes:
        fitz_page (fitz.Page): Page object from PyMuPDF.
        number (int): Zero-based page index.
        width (float): Page width in points.
        height (float): Page height in points.
    """

    fitz_page: fitz.Page
    number: int
    width: float
    height: float

    def get_dict(self) -> dict[str, Any]:
        """
        Build a dictionary representation of the page.

        Returns:
            dict[str, Any]: Page number and size data.
        """

        return {
            "number": self.number,
            "width": self.width,
            "height": self.height,
        }

@dataclass(slots=True)
class Block:
    """
    Capture block metadata and its bounding box on a page.

    Attributes:
        page (Page): Parent page.
        id (int): Sequential block identifier.
        number (int): Block index from the PDF.
        bbox (tuple[float, float, float, float]): Bounding box (xl, yt, xr, yb).
    """

    page: Page
    id: int
    number: int
    bbox: tuple[float, float, float, float]

    @property
    def xl(self) -> float:
        """
        Return the left x coordinate.

        Returns:
            float: Bounding box left edge.
        """

        return self.bbox[0]

    @property
    def yt(self) -> float:
        """
        Return the top y coordinate.

        Returns:
            float: Bounding box top edge.
        """

        return self.bbox[1]

    @property
    def xr(self) -> float:
        """
        Return the right x coordinate.

        Returns:
            float: Bounding box right edge.
        """

        return self.bbox[2]

    @property
    def yb(self) -> float:
        """
        Return the bottom y coordinate.

        Returns:
            float: Bounding box bottom edge.
        """

        return self.bbox[3]

    @property
    def xc(self) -> float:
        """
        Return the horizontal center.

        Returns:
            float: Midpoint between xl and xr.
        """

        return (self.xl + self.xr) / 2

    @property
    def yc(self) -> float:
        """
        Return the vertical center.

        Returns:
            float: Midpoint between yt and yb.
        """

        return (self.yt + self.yb) / 2
    
    def get_dict(self) -> dict[str, Any]:
        """
        Build a dictionary for the block with page fields namespaced.

        Returns:
            dict[str, Any]: Block geometry and page metadata.
        """

        page_dict = self.page.get_dict()
        for key in page_dict.copy():
            page_dict[f"page_{key}"] = page_dict.pop(key)

        return {
            "id": self.id, 
            "number": self.number,
            "xl": self.xl,
            "yt": self.yt,
            "xr": self.xr,
            "yb": self.yb,
            "xc": self.xc,
            "yc": self.yc,
            **page_dict
        }


@dataclass(slots=True)
class Line:
    """
    Store line metadata inside a block.

    Attributes:
        block (Block): Parent block.
        id (int): Sequential line identifier.
        number (int): Line index within the block.
        bbox (tuple[float, float, float, float]): Bounding box (xl, yt, xr, yb).
    """

    block: Block
    id: int
    number: int
    bbox: tuple[float, float, float, float]

    @property
    def page(self) -> Page:
        """
        Return the page containing the line.

        Returns:
            Page: Page of the parent block.
        """

        return self.block.page

    @property
    def xl(self) -> float:
        """
        Return the left x coordinate.

        Returns:
            float: Bounding box left edge.
        """

        return self.bbox[0]

    @property
    def yt(self) -> float:
        """
        Return the top y coordinate.

        Returns:
            float: Bounding box top edge.
        """

        return self.bbox[1]

    @property
    def xr(self) -> float:
        """
        Return the right x coordinate.

        Returns:
            float: Bounding box right edge.
        """

        return self.bbox[2]

    @property
    def yb(self) -> float:
        """
        Return the bottom y coordinate.

        Returns:
            float: Bounding box bottom edge.
        """

        return self.bbox[3]

    @property
    def xc(self) -> float:
        """
        Return the horizontal center.

        Returns:
            float: Midpoint between xl and xr.
        """

        return (self.xl + self.xr) / 2

    @property
    def yc(self) -> float:
        """
        Return the vertical center.

        Returns:
            float: Midpoint between yt and yb.
        """

        return (self.yt + self.yb) / 2
    
    @property
    def width(self) -> float:
        """
        Return the line width.

        Returns:
            float: Difference between xr and xl.
        """

        return self.xr - self.xl

    @property
    def height(self) -> float:
        """
        Return the line height.

        Returns:
            float: Difference between yb and yt.
        """

        return self.yb - self.yt
    
    @property
    def area(self) -> float:
        """
        Return the line area.

        Returns:
            float: Product of width and height.
        """

        return self.width * self.height
    
    def get_dict(self) -> dict[str, Any]:
        """
        Build a dictionary for the line with block and page prefixes.

        Returns:
            dict[str, Any]: Line geometry plus parent metadata.
        """

        block_dict = self.block.get_dict()
        for key in block_dict.copy():
            if not key.startswith("page_"):
                block_dict[f"block_{key}"] = block_dict.pop(key)

        return {
            "id": self.id, 
            "number": self.number,
            "xl": self.xl,
            "yt": self.yt,
            "xr": self.xr,
            "yb": self.yb,
            "xc": self.xc,
            "yc": self.yc,
            "width": self.width,
            "height": self.height,
            "area": self.area,
            **block_dict
        }
    


@dataclass(slots=True)
class Content:
    """
    Store a text span and its visual attributes.

    Attributes:
        line (Line): Parent line.
        id (int): Sequential content identifier.
        number (int): Span index within the line.
        text (str): Span text.
        bbox (tuple[float, float, float, float]): Bounding box (xl, yt, xr, yb).
        origin (tuple[float, float]): Text origin coordinates.
        ascender (float): Font ascender height.
        descender (float): Font descender depth.
        size (float): Font size.
        font (str): Font family name.
        flags (int): Text flags from PyMuPDF.
        char_flags (int): Character flags from PyMuPDF.
        bidi (int): Bidirectional level.
        alpha (int): Alpha channel value.
        rgb_color (int): RGB color integer.
        horizontal_end_on_page (int | None): Bucket index assigned across the page.
    """

    line: Line
    id: int
    number: int
    text: str
    bbox: tuple[float, float, float, float]
    origin: tuple[float, float]
    ascender: float
    descender: float
    size: float
    font: str
    flags: int
    char_flags: int
    bidi: int
    alpha: int
    rgb_color: int
    horizontal_end_on_page: int | None = None

    @property
    def block(self) -> Block:
        """
        Return the parent block.

        Returns:
            Block: Block that contains the line.
        """

        return self.line.block

    @property
    def page(self) -> Page:
        """
        Return the page containing the span.

        Returns:
            Page: Page of the parent block.
        """

        return self.block.page

    @property
    def xl(self) -> float:
        """
        Return the left x coordinate.

        Returns:
            float: Bounding box left edge.
        """

        return self.bbox[0]

    @property
    def yt(self) -> float:
        """
        Return the top y coordinate.

        Returns:
            float: Bounding box top edge.
        """

        return self.bbox[1]

    @property
    def xr(self) -> float:
        """
        Return the right x coordinate.

        Returns:
            float: Bounding box right edge.
        """

        return self.bbox[2]

    @property
    def yb(self) -> float:
        """
        Return the bottom y coordinate.

        Returns:
            float: Bounding box bottom edge.
        """

        return self.bbox[3]

    @property
    def xc(self) -> float:
        """
        Return the horizontal center.

        Returns:
            float: Midpoint between xl and xr.
        """

        return (self.xl + self.xr) / 2

    @property
    def yc(self) -> float:
        """
        Return the vertical center.

        Returns:
            float: Midpoint between yt and yb.
        """

        return (self.yt + self.yb) / 2

    @property
    def xo(self) -> float:
        """
        Return the origin x coordinate.

        Returns:
            float: X value from origin.
        """

        return self.origin[0]

    @property
    def yo(self) -> float:
        """
        Return the origin y coordinate.

        Returns:
            float: Y value from origin.
        """

        return self.origin[1]

    @property
    def width(self) -> float:
        """
        Return the span width.

        Returns:
            float: Difference between xr and xl.
        """

        return self.xr - self.xl

    @property
    def height(self) -> float:
        """
        Return the span height.

        Returns:
            float: Difference between yb and yt.
        """

        return self.yb - self.yt

    @property
    def area(self) -> float:
        """
        Return the span area.

        Returns:
            float: Product of width and height.
        """

        return self.width * self.height

    def get_dict(self) -> dict[str, Any]:
        """
        Build a dictionary for the content with parent fields prefixed.

        Returns:
            dict[str, Any]: Text data, geometry, and inherited metadata.
        """

        line_dict = self.line.get_dict()
        for key in line_dict.copy():
            if not (
                key.startswith('page_') 
                or key.startswith('block_')
            ):
                line_dict[f"line_{key}"] = line_dict.pop(key)

        return {
            'id': self.id, 
            'number': self.number,
            'text': self.text,
            'xl': self.xl,
            'yt': self.yt,
            'xr': self.xr,
            'yb': self.yb,
            'xc': self.xc,
            'yc': self.yc,
            'xo': self.xo,
            'yo': self.yo,
            'width': self.width,
            'height': self.height,
            'area': self.area,
            'ascender': self.ascender,
            'descender': self.descender,
            'size': self.size,
            'font': self.font,
            'flags': self.flags,
            'char_flags': self.char_flags,
            'bidi': self.bidi,
            'alpha': self.alpha,
            'rgb_color': self.rgb_color, 
            'horizontal_end_on_page': self.horizontal_end_on_page, 
            **line_dict
        }


class PDFContents(list[Content]):
    def __init__(
        self,
        contents: list[Content], 
        sorted_by: tuple[str, ...] | None = None, 
        horizontal_end_on_page_by_x: tuple[float, ...] | None = None, 
        is_joined: bool = False
    ) -> None:
        """
        Wrap a list of content items with sorting and grouping metadata.

        Args:
            contents (list[Content]): Contents to manage.
            sorted_by (tuple[str, ...] | None): Cached sort keys.
            horizontal_end_on_page_by_x (tuple[float, ...] | None): X delimiters used to bucket spans.
            is_joined (bool): Flag indicating whether sequential spans were already joined.
        """

        super().__init__(contents)

        self.__sorted_by = sorted_by
        self.__horizontal_end_on_page_by_x = horizontal_end_on_page_by_x
        self.__is_joined = is_joined

    @property
    def sorted_by(self) -> tuple[str, ...] | None:
        """
        Return the cached sort keys.

        Returns:
            tuple[str, ...] | None: Attributes used in the last sort.
        """

        return self.__sorted_by
    
    @property
    def horizontal_end_on_page_by_x(self) -> tuple[float, ...] | None:
        """
        Return the cached x delimiters for horizontal buckets.

        Returns:
            tuple[float, ...] | None: Delimiters applied to contents.
        """

        return self.__horizontal_end_on_page_by_x
    
    @property
    def is_joined(self) -> bool:
        """
        Indicate whether sequential spans were merged.

        Returns:
            bool: True when join() has been applied.
        """

        return self.__is_joined

    def copy(self) -> "PDFContents":
        """
        Create a shallow copy preserving cached metadata.

        Returns:
            PDFContents: Duplicated contents list.
        """

        return PDFContents(
            self, 
            self.__sorted_by, 
            self.__horizontal_end_on_page_by_x, 
            self.__is_joined
        )
    
    def sort(
        self, 
        by: tuple[str, ...] = (
            "page.number",
            "yo",
            "xo",
            "block.id",
            "line.id"
        ), 
        use_cache: bool = True
    ) -> None:
        """
        Sort contents in place by the provided attributes.

        Args:
            by (tuple[str, ...]): Attribute paths used to order items.
            use_cache (bool): Skip sorting when already ordered with the same keys.
        """

        if (
            use_cache 
            and self.__sorted_by is not None
        ):
            if self.__sorted_by == by:
                return

        getter = attrgetter(*by)
        super().sort(key=getter)

        self.__sorted_by = by

    def sorted(
        self, 
        by: tuple[str, ...] = (
            "page.number",
            "yo",
            "xo",
            "block.id",
            "line.id"
        ), 
        use_cache: bool = True
    ) -> "PDFContents":
        """
        Return a sorted copy without mutating the original list.

        Args:
            by (tuple[str, ...]): Attribute paths used to order items.
            use_cache (bool): Reuse cached ordering when possible.

        Returns:
            PDFContents: New list sorted by the given keys.
        """

        pdf_contents = self.copy()
        pdf_contents.sort(by, use_cache)

        return pdf_contents

    def join(
        self, 
        use_cache: bool = True
    ) -> None:        
        """
        Merge sequential spans that share layout and style.

        Args:
            use_cache (bool): Skip processing when already joined.
        """

        if use_cache and self.__is_joined:
            return
        
        self.sort(by=(
            "page.number",
            "yo",
            "xo",
            "block.id",
            "line.id", 
            "rgb_color", 
            "font", 
            "size"
        ))

        joined_pdf_contents = []
        
        new_content_id = 0 
        i = 0
        while i < len(self):
            sequencial_contents = [self[i]]

            j = i + 1
            while (
                j < len(self)
                and self._is_sequential(self[j], self[j - 1])
            ):
                sequencial_contents.append(self[j])
                j += 1

            content = self._create_content_by_sequential(
                sequencial_contents, 
                new_content_id
            )

            joined_pdf_contents.append(content)
            
            i = j
            new_content_id += 1

        joined_pdf_contents = PDFContents(joined_pdf_contents)
        if self.__sorted_by is not None:
            sort_by = self.__sorted_by
        else:
            sort_by = (
                "page.number",
                "block.id",
                "line.id"
            )

        joined_pdf_contents.sort(by=sort_by)

        self._replace_contents(joined_pdf_contents)

        self.__is_joined = True

    def joined(
        self, 
        use_cache: bool = True
    ) -> "PDFContents":
        """
        Return a joined copy of the contents list.

        Args:
            use_cache (bool): Skip processing when a joined version is cached.

        Returns:
            PDFContents: Copy where sequential spans are merged.
        """

        pdf_contents = self.copy()
        pdf_contents.join(use_cache)
    
        return pdf_contents

    def assign_horizontal_end_on_page(
        self, 
        x_delimiters: tuple[float, ...], 
        use_cache: bool = True
    ) -> None:
        """
        Assign each content to a horizontal bucket using x delimiters.

        Args:
            x_delimiters (tuple[float, ...]): X thresholds that define buckets.
            use_cache (bool): Skip assignment when cached delimiters match.
        """

        if (
            use_cache 
            and self.__horizontal_end_on_page_by_x is not None
        ):
            if self.__horizontal_end_on_page_by_x == x_delimiters:
                return
        
        for content in self:
            assigned_bucket = len(x_delimiters)
            for i, x_delimiter in enumerate(x_delimiters):
                if content.xl <= x_delimiter:
                    assigned_bucket = i
                    break
                
            content.horizontal_end_on_page = assigned_bucket

        self.__horizontal_end_on_page_by_x = x_delimiters

    def horizontal_end_on_page_assigned(
        self, 
        x_delimiters: tuple[float, ...], 
        use_cache: bool = True
    ) -> "PDFContents":
        """
        Return a copy with horizontal buckets assigned.

        Args:
            x_delimiters (tuple[float, ...]): X thresholds that define buckets.
            use_cache (bool): Skip reassignment when cached delimiters match.

        Returns:
            PDFContents: Copy with bucket metadata updated.
        """

        pdf_contents = self.copy()
        pdf_contents.assign_horizontal_end_on_page(x_delimiters, use_cache)
    
        return pdf_contents

    def get_contents_from_same_block(
        self, 
        i_ref: int
    ) -> "PDFContents":
        """
        Return contents that share the same block as the reference item.

        Args:
            i_ref (int): Index of the reference content in the current list.

        Returns:
            PDFContents: Contents from the same block.
        """

        pdf_content = self.copy()
        pdf_content.sort(by=(
            "page.number", 
            "block.id"
        ))

        # Descovering the first content of the block
        i_initial = 0
        while (
            i_initial < len(pdf_content)
            and not self._is_same_block(pdf_content[i_initial], self[i_ref])
        ):
            i_initial += 1

        if i_initial == len(pdf_content):
            raise ValueError("Reference content not found when searching for same block.")

        contents_from_same_block = [pdf_content[i_initial]]

        # Extracting contents
        i = i_initial + 1
        while (
            i < len(pdf_content)
            and self._is_same_block(pdf_content[i], pdf_content[i - 1])
        ):
            contents_from_same_block.append(pdf_content[i])
            i += 1

        contents_from_same_block = PDFContents(contents_from_same_block)
        if self.__sorted_by is not None:
            sort_by = self.__sorted_by
        else:
            sort_by = ("id",)

        contents_from_same_block.sort(by=sort_by)

        return contents_from_same_block

    def get_contents_from_same_row(
        self, 
        i_ref: int, 
        yo_diff_tolerance: float = 0.0
    ) -> "PDFContents":
        """
        Return contents that align on the same row as the reference item.

        Args:
            i_ref (int): Index of the reference content in the current list.
            yo_diff_tolerance (float): Allowed vertical offset between items.

        Returns:
            PDFContents: Contents from the same row.
        """

        if yo_diff_tolerance < 0:
            raise ValueError("The argument 'yo_diff_tolerance' can not be less then zero.")

        pdf_content = self.copy()
        pdf_content.sort(by=(
            "page.number", 
            "yo"
        ))

        # Descovering the first content of the row
        i_initial = 0
        while (
            i_initial < len(pdf_content) 
            and not self._is_same_row(pdf_content[i_initial], self[i_ref], yo_diff_tolerance)
        ):
            i_initial += 1
            
        if i_initial == len(pdf_content):
            raise ValueError("Reference content not found when searching for same row.")

        contents_from_same_row = [pdf_content[i_initial]]

        # Extracting contents
        i = i_initial + 1
        while (
            i < len(pdf_content) 
            and self._is_same_row(pdf_content[i], pdf_content[i - 1], yo_diff_tolerance)
        ):
            contents_from_same_row.append(pdf_content[i])
            i += 1

        contents_from_same_row = PDFContents(contents_from_same_row)
        if self.__sorted_by is not None:
            sort_by = self.__sorted_by
        else:
            sort_by = ("id",)

        contents_from_same_row.sort(by=sort_by)

        return contents_from_same_row
    
    def get_contents_from_same_line(
        self, 
        i_ref: int
    ) -> "PDFContents":
        """
        Return contents that share the same line as the reference item.

        Args:
            i_ref (int): Index of the reference content in the current list.

        Returns:
            PDFContents: Contents from the same line.
        """

        pdf_content = self.copy()
        pdf_content.sort(by=(
            "page.number",
            "line.id",
        ))

        # Descovering the first content of the line
        i_initial = 0
        while (
            i_initial < len(pdf_content) 
            and not self._is_same_line(pdf_content[i_initial], self[i_ref])
        ):
            i_initial += 1

        if i_initial == len(pdf_content):
            raise ValueError("Reference content not found when searching for same line.")

        contents_from_same_line = [pdf_content[i_initial]]

        # Extracting contents
        i = i_initial + 1
        while (
            i < len(pdf_content) 
            and self._is_same_line(pdf_content[i], pdf_content[i - 1])
        ):
            contents_from_same_line.append(pdf_content[i])
            i += 1

        contents_from_same_line = PDFContents(contents_from_same_line)
        if self.__sorted_by is not None:
            sort_by = self.__sorted_by
        else:
            sort_by = ("id",)

        contents_from_same_line.sort(by=sort_by)
        
        return contents_from_same_line

    def _replace_contents(
        self, 
        new_pdf_contents: list[Content]
    ) -> None:
        """
        Replace the current list items with a new collection.

        Args:
            new_pdf_contents (list[Content]): Contents that overwrite the list.
        """

        self.clear()
        self.extend(new_pdf_contents)

    @staticmethod
    def _is_sequential(content1: Content, content2: Content) -> bool:
        """
        Check if two contents belong to the same sequence for joining.

        Args:
            content1 (Content): First content item.
            content2 (Content): Second content item.

        Returns:
            bool: True when line, style, and position align.
        """

        content1_line_id = content1.line.id
        content2_line_id = content2.line.id

        content1_font = content1.font
        content2_font = content2.font

        content1_flags = content1.flags
        content2_flags = content2.flags

        content1_char_flags = content1.char_flags
        content2_char_flags = content2.char_flags

        content1_bidi = content1.bidi
        content2_bidi = content2.bidi

        content1_alpha = content1.alpha
        content2_alpha = content2.alpha

        content1_rgb_color = content1.rgb_color
        content2_rgb_color = content2.rgb_color

        content1_horizontal_end_on_page = content1.horizontal_end_on_page
        content2_horizontal_end_on_page = content2.horizontal_end_on_page

        content1_size = round(content1.size, 2)
        content2_size = round(content2.size, 2)

        content1_yo = round(content1.yo, 2)
        content2_yo = round(content2.yo, 2)

        return (
            content1_line_id == content2_line_id
            and content1_font == content2_font
            and content1_flags == content2_flags
            and content1_char_flags == content2_char_flags
            and content1_bidi == content2_bidi
            and content1_alpha == content2_alpha
            and content1_rgb_color == content2_rgb_color
            and content1_horizontal_end_on_page == content2_horizontal_end_on_page
            and content1_size == content2_size
            and content1_yo == content2_yo
        )
    
    @staticmethod
    def _is_same_block(content1: Content, content2: Content) -> bool:
        """
        Check whether two contents belong to the same block.

        Args:
            content1 (Content): First content item.
            content2 (Content): Second content item.

        Returns:
            bool: True when block identifiers match.
        """

        content1_block_id = content1.block.id
        content2_block_id = content2.block.id

        return content1_block_id == content2_block_id
    
    @staticmethod
    def _is_same_row(content1: Content, content2: Content, yo_diff_tolerance: float) -> bool:
        """
        Check whether two contents share the same row within a tolerance.

        Args:
            content1 (Content): First content item.
            content2 (Content): Second content item.
            yo_diff_tolerance (float): Allowed vertical offset.

        Returns:
            bool: True when page matches and vertical gap is within tolerance.
        """

        content1_page_num = content1.page.number
        content2_page_num = content2.page.number
        content1_yo = round(content1.yo, 2)
        content2_yo = round(content2.yo, 2)

        return (
            content1_page_num == content2_page_num
            and abs(content1_yo - content2_yo) <= yo_diff_tolerance
        )
    
    @staticmethod
    def _is_same_line(content: Content, previous_content: Content) -> bool:
        """
        Check whether two contents belong to the same line.

        Args:
            content (Content): Current content item.
            previous_content (Content): Previous content item.

        Returns:
            bool: True when line identifiers match.
        """

        content_line_id = int(content.line.id)
        previous_content_line_id = int(previous_content.line.id)

        return content_line_id == previous_content_line_id

    @staticmethod
    def _create_content_by_sequential(
        sequencial_contents: list[Content], 
        new_content_id: int
    ) -> Content:
        """
        Create a new content item by merging sequential spans.

        Args:
            sequencial_contents (list[Content]): Contents to be merged.
            new_content_id (int): Identifier for the new content.

        Returns:
            Content: Aggregated content covering the merged spans.
        """

        joined_content_line = sequencial_contents[0].line

        joined_content_bbox = (
            min([content.xl for content in sequencial_contents]), 
            min([content.yt for content in sequencial_contents]), 
            max([content.xr for content in sequencial_contents]), 
            max([content.yb for content in sequencial_contents])
        )
            
        joined_content_text = " ".join(
            [
                content.text
                for content in sequencial_contents
            ]
        )
        joined_content_number = min([content.number for content in sequencial_contents])
        joined_content_xo = min([content.xo for content in sequencial_contents])
        joined_content_yo = min([content.yo for content in sequencial_contents])
        joined_content_origin = (joined_content_xo, joined_content_yo)
        joined_content_ascender = max([content.ascender for content in sequencial_contents])
        joined_content_descender = min([content.descender for content in sequencial_contents])
        joined_content_size = sequencial_contents[0].size
        joined_content_font = sequencial_contents[0].font
        joined_content_flags = sequencial_contents[0].flags
        joined_content_char_flags = sequencial_contents[0].char_flags
        joined_content_bidi = sequencial_contents[0].bidi
        joined_content_alpha = sequencial_contents[0].alpha
        joined_content_rgb_color = sequencial_contents[0].rgb_color
        joined_horizontal_end_on_page = sequencial_contents[0].horizontal_end_on_page

        return Content(
            joined_content_line, 
            new_content_id, 
            joined_content_number, 
            joined_content_text, 
            joined_content_bbox, 
            joined_content_origin, 
            joined_content_ascender, 
            joined_content_descender, 
            joined_content_size, 
            joined_content_font, 
            joined_content_flags, 
            joined_content_char_flags, 
            joined_content_bidi, 
            joined_content_alpha, 
            joined_content_rgb_color, 
            joined_horizontal_end_on_page
        )
