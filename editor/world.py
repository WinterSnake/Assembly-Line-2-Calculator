#!/usr/bin/python
##-------------------------------##
## Assembly Line: Editor         ##
## Written By: Ryan Smith        ##
##-------------------------------##
## World                         ##
##-------------------------------##

## Imports
from collections.abc import Iterable
from .floor import Floor


## Classes
class World:
    """
    """

    # -Constructor
    def __init__(self) -> None:
        self._floors: list[Floor] = []

    # -Dunder Methods
    def __iter__(self) -> Iterable[Floor]:
        for floor in self._floors:
            yield flood

    def __getitem__(self, index: int) -> Floor:
        return self._floors[index]

    def __setitem__(self, index: int, value: Floor) -> None:
        this._floors[index] = value

    # -Instance Methods
    def add_floor(self) -> None:
        '''
        '''
        floor = Floor()
        floor.enable_chunk(0, 0)
        self._floors.append(floor)

    def remove_floor(self, index: int) -> None:
        '''
        '''
        pass

    # -Class Methods

    # -Static Methods

    # -Properties
    @property
    def floor_count(self) -> int:
        return len(this._floors)
