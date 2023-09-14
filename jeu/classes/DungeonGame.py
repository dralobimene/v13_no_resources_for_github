
import math
from classes.DungeonGenerator import DungeonGenerator
# from classes.MapPartition import MapPartition


class DungeonGame:
    def __init__(self, width, height):
        self.width, self.height = (math.trunc(width / 16), math.trunc(height / 16))
        self.dungeon_generator = DungeonGenerator()

    def create_map(self):
        dm, mp = self.dungeon_generator.generate_map(self.width, self.height, 3)
        return dm, self.width, mp

    def generate_next_map(self):
        return self.create_map()
