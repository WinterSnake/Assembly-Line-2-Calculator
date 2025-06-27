#!/usr/bin/python
##-------------------------------##
## Assembly Line: Editor         ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Entity                        ##
##-------------------------------##

## Imports
from __future__ import annotations
from abc import ABC, abstractmethod

## Constants
SplitterCounter = tuple[int, int, int] | tuple[float, float, float]


## Classes
class Entity:
    """Assembly Line Tile Entity"""

    # -Constructor
    def __init__(self, _id: int, direction: int = 0) -> None:
        self.id: int = _id
        self.direction: int = direction
        self.component: EntityComponent | None = None

    # -Dunder Methods
    def __repr__(self) -> str:
        _str = f"Entity(id={self.id}, direction={self.direction}"
        if self.component is not None:
            _str += ", component=" + repr(self.component)
        return _str + ')'


class EntityComponent(ABC):
    """"""
    pass


class CrafterComponent(EntityComponent):
    """Entity component for crafters (basic/advanced)"""

    # -Constructor
    def __init__(
        self, resource_id: int | None, inventory: set[tuple[int, int]],
        energy: float | None = None
    ) -> None:
        self.resource_id: int | None = resource_id
        self.inventory: set[tuple[int, int]] = inventory
        self.energy: float | None = energy

    # -Dunder Methods
    def __repr__(self) -> str:
        _str: str = f"CrafterComponent(output={self.resource_id}, inventory={self.inventory}"
        if self.energy is not None:
            _str += f", energy={self.energy}"
        return _str + ')'


class ProducerComponent(EntityComponent):
    """Entity component for producers (starter/importer)"""

    # -Constructor
    def __init__(self, resource_id: int | None, timer: float | None = None) -> None:
        self.resource_id: int | None = resource_id
        self.timer: float | None = timer  # -Importer only

    # -Dunder Methods
    def __repr__(self) -> str:
        _str: str = f"ProducerComponent(resource={self.resource_id}"
        if self.timer is not None:
            _str += f", timer={self.timer}"
        return _str + ')'


class TransporterComponent(EntityComponent):
    """Entity component for transporters (inputs/outputs)"""

    # -Constructor
    def __init__(self, _id: int) -> None:
        self.id: int = _id

    # -Dunder Methods
    def __repr__(self) -> str:
        return f"TransporterComponent(id={self.id})"


class QueueComponent(EntityComponent):
    """Entity component for transformers (cutter/press/etc)"""

    # -Constructor
    def __init__(self, queue: list[tuple[int, int]]) -> None:
        self.queue: list[tuple[int, int]] = queue

    # -Dunder Methods
    def __repr__(self) -> str:
        return f"QueueComponent({self.queue})"
