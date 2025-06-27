#!/usr/bin/python
##-------------------------------##
## Assembly Line: Editor         ##
## Written By: Ryan Smith        ##
##-------------------------------##
## Manager                       ##
##-------------------------------##

## Imports
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any
from .chunk import Chunk
from .entity import (
    Entity,
    CrafterComponent, ProducerComponent, QueueComponent, TransporterComponent,
)
from .floor import Floor
from .world import World


## Functions
def load_floor(path: Path) -> Floor:
    """
    """
    # -Internal Functions
    def _build_inventory(entity_data: dict[str, Any]) -> set[tuple[int, int]]:
        '''
        '''
        inventory = set()
        for resource in entity_data['Inventory']['Resources']:
            inventory.add((resource['ResourceType'], resource['Quantity']))
        return inventory
    def _build_queue(entity_data: dict[str, Any]) -> list[tuple[int, int]]:
        '''
        '''
        current = None
        queue = []
        for resource in entity_data['Queue']["Resources"]:
            resource_id = resource['ResourceType']
            if current is None:
                current = [resource_id, 1]
            elif resource_id != current[0]:
                queue.append(tuple(current))
                current = [resource_id, 1]
            else:
                current[1] += 1
        if current is not None:
            queue.append(tuple(current))
        return queue
    # -Body
    floor = Floor()
    # --Chunks
    with open(path / "spaces.json") as f:
        chunks = json.load(f)
    for y, x_chunks in enumerate(chunks):
        for x, enabled in enumerate(x_chunks):
            if not bool(enabled):
                continue
            floor.enable_chunk(x, y)
    # --Starters
    for entity, data in _load_entities(path / "starters.json", floor):
        entity.component = ProducerComponent(data['ResourceType'])
    # --Importers
    for entity, data in _load_entities(path / "importers.json", floor):
        entity.component = ProducerComponent(data['Resource'], data['SelectedTime'])
    # --Rollers
    all(_load_entities(path / "rollers.json", floor))
    # --Sellers
    all(_load_entities(path / "sellers.json", floor))
    # --TODO: Selectors
    for entity, data in _load_entities(path / "selectors.json", floor):
        print(data)
    # --Transporters
    for entity, data in _load_entities(path / "transporter_inputs.json", floor):
        entity.component = TransporterComponent(data['TransporterLineId'])
    for entity, data in _load_entities(path / "transporter_outputs.json", floor):
        entity.component = TransporterComponent(data['TransporterLineId'])
    # --Splitters[Basic]
    all(_load_entities(path / "splitters.json", floor))
    # --Splitters[Advanced]
    # --Splitters[Timer]
    # --Transformers[Basic]
    for entity, data in _load_entities(path / "transformers.json", floor):
        queue = _build_queue(data)
        entity.component = QueueComponent(queue)
    # --Transformers[Advanced]
    for entity, data in _load_entities(path / "quantity_transformers.json", floor):
        queue = _build_queue(data)
        entity.component = QueueComponent(queue)
    # --Crafters[Basic]
    for entity, data in _load_entities(path / "crafters.json", floor):
        resource = data['BlueprintResult'] if data['BlueprintResult'] >= 0 else None
        inventory = _build_inventory(data)
        entity.component = CrafterComponent(resource, inventory)
    # --Crafters[Advanced]
    for entity, data in _load_entities(path / "radioactive_crafters.json", floor):
        resource = data['BlueprintResult'] if data['BlueprintResult'] >= 0 else None
        inventory = _build_inventory(data)
        entity.component = CrafterComponent(resource, inventory, data['Energy'])
    return floor


def _load_entities(file: Path, floor: Floor) -> Iterable[Entity, dict[str, Any]]:
    """
    """
    # -Internal Functions
    def _load_entity(entity_dict: dict[str, Any]) -> Entity:
        entity = Entity(entity_dict['Type'], entity_dict['Direction'])
        x, y = (int(i) for i in entity_dict['Position'])
        offset_x, offset_y = (x % Chunk.Size, y % Chunk.Size)
        chunk = floor.get_chunk_from_world_coordinates(x, y)
        chunk[offset_x, offset_y] = entity
        return entity
    # -Body
    with open(file) as f:
        for entity_data in json.load(f):
            yield (_load_entity(entity_data), entity_data)
