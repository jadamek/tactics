from map import Map
from tile import Tile
import unittest, random, sfml as sf
from numpy import arange

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
        
        # Placing tiles out of bounds
        self.assertFalse(map.place(tile1, -1, 0), "Placing tile at (-1, 0) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.place(tile1, 2, 0), "Placing tile at (2, 0) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.place(tile1, 0, -1), "Placing tile at (0, -1) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.place(tile1, 0, 2), "Placing tile at (0, 2) is out of bounds for 2x2 map, and should return False")
        
        for ix in range(map.width):
            for iy in range(map.length):
                self.assertEqual(map.tiles_[iy][ix], [], "Position [" + str(ix) + ", " + str(iy) + "] in unfilled map should remain an empty array after out-of-bounds placing, but is " + str(map.tiles_[iy][ix]) + " instead")

        # Placing tiles in bounds
        self.assertTrue(map.place(tile1, x, y), "Placing tile at (" + str(x) + ", " + str(y) + ") should succeed and return True")
             
        self.assertEqual(len(map.tiles_[y][x]), 1, "Placed a single tile at ("+str(x)+", "+str(y)+"), but length of jagged array for ("+str(x)+", "+str(y)+") is " + str(len(map.tiles_[y][x])) + " instead")
        self.assertEqual(map.tiles_[y][x][0], tile1, "Placed a tile at ("+str(x)+", "+str(y)+"), and front of array at ("+str(x)+", "+str(y)+") should be Tile1, but is " + str(map.tiles_[y][x][0]) + " instead")        
        self.assertEqual(tile1.position, sf.Vector3(1, 1, 0), "Placed a tile at ("+str(x)+", "+str(y)+"), and its position should be (" + str(sf.Vector3(1, 1, 0)) + "), but is (" + str(tile1.position) + ") instead")

        # Placing tiles on top of another
        tile2 = Tile(None, 3)
        self.assertTrue(map.place(tile2, x, y), "Placing tile at (" + str(x) + ", " + str(y) + ") should succeed and return True")
             
        self.assertEqual(len(map.tiles_[y][x]), 2, "Placed Tile2 on top of Tile1, but length of jagged array for ("+str(x)+", "+str(y)+") is " + str(len(map.tiles_[y][x])) + " instead of 2")
        self.assertEqual(map.tiles_[y][x][1], tile2, "Placed Tile2 on top of Tile1, and second item in array at ("+str(x)+", "+str(y)+") should be Tile2, but is " + str(map.tiles_[y][x][1]) + " instead")
        self.assertEqual(tile1.occupant, tile2, "Placed Tile2 on top of Tile1, and Tile1's occupant should be Tile2, but is " + str(tile1.occupant) + " instead ")
        self.assertEqual(tile2.position, sf.Vector3(1, 1, 5), "Placed Tile2 on top of Tile1, and its position should be (" + str(sf.Vector3(1, 1, 5)) + "), but is (" + str(tile2.position) + ") instead")

    #--------------------------------------------------------------------------------
    def test_map_03_get_tile_at_position(self):
    #--------------------------------------------------------------------------------
        map = Map(2, 2)
        x = 1
        y = 1
        
        # Grabbing tiles out of bounds
        self.assertFalse(map.at(-1, 0), "Grabbing tile at (-1, 0) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.at(2, 0), "Grabbing tile at (2, 0) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.at(0, -1), "Grabbing tile at (0, -1) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.at(0, 2), "Grabbing tile at (0, 2) is out of bounds for 2x2 map, and should return False")

        for ix in range(map.width):
            for iy in range(map.length):
                self.assertFalse(map.at(ix, iy), "Position [" + str(ix) + ", " + str(iy) + "] in unfilled map should be an empty array and thus return False")
                
        # Setup map of three stacked tiles 
        tile1 = Tile(None, 5)
        tile2 = Tile(None, 3)
        tile3 = Tile(None, 2)
        
        map.place(tile1, x, y)
        map.place(tile2, x, y)
        map.place(tile3, x, y)
        
        self.assertEqual(map.at(x, y), tile3, "Unspecified z-coordinate should return top-most tile.")
        self.assertEqual(map.at(x, y, -1), tile1, "Lower than floor level (0) z should return floor tile")
        self.assertEqual(map.at(x, y, 11), tile3, "Higher z than top-most tile should return top-most tile")
        
        for z in range(6):
            self.assertEqual(map.at(x, y, z), tile1, "Z-level of " + str(z) + " is within 0-5, and should return floor Tile1")
        for z in range(6, 9):
            self.assertEqual(map.at(x, y, z), tile2, "Z-level of " + str(z) + " is within 6-8, and should return floor Tile2")
        for z in range(9, 11):
            self.assertEqual(map.at(x, y, z), tile3, "Z-level of " + str(z) + " is within 9-10, and should return floor Tile3")
            
    #--------------------------------------------------------------------------------
    def test_map_04_insert_tile(self):
    #--------------------------------------------------------------------------------
        map = Map(2, 2)
        x = 1
        y = 1
        
        tile = Tile(None, 10)
                       
        # Inserting tiles out of bounds
        self.assertFalse(map.insert(tile, -1, 0, 0), "Inserting tile at (-1, 0, 0) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.insert(tile, 2, 0, 0), "Inserting tile at (2, 0, 0) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.insert(tile, 0, -1, 0), "Inserting tile at (0, -1, 0) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.insert(tile, 0, 2, 0), "Inserting tile at (0, 2, 0) is out of bounds for 2x2 map, and should return False")

        for ix in range(map.width):
            for iy in range(map.length):
                self.assertFalse(map.insert(tile, ix, iy, 0), "Position [" + str(ix) + ", " + str(iy) + "] in unfilled map should be an empty array and thus return False")
                            
        # Setup map of three stacked tiles 
        tile1 = Tile(None, 5)
        tile2 = Tile(None, 3)
        tile3 = Tile(None, 2)
        
        map.place(tile1, x, y)
        map.place(tile2, x, y)
        map.place(tile3, x, y)
        
        self.assertFalse(map.insert(tile, x, y, -1), "Inserting tile at (" + str(ix) + ", " + str(iy) + ", -1) is out of bounds for 2x2x3 column, and should return False")
        self.assertFalse(map.insert(tile, x, y, 3), "Inserting tile at (" + str(ix) + ", " + str(iy) + ", 3) is out of bounds for 2x2x3 column, and should return False")
        
        # Insert on bottom
        tile4 = Tile(None, 8)
        self.assertTrue(map.insert(tile4, x, y, 0), "Inserting tile at (" + str(x) + ", " + str(y) + ", 1) should succeed and return True")
        
        self.assertEqual(len(map.tiles_[y][x]), 4, "Inserted tile under 3-tile stack at (" + str(ix) + ", " + str(iy) + "), but stack is " + str(len(map.tiles_[y][x])) + " tiles long, not 4")
        self.assertEqual(map.tiles_[y][x][0], tile4, "Inserted tile at layer 0, but found " + str(map.tiles_[y][x][0]) + " there instead")
        self.assertEqual(tile4.occupant, tile1, "Inserted Tile4 under Tile1, but Tile4's occupant is not Tile1")
        self.assertEqual(tile3.position.z, 16, "Inserted Tile4 at bottom of stack, but top tile did not rise by " + str(tile4.get_height()) + ", and is at " + str(tile3.position.z) + " instead")
        
        tile5 = Tile(None, 10)
        
        # Insert Tile5 under Tile2 and Tile3, and above Tile4 and Tile1
        self.assertTrue(map.insert(tile5, x, y, 2), "Inserting tile at (" + str(x) + ", " + str(y) + ", 1) should succeed and return True")
        
        self.assertEqual(len(map.tiles_[y][x]), 5, "Inserted tile into 4-tile stack at (" + str(ix) + ", " + str(iy) + "), but stack is " + str(len(map.tiles_[y][x])) + " tiles long, not 5")
        self.assertEqual(map.tiles_[y][x][2], tile5, "Inserted tile at layer 2, but found " + str(map.tiles_[y][x][2]) + " there instead")
        self.assertEqual(tile5.occupant, tile2, "Inserted Tile5 under Tile2, but Tile5's occupant is not Tile2")
        self.assertEqual(tile1.occupant, tile5, "Inserted Tile5 above Tile1, but Tile1's occupant is not Tile5")
        self.assertEqual(tile3.position.z, 26, "Inserted Tile5 at bottom of stack, but top tile did not rise by " + str(tile.get_height()) + ", and is at " + str(tile3.position.z) + " instead")
        
    #--------------------------------------------------------------------------------
    def test_map_05_replace_tile(self):
    #--------------------------------------------------------------------------------
        map = Map(2, 2)
        x = 1
        y = 1
        
        tile = Tile(None, 10)
                       
        # Replacing tiles out of bounds
        self.assertFalse(map.replace(tile, -1, 0, 0), "Replacing tile at (-1, 0, 0) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.replace(tile, 2, 0, 0), "Replacing tile at (2, 0, 0) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.replace(tile, 0, -1, 0), "Replacing tile at (0, -1, 0) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.replace(tile, 0, 2, 0), "Replacing tile at (0, 2, 0) is out of bounds for 2x2 map, and should return False")

        for ix in range(map.width):
            for iy in range(map.length):
                self.assertFalse(map.replace(tile, ix, iy, 0), "Position [" + str(ix) + ", " + str(iy) + "] in unfilled map should be an empty array and thus return False")
                            
        # Setup map of three stacked tiles 
        tile1 = Tile(None, 5)
        tile2 = Tile(None, 3)
        tile3 = Tile(None, 2)
        
        map.place(tile1, x, y)
        map.place(tile2, x, y)
        map.place(tile3, x, y)
        
        self.assertFalse(map.replace(tile, x, y, -1), "Replacing tile at (" + str(ix) + ", " + str(iy) + ", -1) is out of bounds for 2x2x3 column, and should return False")
        self.assertFalse(map.replace(tile, x, y, 3), "Replacing tile at (" + str(ix) + ", " + str(iy) + ", 3) is out of bounds for 2x2x3 column, and should return False")
               
        tile5 = Tile(None, 1)
        
        # Replace middle tile (Tile2)
        self.assertTrue(map.replace(tile5, x, y, 1), "Replacing tile at (" + str(x) + ", " + str(y) + ", 1) should succeed and return True")
        
        self.assertEqual(len(map.tiles_[y][x]), 3, "Replaced Tile2 with Tile5, but stack at (" + str(ix) + ", " + str(iy) + ") is " + str(len(map.tiles_[y][x])) + " tiles long, not 3")
        self.assertEqual(map.tiles_[y][x][1], tile5, "Replaced Tile2 with Tile5, but found " + str(map.tiles_[y][x][1]) + " in its place instead")
        self.assertNotIn(tile2, map.tiles_[y][x], "Replaced Tile2 with Tile5, but Tile2 still found in stack")
        self.assertEqual(tile5.occupant, tile3, "Replaced Tile5 with Tile5, but Tile5's occupant is not Tile3")
        self.assertEqual(tile1.occupant, tile5, "Replaced Tile5 above Tile2, but Tile1's occupant is not Tile5")
        self.assertEqual(tile3.position.z, 6, "Replaced Tile2 of height " + str(tile2.get_height()) + " with Tile5 of height " + str(tile5.get_height()) + ", but top tile did not lower by " + str(tile2.get_height() - tile5.get_height()) + ", and is at " + str(tile3.position.z) + " instead")                

        # Replace bottom tile (Tile1)
        tile4 = Tile(None, 8)
        self.assertTrue(map.replace(tile4, x, y, 0), "Replacing tile at (" + str(x) + ", " + str(y) + ", 0) should succeed and return True")
        
        self.assertEqual(len(map.tiles_[y][x]), 3, "Replaced Tile1 with Tile4, but stack at (" + str(ix) + ", " + str(iy) + ") is " + str(len(map.tiles_[y][x])) + " tiles long, not 3")
        self.assertEqual(map.tiles_[y][x][0], tile4, "Replaced Tile1 with Tile4, but found " + str(map.tiles_[y][x][0]) + " in its place instead")
        self.assertNotIn(tile1, map.tiles_[y][x], "Replaced Tile1 with Tile4, but Tile1 still found in stack")
        self.assertEqual(tile4.occupant, tile5, "Replaced Tile1 with Tile4, but Tile4's occupant is not Tile5")
        self.assertEqual(tile3.position.z, 9, "Replaced Tile1 of height " + str(tile1.get_height()) + " with Tile4 of height " + str(tile4.get_height()) + ", but top tile did not rise by " + str(tile4.get_height() - tile1.get_height()) + ", and is at " + str(tile3.position.z) + " instead")

    #--------------------------------------------------------------------------------
    def test_map_06_remove_tile(self):
    #--------------------------------------------------------------------------------
        map = Map(2, 2)
        x = 1
        y = 1
                               
        # Replacing tiles out of bounds
        self.assertFalse(map.remove(-1, 0, 0), "Removing tile at (-1, 0, 0) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.remove(2, 0, 0), "Removing tile at (2, 0, 0) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.remove(0, -1, 0), "Removing tile at (0, -1, 0) is out of bounds for 2x2 map, and should return False")
        self.assertFalse(map.remove(0, 2, 0), "Removing tile at (0, 2, 0) is out of bounds for 2x2 map, and should return False")

        for ix in range(map.width):
            for iy in range(map.length):
                self.assertFalse(map.remove(ix, iy, 0), "Position [" + str(ix) + ", " + str(iy) + "] in unfilled map should be an empty array and thus return False")
                            
        # Setup map of three stacked tiles 
        tile1 = Tile(None, 5)
        tile2 = Tile(None, 3)
        tile3 = Tile(None, 10)
        tile4 = Tile(None, 2)
        
        map.place(tile1, x, y)
        map.place(tile2, x, y)
        map.place(tile3, x, y)
        map.place(tile4, x, y)
        
        self.assertFalse(map.remove(x, y, -1), "Removing tile at (" + str(ix) + ", " + str(iy) + ", -1) is out of bounds for 2x2x4 column, and should return False")
        self.assertFalse(map.remove(x, y, 4), "Removing tile at (" + str(ix) + ", " + str(iy) + ", 4) is out of bounds for 2x2x4 column, and should return False")
        
        # Remove top tile (Tile4)
        self.assertTrue(map.remove(x, y, 3), "Removing tile at (" + str(x) + ", " + str(y) + ", 3) should succeed and return True")
        
        self.assertEqual(len(map.tiles_[y][x]), 3, "Removed Tile4 from 4-tile stack at (" + str(ix) + ", " + str(iy) + "), but it's " + str(len(map.tiles_[y][x])) + " tiles long, not 3")        
        self.assertNotIn(tile4, map.tiles_[y][x], "Removed Tile4, but still found it in stack")
        self.assertEqual(tile3.occupant, None, "Removed Tile4, but Tile3's occupant is " + str(tile3.occupant) + ", not None")
        
        # Remove middle tile (Tile2)
        self.assertTrue(map.remove(x, y, 1), "Removing tile at (" + str(x) + ", " + str(y) + ", 1) should succeed and return True")
        
        self.assertEqual(len(map.tiles_[y][x]), 2, "Removed Tile2 from 3-tile stack at (" + str(ix) + ", " + str(iy) + "), but it's " + str(len(map.tiles_[y][x])) + " tiles long, not 2")        
        self.assertNotIn(tile2, map.tiles_[y][x], "Removed Tile2, but still found it in stack")
        self.assertEqual(tile1.occupant, tile3, "Removed Tile2, but Tile1's occupant is " + str(tile3.occupant) + ", not Tile3")
        self.assertEqual(tile3.position.z, 5, "Removed Tile2 of height " + str(tile2.get_height()) + " but top tile did not fall by that amount and is at " + str(tile3.position.z) + " instead")

    #--------------------------------------------------------------------------------
    def test_map_07_unit_scale(self):
    #--------------------------------------------------------------------------------
        # Default scale
        map = Map(2, 2)
        
        self.assertEqual(map.scale_.x, 32, "Default map's width scaling should be 32px/unit, but is " + str(map.scale_.x))
        self.assertEqual(map.scale_.y, 24, "Default map's length scaling should be 24px/unit, but is " + str(map.scale_.y))
        self.assertEqual(map.scale_.z, 8, "Default map's height scaling should be 8px/unit, but is " + str(map.scale_.z))
        
        # Scale specified out of bounds
        map = Map(2, 2, sf.Vector3(0, 0, 0))
        
        self.assertEqual(map.scale_.x, 1, "Out of bound width scale (< 1) width scaling should be 1px/unit, but is " + str(map.scale_.x))
        self.assertEqual(map.scale_.y, 1, "Out of bound length scale (< 1) length scaling should be 1px/unit, but is " + str(map.scale_.y))
        self.assertEqual(map.scale_.z, 1, "Out of bound height scale (< 1) scaling should be 1px/unit, but is " + str(map.scale_.z))
        
        # In bound scale
        scale = sf.Vector3(random.randint(1, 100), random.randint(1, 100), random.randint(1, 100))

        map = Map(2, 2, scale)
        self.assertEqual(map.scale_.x, scale.x, "Map constructed with scaling vector " + str(scale) + " should have a width scaling of " + str(scale.x) + "px/unit, but is " + str(map.scale_.x))
        self.assertEqual(map.scale_.y, scale.y, "Map constructed with scaling vector " + str(scale) + " should have a length scaling of " + str(scale.y) + "px/unit, but is " + str(map.scale_.y))
        self.assertEqual(map.scale_.z, scale.z, "Map constructed with scaling vector " + str(scale) + " should have a height scaling of " + str(scale.z) + "px/unit, but is " + str(map.scale_.y))

        # Setting scale to out of bounds
        map.set_unit_scale(sf.Vector3(0, 0, 0))
        
        self.assertEqual(map.scale_.x, 1, "Setting scale out of bounds (< 1) width scaling should be 1px/unit, but is " + str(map.scale_.x))
        self.assertEqual(map.scale_.y, 1, "Setting scale out of bounds(< 1) length scaling should be 1px/unit, but is " + str(map.scale_.y))
        self.assertEqual(map.scale_.z, 1, "Setting scale out of bounds (< 1) scaling should be 1px/unit, but is " + str(map.scale_.z))
    #--------------------------------------------------------------------------------
    def test_map_08_isometric_transforming(self):
    #--------------------------------------------------------------------------------
        for i in range(10):
            scale = sf.Vector3(random.randint(1, 100), random.randint(1, 100), random.randint(1, 100))
        
            map = Map(1, 1, scale)
            
            for i in range(100):
                p1 = sf.Vector3(random.randint(1, 100), random.randint(1, 100), random.randint(1, 100))                
                p1x = map.get_isometric_transform(p1).transform_point(sf.Vector2(0, 0))

                # Randomly shift X
                p2 = sf.Vector3(random.randint(1, 100), p1.y, p1.z)
                p2x = map.get_isometric_transform(p2).transform_point(sf.Vector2(0, 0))

                self.assertEqual(p2x.x - p1x.x, 0.5 * map.scale_.x * (p2.x - p1.x), "Isometric shift in x when shifting x from " + str(p1.x) + " to " + str(p2.x) + " for a map with scale " + str(map.scale_) + " should be " + str(0.5 * map.scale_.x * (p2.x - p1.x)) + ", not " + str(p2x.x - p1x.x))
                self.assertEqual(p2x.y - p1x.y, 0.5 * map.scale_.y * (p2.x - p1.x), "Isometric shift in y when shifting x from " + str(p1.x) + " to " + str(p2.x) + " for a map with scale " + str(map.scale_) + " should be " + str(0.5 * map.scale_.y * (p2.x - p1.x)) + ", not " + str(p2x.y - p1x.y))

                # Randomly shift Y
                p2 = sf.Vector3(p1.x, random.randint(1, 100), p1.z)
                p2x = map.get_isometric_transform(p2).transform_point(sf.Vector2(0, 0))

                self.assertEqual(p2x.x - p1x.x, -0.5 * map.scale_.x * (p2.y - p1.y), "Isometric shift in x when shifting y from " + str(p1.y) + " to " + str(p2.y) + " for a map with scale " + str(map.scale_) + " should be " + str(-0.5 * map.scale_.x * (p2.y - p1.y)) + ", not " + str(p2x.x - p1x.x))
                self.assertEqual(p2x.y - p1x.y, 0.5 * map.scale_.y * (p2.y - p1.y), "Isometric shift in y when shifting y from " + str(p1.y) + " to " + str(p2.y) + " for a map with scale " + str(map.scale_) + " should be " + str(0.5 * map.scale_.y * (p2.y - p1.y)) + ", not " + str(p2x.y - p1x.y))

                # Randomly shift Z
                p2 = sf.Vector3(p1.x, p1.y, random.randint(1, 100))
                p2x = map.get_isometric_transform(p2).transform_point(sf.Vector2(0, 0))

                self.assertEqual(p1x.y - p2x.y, map.scale_.z * (p2.z - p1.z), "Isometric shift in y when shifting z from " + str(p1.z) + " to " + str(p2.z) + " for a map with scale " + str(map.scale_) + " should be " + str(map.scale_.z * (p2.z - p1.z)) + ", not " + str(p1x.y - p2x.y))

    #--------------------------------------------------------------------------------
    def test_map_09_get_height(self):
    #--------------------------------------------------------------------------------
        map = Map(2, 2)

        # Setup map of three stacked tiles 
        tile1 = Tile(None, 5)
        tile2 = Tile(None, 3)
        tile3 = Tile(None, 10)
        
        map.place(tile1, 0, 0)
        map.place(tile2, 0, 1)
        map.place(tile3, 1, 1)

        # Out of bound coordinates should return False
        self.assertFalse(map.height(sf.Vector2(-0.5, 0)), "Out-bound position " + str(sf.Vector2(-0.5, 0)) + " returned " + str(map.height(sf.Vector2(-0.5, 0))) + ", not False")
        self.assertFalse(map.height(sf.Vector2(1.5, 0)), "Out-bound position " + str(sf.Vector2(1.5, 0)) + " returned " + str(map.height(sf.Vector2(1.5, 0))) + ", not False")
        self.assertFalse(map.height(sf.Vector2(0, -0.5)), "Out-bound position " + str(sf.Vector2(0, -0.5)) + " returned " + str(map.height(sf.Vector2(0, -0.5))) + ", not False")
        self.assertFalse(map.height(sf.Vector2(0, 1.5)), "Out-bound position " + str(sf.Vector2(0, 1.5)) + " returned " + str(map.height(sf.Vector2(0, 1.5))) + ", not False")

        for dx in arange(-0.4, 0.5, 0.1):
            for dy in arange(-0.4, 0.5, 0.1):
                # Coordinate of a blank tile space should return False
                self.assertFalse(map.height(sf.Vector2(1 + dx, 0 + dy)), "Blank region " + str(sf.Vector2(1 + dx, 0 + dy)) + " returned " + str(map.height(sf.Vector2(1 + dx, 0 + dy))) + ", not False")

                # In-bound coordinate of a filled tile space should return the tile of that space
                self.assertEqual(map.height(sf.Vector2(0 + dx, 0 + dy)), 5, "Position " + str(sf.Vector2(0 + dx, 0 + dy)) + " returned " + str(map.height(sf.Vector2(0 + dx, 0 + dy))) + ", not 5")
                self.assertEqual(map.height(sf.Vector2(0 + dx, 1 + dy)), 3, "Position " + str(sf.Vector2(0 + dx, 1 + dy)) + " returned " + str(map.height(sf.Vector2(0 + dx, 1 + dy))) + ", not 3")
                self.assertEqual(map.height(sf.Vector2(1 + dx, 1 + dy)), 10, "Position " + str(sf.Vector2(1 + dx, 1 + dy)) + " returned " + str(map.height(sf.Vector2(1 + dx, 1 + dy))) + ", not 10")
                
if __name__ == "__main__":
    unittest.main(verbosity = 2)