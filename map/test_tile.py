from tile import Tile
import unittest, random

class TestTiles(unittest.TestCase):
    #--------------------------------------------------------------------------------
    def test_00_tile_initialization(self):
    #--------------------------------------------------------------------------------
        tile = Tile()
        self.assertEqual(tile.height, 1.0, "Tile height improperly default initialized as: " + str(tile.height) + "; should be 1.0.")
        
        tile = Tile(None, -10)
        self.assertEqual(tile.height, 0.0, "Tile height improperly initialized as: " + str(tile.height) + "; should be 0.0")
        
        tile = Tile(None, 10)
        self.assertEqual(tile.height, 10.0, "Tile height improperly initialized as: " + str(tile.height) + "; should be 10")
        
    #--------------------------------------------------------------------------------
    def test_01_raise_tile(self):
    #--------------------------------------------------------------------------------
        tile1 = Tile()
        tile2 = Tile()
        tile3 = Tile()
        
        base = random.randint(1, 1000)
        tile1.rise(base)
        self.assertEqual(tile1.position.z, base, "Rose Tile1 from 0 => " + str(base) + ", but currently lies at: " + str(tile1.position.z))
        self.assertEqual(tile2.position.z, 0.0, "Tile2 somehow changed position during tile1 rising. Now lies at: " + str(tile2.position.z))
                
        tile1.occupant = tile2
        tile2.occupant = tile3
        
        level1 = random.randint (1, 1000)    
        tile1.rise(level1)
        self.assertEqual(tile1.position.z, base + level1, "Raising Tile1 from " + str(base) + " => " + str(base + level1) + ", but currently lies at: " + str(tile1.position.z))
        self.assertEqual(tile2.position.z, level1, "Raising Tile1 from " + str(base) + " => " + str(base + level1) + ", which should raise Tile2 0 => " + str(level1) + ", but instead currently lies at: " + str(tile2.position.z))
        self.assertEqual(tile3.position.z, level1, "Raising Tile1 from " + str(base) + " => " + str(base + level1) + ", which should raise Tile3 0 => " + str(level1) + ", but instead currently lies at: " + str(tile3.position.z))
        
        level2 = random.randint (1, 1000)
        tile2.rise(level2)
        self.assertEqual(tile1.position.z, base + level1, "Tile1 somehow changed position during tile2 rising. Now lies at: " + str(tile1.position.z))
        self.assertEqual(tile2.position.z, level1 + level2, "Rose Tile2 from " + str(level1) + " => " + str(level1 + level2) + ", but currently lies at: " + str(tile2.position.z))
        self.assertEqual(tile3.position.z, level1 + level2, "Raising Tile2 from " + str(level1) + " => " + str(level1 + level2) + ", which should raise Tile3 from " + str(level1) + " => " + str(level1 + level2) + ", but instead currently lies at: " + str(tile3.position.z))
        
        level3 = random.randint (1, 1000)
        tile3.rise(level3)
        self.assertEqual(tile1.position.z, base + level1, "Tile1 somehow changed position during tile3 rising. Now lies at: " + str(tile1.position.z))
        self.assertEqual(tile2.position.z, level1 + level2, "Tile2 somehow changed position during tile3 rising. Now lies at: " + str(tile2.position.z))
        self.assertEqual(tile3.position.z, level1 + level2 + level3, "Rose Tile3 from " + str(level1 + level2) + " => " + str(level1 + level2 + level3) + ", but currently lies at: " + str(tile3.position.z))
        
if __name__ == "__main__":
    unittest.main(verbosity = 2)