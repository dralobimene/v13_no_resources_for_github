import random
import math

from classes.Room import Room
from classes.Path import Path
from classes.DivideDirection import DivideDirection
from classes.TileTypes import TileTypes
from classes.MapPartition import MapPartition


class DungeonGenerator:
    def __init__(self):
        self.tile_dict = None

    def __write_room_to_map(self, map: list, map_width: int, room: Room) -> list:
        if room is None:
            return map
        map_height = math.trunc(len(map) / map_width)
        for y in range(room.height):
            for x in range(room.width):
                map_x = x + room.x
                map_y = y + room.y
                if (map_x < 0 or map_x >= map_width):
                    continue
                if (map_y < 0 or map_y >= map_height):
                    continue
                map_i = self.index_from_coordinates(map_x, map_y, map_width)
                map[map_i] = self.tile_dict.get(TileTypes.FLOOR)

    def __write_path_to_map(self, map: list, map_width: int, path: Path) -> list:
        if path is None:
            return map
        map_height = math.trunc(len(map) / map_width)
        for x, y in path.path:
            if x < 0 or x >= map_width:
                continue
            if y < 0 or y >= map_height:
                continue
            map_i = self.index_from_coordinates(x, y, map_width)
            map[map_i] = self.tile_dict.get(TileTypes.PATH)

    def __write_partitions_to_map(self, map: list, map_width: int, partition: MapPartition) -> list:
        self.__recurse_partition_to_map(map, map_width, partition)

    def __recurse_partition_to_map(self, map: list, map_width: int, partition: MapPartition) -> MapPartition:
        if partition.room is not None:
            self.__write_room_to_map(map, map_width, partition.room)
        if partition.path is not None:
            self.__write_path_to_map(map, map_width, partition.path)
        if partition.children[0] is not None:
            self.__recurse_partition_to_map(map, map_width, partition.children[0])
        if partition.children[1] is not None:
            self.__recurse_partition_to_map(map, map_width, partition.children[1])

    def __create_partitions(self, x: int, y: int, width: int, height: int, divisions: int) -> MapPartition:
        partition = MapPartition(x, y, width, height)
        self.__recurse_partitions(partition, divisions)
        return partition

    def __recurse_partitions(self, partition: MapPartition, divisions: int) -> None:
        if divisions == 0:
            partition.create_room() # create a room in each of the final level partitions
            partition.create_key_point() # create a key point in each room to ensure accessibility
            return
        aspect_ratio = partition.width / partition.height
        divide_direction = DivideDirection(1) if aspect_ratio > 1 else DivideDirection(2)
        if aspect_ratio == 1:
            divide_direction = DivideDirection(random.randint(1, 2))
        partition_1, partition_2 = partition.create_children(divide_direction)
        if partition_1 is not None:
            self.__recurse_partitions(partition_1, divisions - 1)
        if partition_2 is not None:
            self.__recurse_partitions(partition_2, divisions - 1)
        partition.create_path_between_children()
        partition.create_key_point()

    def generate_default_tile_dict(self) -> dict:
        self.tile_dict = {
            TileTypes.EMPTY: 0,
            TileTypes.FLOOR: 1,
            TileTypes.PATH: 2,
            # TileTypes.WALL: 3,
            # TileTypes.DOOR: 4
        }
        return self.tile_dict

    def generate_map(self, width: int, height: int, divisions: int = 4) -> list:
        if (self.tile_dict is None):
            self.generate_default_tile_dict()
        generated_map = [self.tile_dict.get(TileTypes.EMPTY)]*(width * height)
        map_partitions = self.__create_partitions(0, 0, width, height, divisions)
        self.__write_partitions_to_map(generated_map, width, map_partitions)
        return (generated_map, map_partitions)

    def index_from_coordinates(self, x: int, y: int, width: int) -> int:
        return int(x + math.trunc(y * width))

    def coordinates_from_index(self, i: int, width: int) -> tuple:
        return (i % width, math.trunc(i / width))
