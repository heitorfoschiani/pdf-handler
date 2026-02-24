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
        Return dict by processing the available inputs.
        
        Returns:
            dict[str, Any]: Result produced by the function logic.
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
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.bbox[0]

    @property
    def yt(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.bbox[1]

    @property
    def xr(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.bbox[2]

    @property
    def yb(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.bbox[3]

    @property
    def xc(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return (self.xl + self.xr) / 2

    @property
    def yc(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return (self.yt + self.yb) / 2
    
    def get_dict(self) -> dict[str, Any]:
        """
        Return dict by processing the available inputs.
        
        Returns:
            dict[str, Any]: Result produced by the function logic.
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
        Execute the function logic using the provided inputs.
        
        Returns:
            Page: Result produced by the function logic.
        """

        return self.block.page

    @property
    def xl(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.bbox[0]

    @property
    def yt(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.bbox[1]

    @property
    def xr(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.bbox[2]

    @property
    def yb(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.bbox[3]

    @property
    def xc(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return (self.xl + self.xr) / 2

    @property
    def yc(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return (self.yt + self.yb) / 2
    
    @property
    def width(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.xr - self.xl

    @property
    def height(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.yb - self.yt
    
    @property
    def area(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.width * self.height
    
    def get_dict(self) -> dict[str, Any]:
        """
        Return dict by processing the available inputs.
        
        Returns:
            dict[str, Any]: Result produced by the function logic.
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
        Execute the function logic using the provided inputs.
        
        Returns:
            Block: Result produced by the function logic.
        """

        return self.line.block

    @property
    def page(self) -> Page:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            Page: Result produced by the function logic.
        """

        return self.block.page

    @property
    def xl(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.bbox[0]

    @property
    def yt(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.bbox[1]

    @property
    def xr(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.bbox[2]

    @property
    def yb(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.bbox[3]

    @property
    def xc(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return (self.xl + self.xr) / 2

    @property
    def yc(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return (self.yt + self.yb) / 2

    @property
    def xo(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.origin[0]

    @property
    def yo(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.origin[1]

    @property
    def width(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.xr - self.xl

    @property
    def height(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.yb - self.yt

    @property
    def area(self) -> float:
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            float: Result produced by the function logic.
        """

        return self.width * self.height

    def get_dict(self) -> dict[str, Any]:
        """
        Return dict by processing the available inputs.
        
        Returns:
            dict[str, Any]: Result produced by the function logic.
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
    """
    Store parsed PDF content spans and provide sorting, grouping, and join helpers.
    """

    def __init__(
        self,
        contents: list[Content], 
        sorted_by: tuple[str, ...] | None = None, 
        horizontal_end_on_page_by_x: tuple[float, ...] | None = None, 
        is_joined: bool = False
    ) -> None:
        """
        Initialize the instance by assigning the provided values.
        
        Args:
            contents (list[Content]): Contents used by the function logic.
            sorted_by (tuple[str, ...] | None): Sorted by used by the function logic.
            horizontal_end_on_page_by_x (tuple[float, ...] | None): Horizontal end on page by x used by the function logic.
            is_joined (bool): Is joined used by the function logic.
        """

        super().__init__(contents)

        self.__sorted_by = sorted_by
        self.__horizontal_end_on_page_by_x = horizontal_end_on_page_by_x
        self.__is_joined = is_joined

    @property
    def sorted_by(self) -> tuple[str, ...] | None:
        """
        Sorted by by applying the function logic.
        
        Returns:
            tuple[str, ...] | None: Result produced by the function logic.
        """

        return self.__sorted_by
    
    @property
    def horizontal_end_on_page_by_x(self) -> tuple[float, ...] | None:
        """
        Horizontal end on page by x by applying the function logic.
        
        Returns:
            tuple[float, ...] | None: Result produced by the function logic.
        """

        return self.__horizontal_end_on_page_by_x
    
    @property
    def is_joined(self) -> bool:
        """
        Evaluate whether joined by checking the provided data.
        
        Returns:
            bool: Boolean result of the evaluated condition.
        """

        return self.__is_joined

    def copy(self) -> "PDFContents":
        """
        Execute the function logic using the provided inputs.
        
        Returns:
            'PDFContents': Result produced by the function logic.
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
        Sort data by applying the transformation rules.
        
        Args:
            by (tuple[str, ...]): By used by the function logic.
            use_cache (bool): Use cache used by the function logic.
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
        Execute the function logic using the provided inputs.
        
        Args:
            by (tuple[str, ...]): By used by the function logic.
            use_cache (bool): Use cache used by the function logic.
        
        Returns:
            'PDFContents': Result produced by the function logic.
        """

        pdf_contents = self.copy()
        pdf_contents.sort(by, use_cache)

        return pdf_contents

    def join(
        self, 
        use_cache: bool = True
    ) -> None:        
        """
        Execute the function logic using the provided inputs.
        
        Args:
            use_cache (bool): Use cache used by the function logic.
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
        Execute the function logic using the provided inputs.
        
        Args:
            use_cache (bool): Use cache used by the function logic.
        
        Returns:
            'PDFContents': Result produced by the function logic.
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
        Assign horizontal end on page by updating the target state.
        
        Args:
            x_delimiters (tuple[float, ...]): X delimiters used by the function logic.
            use_cache (bool): Use cache used by the function logic.
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
        Horizontal end on page assigned by applying the function logic.
        
        Args:
            x_delimiters (tuple[float, ...]): X delimiters used by the function logic.
            use_cache (bool): Use cache used by the function logic.
        
        Returns:
            'PDFContents': Result produced by the function logic.
        """

        pdf_contents = self.copy()
        pdf_contents.assign_horizontal_end_on_page(x_delimiters, use_cache)
    
        return pdf_contents
    
    def get_contents_from_same_attr(
        self, 
        i_ref: int, 
        attr: str, 
        diff_tolerance: int | float = 0
    ) -> "PDFContents":
        """
        Return contents from same attr by processing the available inputs.
        
        Args:
            i_ref (int): I ref used by the function logic.
            attr (str): Attr used by the function logic.
            diff_tolerance (int | float): Diff tolerance used by the function logic.
        
        Returns:
            'PDFContents': Result produced by the function logic.
        """

        if diff_tolerance < 0:
            raise ValueError("The argument 'diff_tolerance' can not be less then zero.")

        content_ref = self[i_ref]
        get_attr = attrgetter(attr)
        ref_attr = get_attr(content_ref)

        if not (isinstance(ref_attr, int) or isinstance(ref_attr, float)):
            raise ValueError("The 'attr' must be int or float.")

        pdf_content = self.copy()
        pdf_content.sort(by=(
            "page.number", 
            attr
        ))

        # Discovering the first content of the block
        i_initial = 0
        while (
            i_initial < len(pdf_content)
            and not self._is_same_attr(pdf_content[i_initial], content_ref, attr, diff_tolerance)
        ):
            i_initial += 1

        if i_initial == len(pdf_content):
            raise ValueError("Reference content not found when searching for same attr.")

        contents_from_same_attr = [pdf_content[i_initial]]

        # Extracting contents
        i = i_initial + 1
        while (
            i < len(pdf_content)
            and self._is_same_attr(pdf_content[i], content_ref, attr, diff_tolerance)
        ):
            contents_from_same_attr.append(pdf_content[i])
            i += 1

        contents_from_same_attr = PDFContents(contents_from_same_attr)
        if self.__sorted_by is not None:
            sort_by = self.__sorted_by
        else:
            sort_by = ("id",)

        contents_from_same_attr.sort(by=sort_by)

        return contents_from_same_attr

    def get_contents_from_same_row(
        self, 
        i_ref: int, 
        yo_diff_tolerance: float = 0.0
    ) -> "PDFContents":
        """
        Return contents from same row by processing the available inputs.
        
        Args:
            i_ref (int): I ref used by the function logic.
            yo_diff_tolerance (float): Yo diff tolerance used by the function logic.
        
        Returns:
            'PDFContents': Result produced by the function logic.
        """

        if yo_diff_tolerance < 0:
            raise ValueError("The argument 'yo_diff_tolerance' can not be less then zero.")

        content_ref = self[i_ref]

        pdf_content = self.copy()
        pdf_content.sort(by=(
            "page.number", 
            "yo"
        ))

        # discovering the first content of the row
        i_initial = 0
        while (
            i_initial < len(pdf_content) 
            and not self._is_same_row(pdf_content[i_initial], content_ref, yo_diff_tolerance)
        ):
            i_initial += 1
            
        if i_initial == len(pdf_content):
            raise ValueError("Reference content not found when searching for same row.")

        contents_from_same_row = [pdf_content[i_initial]]

        # Extracting contents
        i = i_initial + 1
        while (
            i < len(pdf_content) 
            and self._is_same_row(pdf_content[i], content_ref, yo_diff_tolerance)
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
    
    def check_if_matches(
        self, 
        known_contents: list[dict], 
        exactly_text: bool = False
    ) -> bool:
        """
        Validate if matches by checking the required conditions.
        
        Args:
            known_contents (list[dict]): Known contents used by the function logic.
            exactly_text (bool): Exactly text used by the function logic.
        
        Returns:
            bool: Result produced by the function logic.
        """

        for known_content in known_contents:
            found_match = False
            for content in self:
                if all(
                    (attrgetter(key)(content) == value)
                    if (key != "text" or exactly_text)
                    else (value in attrgetter(key)(content))
                    for key, value in known_content.items()
                ):
                    found_match = True
                    break

            if not found_match:
                return False

        return True

    def _replace_contents(
        self, 
        new_pdf_contents: list[Content]
    ) -> None:
        """
        Replace contents by applying the function logic.
        
        Args:
            new_pdf_contents (list[Content]): New pdf contents used by the function logic.
        """

        self.clear()
        self.extend(new_pdf_contents)

    @staticmethod
    def _is_sequential(content1: Content, content2: Content) -> bool:
        """
        Evaluate whether sequential by checking the provided data.
        
        Args:
            content1 (Content): Content1 used by the function logic.
            content2 (Content): Content2 used by the function logic.
        
        Returns:
            bool: Result produced by the function logic.
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
    def _is_same_attr(
        content1: Content, 
        content2: Content, 
        attr: str, 
        diff_tolerance: int | float
    ) -> bool:
        """
        Evaluate whether same attr by checking the provided data.
        
        Args:
            content1 (Content): Content1 used by the function logic.
            content2 (Content): Content2 used by the function logic.
            attr (str): Attr used by the function logic.
            diff_tolerance (int | float): Diff tolerance used by the function logic.
        
        Returns:
            bool: Result produced by the function logic.
        """

        get_attr = attrgetter(attr)
        content1_page = content1.page
        content2_page = content2.page
        content1_attr = get_attr(content1)
        content2_attr = get_attr(content2)

        return (
            content1_page == content2_page
            and abs(content1_attr - content2_attr) <= diff_tolerance
        )
    
    @staticmethod
    def _is_same_row(content1: Content, content2: Content, yo_diff_tolerance: float) -> bool:
        """
        Evaluate whether same row by checking the provided data.
        
        Args:
            content1 (Content): Content1 used by the function logic.
            content2 (Content): Content2 used by the function logic.
            yo_diff_tolerance (float): Yo diff tolerance used by the function logic.
        
        Returns:
            bool: Result produced by the function logic.
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
    def _create_content_by_sequential(
        sequencial_contents: list[Content], 
        new_content_id: int
    ) -> Content:
        """
        Create content by sequential by composing values from the inputs.
        
        Args:
            sequencial_contents (list[Content]): Sequencial contents used by the function logic.
            new_content_id (int): New content id used by the function logic.
        
        Returns:
            Content: Result produced by the function logic.
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
        ).strip()

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
