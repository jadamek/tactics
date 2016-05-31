from map import Map
from tile import Tile
import unittest, random, sfml as sf

class TestMap(unittest.TestCase):
    #--------------------------------------------------------------------------------
    def test_map_00_default_initialization(self):
    #--------------------------------------------------------------------------------
        map = Map()
        self.assertEqual(map.width, 10, "Default map should have a recorded width of 10, not " + str(map.width))
        self.assertEqual(map.length, 10, "Default map should have a recorded length of 10, not " + str(map.length))
        self.assertEqual(len(map.tiles_[0]), 10, "Default map should have an actual width of 10, not " + str(len(map.tiles_[0])))
        self.assertEqual(len(map.tiles_), 10, "Default map should have an actual length of 10, not " + str(len(map.tiles_)))

        for x in range(map.width):
            for y in range(map.length):
                self.assertEqual(map.tiles_[y][x], [], "Position [" + str(x) + ", " + str(y) + "] in default map should be an empty array, but is " + str(map.tiles_[y][x]) + " instead")
    
    #--------------------------------------------------------------------------------
    def test_map_01_initialization(self):
    #--------------------------------------------------------------------------------
        # W x L
        width = random.randint(1, 100)
        length = random.randint(1, 100)
        
        map = Map(width, length)
        self.assertEqual(map.width, width, "Default map should have a recorded width of " + str(width) + ", not " + str(map.width))
        self.assertEqual(map.length, length, "Default map should have a recorded length of " + str(length) + ", not " + str(map.length))
        self.assertEqual(len(map.tiles_[0]), width, "Default map should have an actual width of " + str(width) + ", not " + str(len(map.tiles_[0])))
        self.assertEqual(len(map.tiles_), length, "Default map should have an actual length of " + str(length) + ", not " + str(len(map.tiles_)))

        for x in range(map.width):
            for y in range(map.length):
                self.assertEqual(map.tiles_[y][x], [], "Position [" + str(x) + ", " + str(y) + "] in unfilled map should be an empty array, but is " + str(map.tiles_[y][x]) + " instead")
        
        # W x -1
        map = Map(width, -1)
        self.assertEqual(map.width, width, "Default map should have a recorded width of " + str(width) + ", not " + str(map.width))
        self.assertEqual(map.length, 1, "Default map should have a recorded length of 1, not " + str(map.length))
        self.assertEqual(len(map.tiles_[0]), width, "Default map should have an actual width of " + str(width) + ", not " + str(len(map.tiles_[0])))
        self.assertEqual(len(map.tiles_), 1, "Default map should have an actual length of 1, not " + str(len(map.tiles_)))

        for x in range(map.width):
            for y in range(map.length):
                self.assertEqual(map.tiles_[y][x], [], "Position [" + str(x) + ", " + str(y) + "] in unfilled map should be an empty array, but is " + str(map.tiles_[y][x]) + " instead")

        # -1 x -1
        map = Map(-1, -1)
        self.assertEqual(map.width, 1, "Default map should have a recorded width of 1, not " + str(map.width))
        self.assertEqual(map.length, 1, "Default map should have a recorded length of 1, not " + str(map.length))
        self.assertEqual(len(map.tiles_[0]), 1, "Default map should have an actual width of 1, not " + str(len(map.tiles_[0])))
        self.assertEqual(len(map.tiles_), 1, "Default map should have an actual length of 1, not " + str(len(map.tiles_)))

        for x in range(map.width):
            for y in range(map.length):
                self.assertEqual(map.tiles_[y][x], [], "Position [" + str(x) + ", " + str(y) + "] in unfilled map should be an empty array, but is " + str(map.tiles_[y][x]) + " instead")

    #--------------------------------------------------------------------------------
    def test_map_02_place_tile(self):
    #--------------------------------------------------------------------------------
        map = Map(2, 2)
        x = 1
        y = 1
        
        tile1 = Tile(None, 5)
        
        # Placing tiles out-of-bounds
        self.assertFalse(map.place(tile1, -1, 0), "Placing tile at (-1, 0) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.place(tile1, 2, 0), "Placing tile at (2, 0) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.place(tile1, 0, -1), "Placing tile at (0, -1) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.place(tile1, 0, 2), "Placing tile at (0, 2) is out of bounds for 2x2 map, and should return False")
        
        for ix in range(map.width):
            for iy in range(map.length):
                self.assertEqual(map.tiles_[iy][ix], [], "Position [" + str(ix) + ", " + str(iy) + "] in unfilled map should remain an empty array after out-of-bounds placing, but is " + str(map.tiles_[iy][ix]) + " instead")

        # Placing tiles in-bounds
        map.place(tile1, x, y)   
             
        self.assertEqual(len(map.tiles_[y][x]), 1, "Placed a single tile at ("+str(x)+", "+str(y)+"), but length of jagged array for ("+str(x)+", "+str(y)+") is " + str(len(map.tiles_[y][x])) + " instead")
        self.assertEqual(map.tiles_[y][x][0], tile1, "Placed a tile at ("+str(x)+", "+str(y)+"), and front of array at ("+str(x)+", "+str(y)+") should be Tile1, but is " + str(map.tiles_[y][x][0]) + " instead")        
        self.assertEqual(tile1.position, sf.Vector3(1, 1, 0), "Placed a tile at ("+str(x)+", "+str(y)+"), and its position should be (" + str(sf.Vector3(1, 1, 0)) + "), but is (" + str(tile1.position) + ") instead")

        # Placing tiles on top of another
        tile2 = Tile(None, 3)
        map.place(tile2, x, y)   
             
        self.assertEqual(len(map.tiles_[y][x]), 2, "Placed Tile2 on top of Tile1, but length of jagged array for ("+str(x)+", "+str(y)+") is " + str(len(map.tiles_[y][x])) + " instead of 2")
        self.assertEqual(map.tiles_[y][x][1], tile2, "Placed Tile2 on top of Tile1, and second item in array at ("+str(x)+", "+str(y)+") should be Tile2, but is " + str(map.tiles_[y][x][1]) + " instead")
        self.assertEqual(tile1.occupant, tile2, "Placed Tile2 on top of Tile1, and Tile1's occupant should be Tile2, but is " + str(tile1.occupant) + " instead ")
        self.assertEqual(tile2.position, sf.Vector3(1, 1, 5), "Placed Tile2 on top of Tile1, and its position should be (" + str(sf.Vector3(1, 1, 5)) + "), but is (" + str(tile2.position) + ") instead")

if __name__ == "__main__":
    unittest.main(verbosity = 2)