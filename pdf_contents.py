import fitz
from typing import Any
from statistics import mode


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
        ascender: float | None, 
        descender: float | None, 
        size: float | None, 
        font: str | None, 
        flags: int | None, 
        char_flags: int | None, 
        bidi: int | None, 
        alpha: int | None, 
        rgb_color: int | None
    ):
        self.__line = line
        self.__id = id
        self.__number = number
        self.__text = text
        self.__bbox = bbox
        self.__origin = origin
        self.__size = size
        self.__font = font
        self.__flags = flags
        self.__char_flags = char_flags
        self.__ascender = ascender
        self.__descender = descender
        self.__bidi = bidi
        self.__alpha = alpha
        self.__rgb_color = rgb_color

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
    def size(self) -> float | None:
        return self.__size

    @property
    def font(self) -> str | None:
        return self.__font

    @property
    def flags(self) -> int | None:
        return self.__flags

    @property
    def char_flags(self) -> int | None:
        return self.__char_flags

    @property
    def ascender(self) -> float | None:
        return self.__ascender

    @property
    def descender(self) -> float | None:
        return self.__descender

    @property
    def bidi(self) -> int | None:
        return self.__bidi

    @property
    def alpha(self) -> int | None:
        return self.__alpha

    # ── color ──

    @property
    def rgb_color(self) -> int | None:
        return self.__rgb_color
    
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
            "size": self.size,
            "font": self.font,
            "flags": self.flags,
            "char_flags": self.char_flags,
            "ascender": self.ascender,
            "descender": self.descender,
            "bidi": self.bidi,
            "alpha": self.alpha,
            "rgb_color": self.rgb_color,
            **line_dict
        }
    

class PDFContents(list[Content]):
    def __init__(
        self,
        contents: list[Content], 
        is_sorted: bool = False, 
        is_joined_by_line: bool = False, 
        is_joined_by_sequential: bool = False, 
        is_page_side_assigned: bool = False
    ):
        super().__init__(contents)

        self.__is_sorted = is_sorted
        self.__is_joined_by_line = is_joined_by_line
        self.__is_joined_by_sequential = is_joined_by_sequential
        self.__is_page_side_assigned = is_page_side_assigned

    @property
    def is_sorted(self) -> bool:
        return self.__is_sorted
    
    @property
    def is_joined_by_line(self) -> bool:
        return self.__is_joined_by_line
    
    @property
    def is_joined_by_sequential(self) -> bool:
        return self.__is_joined_by_sequential
    
    @property
    def is_page_side_assigned(self) -> bool:
        return self.__is_page_side_assigned

    def copy(self):
        return PDFContents(
            self, 
            self.is_sorted, 
            self.is_joined_by_line, 
            self.is_joined_by_sequential
        )
    
    def sort(
        self, 
        use_cache: bool = True
    ) -> None:
        if use_cache and self.__is_sorted:
            return
        
        super().sort(key=lambda v: (v.page.number, v.yo, v.xo, v.block.id, v.line.id))

        self.__is_sorted = True

    def sorted(
        self, 
        use_cache: bool = True
    ):
        pdf_contents = self.copy()
        return pdf_contents.sort(use_cache)

    def join(
        self, 
        by: str = "line", 
        use_cache: bool = True
    ) -> None:
        if not self._is_invalid_by(by):
            raise ValueError(f"Invalid 'by' argument: {by}")
        
        self.sort()
        if by == "line":
            if use_cache and self.__is_joined_by_line:
                return 
            
            joined_pdf_contents = self._join_by_lines()
            self._replace_contents(joined_pdf_contents)

            self.__is_joined_by_line = True

        elif by == "sequential":            
            if use_cache and self.__is_joined_by_sequential:
                return 
            
            joined_pdf_contents = self._join_by_sequential()
            self._replace_contents(joined_pdf_contents)

            self.__is_joined_by_sequential = True

    def joined(
        self, 
        by: str = "line", 
        use_cache: bool = True
    ):
        pdf_contents = self.copy()
        return pdf_contents.join(by, use_cache)
    
    def get_contents_from_block(
        self, 
        i_ref: int
    ):
        # Descovering the first content of the block
        i = i_ref
        while self._is_same_block(self[i], self[i - 1]):
            i -= 1

        contents_from_same_block = [self[i]]

        i += 1
        # Extracting contents
        while self._is_same_block(self[i], self[i - 1]):
            contents_from_same_block.append(self[i])
            i += 1

        return PDFContents(contents_from_same_block)

    def assign_page_side(
        self, 
        x_delimiter: float, 
        use_cache: bool = True
    ) -> None:
        if use_cache and self.__is_page_side_assigned:
            return
        
        pass

    def get_line(
        self, 
        count_reference: int
    ):
        pass

    def _replace_contents(
        self, 
        new_pdf_contents: list[Content]
    ) -> None:
        self.clear()
        self.extend(new_pdf_contents)

    def _join_by_lines(self):
        joined_pdf_contents = []
        
        new_content_id = 0 
        i = 0
        while i < len(self):
            sequencial_contents = [self[i]]

            j = i + 1
            while (
                j < len(self)
                and self._is_same_line(self[j], self[j - 1])
            ):
                sequencial_contents.append(self[j])
                j += 1

            content = self._create_content_by_sequential(
                sequencial_contents, 
                new_content_id, 
                by="line"
            )

            joined_pdf_contents.append(content)
            
            i = j
            new_content_id += 1

        return PDFContents(joined_pdf_contents)
    
    def _join_by_sequential(self):
        joined_pdf_contents = []

        return PDFContents(joined_pdf_contents)

    @staticmethod
    def _is_same_line(content: Content, previous_content: Content) -> bool:
        content_line_id = int(content.line.id)
        previous_content_line_id = int(previous_content.line.id)

        return content_line_id == previous_content_line_id
    
    @staticmethod
    def _is_same_block(content: Content, previous_content: Content) -> bool:
        content_block_id = int(content.line.block.id)
        previous_content_block_id = int(previous_content.line.block.id)

        return content_block_id == previous_content_block_id
    
    @staticmethod
    def _is_sequential(content: Content, previous_content: Content) -> bool:
        content_line_id = int(content.line.id)
        previous_content_line_id = int(previous_content.line.id)
        
        pass

    @staticmethod
    def _create_content_by_sequential(
        sequencial_contents: list[Content], 
        new_content_id: int, 
        by: str = "line"
    ) -> Content:
        joined_content_line = sequencial_contents[0].line

        if by == "line":
            joined_content_bbox = sequencial_contents[0].line.bbox
        else:
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
        joined_content_size = (
            sequencial_contents[0].size 
            if all(
                content.size == sequencial_contents[0].size
                for content in sequencial_contents
            )
            else None
        )
        joined_content_font = (
            sequencial_contents[0].font 
            if all(
                content.font == sequencial_contents[0].font
                for content in sequencial_contents
            )
            else None
        )
        joined_content_flags = (
            sequencial_contents[0].flags 
            if all(
                content.flags == sequencial_contents[0].flags
                for content in sequencial_contents
            )
            else None
        )
        joined_content_char_flags = (
            sequencial_contents[0].char_flags 
            if all(
                content.char_flags == sequencial_contents[0].char_flags
                for content in sequencial_contents
            )
            else None
        )
        joined_content_bidi = (
            sequencial_contents[0].bidi 
            if all(
                content.bidi == sequencial_contents[0].bidi
                for content in sequencial_contents
            )
            else None
        )
        joined_content_alpha = (
            sequencial_contents[0].alpha 
            if all(
                content.alpha == sequencial_contents[0].alpha
                for content in sequencial_contents
            )
            else None
        )
        joined_content_rgb_color = (
            sequencial_contents[0].rgb_color 
            if all(
                content.rgb_color == sequencial_contents[0].rgb_color
                for content in sequencial_contents
            )
            else None
        )

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
            joined_content_rgb_color
        )
    
    @staticmethod
    def _is_invalid_by(by: str) -> bool:
        valid_by = ["line", "sequential"]
        return by in valid_by
