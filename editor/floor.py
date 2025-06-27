#!/usr/bin/python
##-------------------------------##
## Assembly Line: Editor         ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Floor                         ##
##-------------------------------##

## Imports
from __future__ import annotations
from collections.abc import Iterable
from typing import ClassVar
from .chunk import Chunk


## Classes
class Floor:

    # -Constructor
    def __init__(self) -> None:
        self._chunks: list[list[Chunk]] = [
            [None for x in range(Floor.Size)]
            for y in range(Floor.Size)
        ]

    # -Dunder Methods
    def __iter__(self) -> Iterable[Entity]:
        for x_chunks in self._chunks:
            for chunk in x_chunks:
                if chunk is None:
                    continue
                yield chunk

    def __getitem__(self, position: tuple[int, int]) -> Chunk:
        x, y = position
        return self._chunks[x][y]

    def __setitem__(self, position: tuple[int, int], value: Chunk) -> None:
        x, y = position
        value.offset = position
        self._chunks[x][y] = value

    # -Instance Methods
    def enable_chunk(self, x: int, y: int) -> None:
        self._chunks[x][y] = Chunk(x, y)

    def get_chunk_from_world_coordinates(self, x: int, y: int) -> Chunk:
        '''
        '''
        chunk_x, chunk_y = (x // Chunk.Size, y // Chunk.Size)
        return self._chunks[chunk_x][chunk_y]

    def disable_chunk(self, x: int, y: int) -> None:
        self._chunks[x][y] = None

    # -Properties
    @property
    def chunk_count(self) -> int:
        count: int = 0
        for x_chunks in self._chunks:
            for chunk in x_chunks:
                if chunk is None:
                    continue
                count += 1
        return count

    # -Class Properties
    Size: ClassVar[int] = 10
