from tile import Tile
import unittest, sfml as sf

class TestTiles(unittest.TestCase):
    #--------------------------------------------------------------------------------
    def test_00_tile_initialization(self):
    #--------------------------------------------------------------------------------
        tile = Tile()
        pass
        
if __name__ == "__main__":
    unittest.main(verbosity = 2)