from map import Map
from tile import Tile
import unittest

class TestTiles(unittest.TestCase):
    #--------------------------------------------------------------------------------
    def test_00_map_initialization(self):
    #--------------------------------------------------------------------------------
        tile = Map()
        pass
        
if __name__ == "__main__":
    unittest.main(verbosity = 2)