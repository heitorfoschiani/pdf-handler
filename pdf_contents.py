import fitz
from typing import Any
from operator import attrgetter


class Page:
    def __init__(
        self, 
        fitz_page: fitz.Page, 
        number: int, 
        width: float, 
        height: float
    ):
        self.__fitz_page = fitz_page
        self.__number = number
        self.__width = width
        self.__height = height

    @property
    def number(self) -> int:
        return self.__number
    
    @property
    def width(self) -> float:
        return self.__width
    
    @property
    def height(self) -> float:
        return self.__height
    
    def get_dict(
        self
    ) -> dict[str, Any]:
        return {
            "number": self.number,
            "width": self.width,
            "height": self.height,
        }
    

class Block:
    def __init__(
        self,
        page: Page, 
        id: int, 
        number: int, 
        bbox: tuple[float, float, float, float]
    ):
        self.__page = page
        self.__id = id
        self.__number = number
        self.__bbox = bbox

    @property
    def page(self) -> Page:
        return self.__page
    
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def number(self) -> int:
        return self.__number
    
    @property
    def bbox(self) -> tuple[float]:
        return self.__bbox

    @property
    def xl(self) -> float:
        return self.__bbox[0]

    @property
    def yt(self) -> float:
        return self.__bbox[1]

    @property
    def xr(self) -> float:
        return self.__bbox[2]

    @property
    def yb(self) -> float:
        return self.__bbox[3]

    @property
    def xc(self) -> float:
        return (self.xl + self.xr) / 2

    @property
    def yc(self) -> float:
        return (self.yt + self.yb) / 2
    
    def get_dict(
        self
    ) -> dict[str, Any]:
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


class Line:
    def __init__(
        self,
        block: Block, 
        id: int, 
        number: int, 
        bbox: tuple[float, float, float, float]
    ):
        self.__block = block
        self.__id = id
        self.__number = number
        self.__bbox = bbox

    @property
    def page(self) -> Page:
        return self.__block.page

    @property
    def block(self) -> Block:
        return self.__block
    
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def number(self) -> int:
        return self.__number
    
    @property
    def bbox(self) -> tuple[float]:
        return self.__bbox

    @property
    def xl(self) -> float:
        return self.__bbox[0]

    @property
    def yt(self) -> float:
        return self.__bbox[1]

    @property
    def xr(self) -> float:
        return self.__bbox[2]

    @property
    def yb(self) -> float:
        return self.__bbox[3]

    @property
    def xc(self) -> float:
        return (self.xl + self.xr) / 2

    @property
    def yc(self) -> float:
        return (self.yt + self.yb) / 2
    
    @property
    def width(self) -> float:
        return self.xr - self.xl

    @property
    def height(self) -> float:
        return self.yb - self.yt
    
    @property
    def area(self) -> float:
        return self.width * self.height
    
    def get_dict(
        self
    ) -> dict[str, Any]:
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
    

class Content:
    def __init__(
        self,
        line: Line,
        id: int,
        number: int,
        text: str,
        bbox: tuple[float, float, float, float],
        origin: tuple[float, float],
        ascender: float,
        descender: float,
        size: float,
        font: str,
        flags: int,
        char_flags: int,
        bidi: int,
        alpha: int,
        rgb_color: int,
        horizontal_end_on_page: int | None = None
    ):
        self.__line = line
        self.__id = id
        self.__number = number
        self.__text = text
        self.__bbox = bbox
        self.__origin = origin
        self.__ascender = ascender
        self.__descender = descender
        self.__size = size
        self.__font = font
        self.__flags = flags
        self.__char_flags = char_flags
        self.__bidi = bidi
        self.__alpha = alpha
        self.__rgb_color = rgb_color
        self.__horizontal_end_on_page = horizontal_end_on_page

    @property
    def line(self) -> Line:
        return self.__line
    
    @property
    def block(self) -> Block:
        return self.line.block

    @property
    def page(self) -> Page:
        return self.block.page
    
    @property
    def id(self) -> int:
        return self.__id
    
    @property
    def number(self) -> int:
        return self.__number

    @property
    def text(self) -> str:
        return self.__text

    # ── geometry ──

    @property
    def bbox(self) -> tuple[float, float, float, float]:
        return self.__bbox
    
    @property
    def origin(self) -> tuple[float, float]:
        return self.__origin

    @property
    def xl(self) -> float:
        return self.__bbox[0]

    @property
    def yt(self) -> float:
        return self.__bbox[1]

    @property
    def xr(self) -> float:
        return self.__bbox[2]

    @property
    def yb(self) -> float:
        return self.__bbox[3]

    @property
    def xc(self) -> float:
        return (self.xl + self.xr) / 2

    @property
    def yc(self) -> float:
        return (self.yt + self.yb) / 2

    @property
    def xo(self) -> float:
        return self.__origin[0]

    @property
    def yo(self) -> float:
        return self.__origin[1]
    
    @property
    def width(self) -> float:
        return self.xr - self.xl

    @property
    def height(self) -> float:
        return self.yb - self.yt
    
    @property
    def area(self) -> float:
        return self.width * self.height

    # ── typography ──

    @property
    def size(self) -> float:
        return self.__size

    @property
    def font(self) -> str:
        return self.__font

    @property
    def flags(self) -> int:
        return self.__flags

    @property
    def char_flags(self) -> int:
        return self.__char_flags

    @property
    def ascender(self) -> float:
        return self.__ascender

    @property
    def descender(self) -> float:
        return self.__descender

    @property
    def bidi(self) -> int:
        return self.__bidi

    @property
    def alpha(self) -> int:
        return self.__alpha

    # ── color ──

    @property
    def rgb_color(self) -> int:
        return self.__rgb_color
    
    # ── position on page ──

    @property
    def horizontal_end_on_page(self) -> int | None:
        return self.__horizontal_end_on_page
    
    @horizontal_end_on_page.setter
    def horizontal_end_on_page(
        self, 
        horizontal_end_on_page: int | None
    ):
        self.__horizontal_end_on_page = horizontal_end_on_page
    
    def get_dict(
        self
    ) -> dict[str, Any]:
        line_dict = self.line.get_dict()
        for key in line_dict.copy():
            if not (
                key.startswith("page_") 
                or key.startswith("block_")
            ):
                line_dict[f"line_{key}"] = line_dict.pop(key)

        return {
            "id": self.id, 
            "number": self.number,
            "text": self.text,
            "xl": self.xl,
            "yt": self.yt,
            "xr": self.xr,
            "yb": self.yb,
            "xc": self.xc,
            "yc": self.yc,
            "xo": self.xo,
            "yo": self.yo,
            "width": self.width,
            "height": self.height,
            "area": self.area,
            "ascender": self.ascender,
            "descender": self.descender,
            "size": self.size,
            "font": self.font,
            "flags": self.flags,
            "char_flags": self.char_flags,
            "bidi": self.bidi,
            "alpha": self.alpha,
            "rgb_color": self.rgb_color, 
            "horizontal_end_on_page": self.horizontal_end_on_page, 
            **line_dict
        }
    

class PDFContents(list[Content]):
    def __init__(
        self,
        contents: list[Content], 
        sorted_by: tuple[str, ...] | None = None, 
        horizontal_end_on_page_by_x: tuple[str, ...] | None = None, 
        is_joined: bool = False
    ):
        super().__init__(contents)

        self.__sorted_by = sorted_by
        self.__horizontal_end_on_page_by_x = horizontal_end_on_page_by_x
        self.__is_joined = is_joined

    @property
    def sorted_by(self) -> tuple[str, ...] | None:
        return self.__sorted_by
    
    @property
    def horizontal_end_on_page_by_x(self) -> tuple[str, ...] | None:
        return self.__horizontal_end_on_page_by_x
    
    @property
    def is_joined(self) -> bool:
        return self.__is_joined

    def copy(self):
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
    ):
        pdf_contents = self.copy()
        pdf_contents.sort(by, use_cache)

        return pdf_contents

    def join(
        self, 
        use_cache: bool = True
    ) -> None:        
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
    ):
        pdf_contents = self.copy()
        pdf_contents.join(use_cache)
    
        return pdf_contents

    def assign_horizontal_end_on_page(
        self, 
        x_delimiters: tuple[float, ...], 
        use_cache: bool = True
    ) -> None:
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
    ):
        pdf_contents = self.copy()
        pdf_contents.assign_horizontal_end_on_page(x_delimiters, use_cache)
    
        return pdf_contents

    def get_contents_from_same_block(
        self, 
        i_ref: int
    ):
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
    ):
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
    ):
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
        self.clear()
        self.extend(new_pdf_contents)

    @staticmethod
    def _is_sequential(content1: Content, content2: Content) -> bool:
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
        content1_block_id = content1.block.id
        content2_block_id = content2.block.id

        return content1_block_id == content2_block_id
    
    @staticmethod
    def _is_same_row(content1: Content, content2: Content, yo_diff_tolerance: float) -> bool:
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
        content_line_id = int(content.line.id)
        previous_content_line_id = int(previous_content.line.id)

        return content_line_id == previous_content_line_id

    @staticmethod
    def _create_content_by_sequential(
        sequencial_contents: list[Content], 
        new_content_id: int
    ) -> Content:
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
