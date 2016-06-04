import unittest

#--- Tests: Map -----------------------------------------------
from map.test_tile import TestTiles
from map.test_map import TestMap
from container.test_zlist import TestZList
from sprite.map.test_sprite_tile import TestSpriteTiles

if __name__ == "__main__":
	unittest.main(verbosity = 2)