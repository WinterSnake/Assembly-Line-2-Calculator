#!/usr/bin/python
##-------------------------------##
## Assembly Line: Editor         ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Chunk                         ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Iterable
from typing import ClassVar
from .entity import Entity


## Classes
class Chunk:
    """
    Assembly Line 2 Floor Chunk
        10x10 floor segment
    """

    # -Constructor
    def __init__(self, x_offset: int, y_offset: int) -> None:
        self.offset: tuple[int, int] = (x_offset, y_offset)
        self._tiles: list[list[Entity | None]] = [
            [None for x in range(Chunk.Size)]
            for y in range(Chunk.Size)
        ]

    # -Dunder Methods
    def __iter__(self) -> Iterable[Entity]:
        for x_tiles in self._tiles:
            for tile in x_tiles:
                if tile is None:
                    continue
                yield tile

    def __getitem__(self, position: tuple[int, int]) -> None:
        x, y = position
        return self._tiles[x][y]

    def __setitem__(self, position: tuple[int, int], value) -> None:
        x, y = position
        self._tiles[x][y] = value

    def __str__(self) -> str:
        return f"Chunk[{self.x}, {self.y}]"

    # -Properties
    @property
    def x(self) -> int:
        return self.offset[0]

    @property
    def x_offset(self) -> int:
        return self.offset[0] * Chunk.Size

    @property
    def y(self) -> int:
        return self.offset[1]

    @property
    def y_offset(self) -> int:
        return self.offset[1] * Chunk.Size

    # -Class Properties
    Size: ClassVar[int] = 10
