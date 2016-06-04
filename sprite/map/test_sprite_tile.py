from sprite_tile import SpriteTile
import random, unittest, sfml as sf

class TestSpriteTiles(unittest.TestCase):
    #--------------------------------------------------------------------------------
    def setUp(self):    
    #--------------------------------------------------------------------------------
        self.texture = sf.Texture.from_file("resources/graphics/Tile.png")
    
    #--------------------------------------------------------------------------------
    def test_sprite_tile_00_construction(self):        
    #--------------------------------------------------------------------------------
        self.texture = sf.Texture.from_file("resources/graphics/Tile.png")

        self.assertEqual(self.texture.width, 64, "Example texture Tile.png should be 64px wide")
        self.assertEqual(self.texture.height, 48, "Example texture Tile.png should be 48px high")
        
        # Default construction
        tile = SpriteTile(self.texture)

        self.assertEqual(tile.width, 32, "Default sprite tile should be 1/2 texture wide (32), but its width is " + str(tile.width))
        self.assertEqual(tile.length, 24, "Default sprite tile should be 1/2 texture height (32), but its length is " + str(tile.length))
        self.assertEqual(tile.height, 0, "Default sprite tile should have no height (0), but its height is " + str(tile.height))
        
        # Out of bound width, length, height - less than 0
        tile = SpriteTile(self.texture, -1, -1, -1)
        
        self.assertEqual(tile.width, 32, "Sprite tile initialized with [-1, -1, -1] should be 1/2 texture wide (32), but its width is " + str(tile.width))
        self.assertEqual(tile.length, 24, "Sprite tile initialized with [-1, -1, -1] should be 1/2 texture height (32), but its length is " + str(tile.length))
        self.assertEqual(tile.height, 0, "Sprite tile initialized with [-1, -1, -1] should have no height (0), but its height is " + str(tile.height))
        
        # Out of bound width or height - greater than 1/2 texture size
        tile = SpriteTile(self.texture, 33, 25)
        
        self.assertEqual(tile.width, 32, "Sprite tile initialized with width and length larger than 1/2 texture image should be 1/2 texture wide (32), but its width is " + str(tile.width))
        self.assertEqual(tile.length, 24, "Sprite tile initialized with width and length larger than 1/2 texture image should be 1/2 texture height (32), but its length is " + str(tile.length))

        # In bound width, length, height
        width = random.randint(1, 32)
        length = random.randint(1, 24)
        height = random.randint(1, 1000)

        tile = SpriteTile(self.texture, width, length, height)
        
        self.assertEqual(tile.width, width, "Sprite tile initialized with [" + str(width) + ", " + str(length) + ", " + str(height) + "] has a width of " + str(tile.width))
        self.assertEqual(tile.length, length, "Sprite tile initialized with [" + str(width) + ", " + str(length) + ", " + str(height) + "] has a length of " + str(tile.length))
        self.assertEqual(tile.height, height, "Sprite tile initialized with [" + str(width) + ", " + str(length) + ", " + str(height) + "] has a height of " + str(tile.height))
       
    #--------------------------------------------------------------------------------
    def test_sprite_tile_01_rect_and_position(self):
    #--------------------------------------------------------------------------------
        for width in range(1, 33):
            for length in range(1, 25):
                for height in range(0, 10):
                    tile = SpriteTile(self.texture, width, length, height)
           
                    self.assertEqual(tile.top_.texture_rectangle, sf.Rectangle((0, 0), (width, length)), "Top (head) sprite texture rect should be in top-left corner (0, 0) with size ("+str(width)+", "+str(length)+"), but is " + str(tile.top_.texture_rectangle))
                    self.assertEqual(tile.center_.texture_rectangle, sf.Rectangle((width, 0), (width, height)), "Center (body) sprite texture rect should be in top-right corner ("+str(width)+", 0) with size ("+str(width)+", "+str(height)+"), but is " + str(tile.top_.texture_rectangle))
                    self.assertEqual(tile.bottom_.texture_rectangle, sf.Rectangle((0, length), (width, length)), "Bottom (floor) sprite texture rect should be in bottom-left corner (0, "+str(length)+") with size ("+str(width)+", "+str(length)+"), but is " + str(tile.top_.texture_rectangle))

                    self.assertEqual(tile.top_.position, sf.Vector2(-1 * width / 2, -1 * length / 2 - height), "Top (head) sprite should be positioned such that it is centered, but raised by height (-1/2*"+str(width)+", -1/2*"+str(length)+" - "+str(height)+"), but is " + str(tile.top_.position))
                    self.assertEqual(tile.center_.position, sf.Vector2(-1 * width / 2, -1 * height), "Center (body) sprite should be positioned such that it is centered horizontally, and raised by height (-1/2*"+str(width)+", -"+str(height)+"), but is " + str(tile.top_.position))
                    self.assertEqual(tile.bottom_.position, sf.Vector2(-1 * width / 2, -1 * length / 2), "Bottom (floor) sprite should be positioned such that it is centered on the origin (-1/2"+str(width)+", -1/2"+str(length)+"), but is " + str(tile.top_.position))

    #--------------------------------------------------------------------------------
    def test_sprite_tile_02_reset_height(self):
    #--------------------------------------------------------------------------------
        heights = random.sample(range(0, 100), 2)
        
        tile = SpriteTile(self.texture, 0, 0, heights[0])
        top_pos = tile.top_.position.y
        center_pos = tile.center_.position.y
        center_height = tile.center_.texture_rectangle.size.y
        
        tile.reset_height(heights[1])
        
        self.assertEqual(tile.top_.position.y - top_pos, heights[0] - heights[1], "Resetting tile's height from " + str(heights[0]) + " to " + str(heights[1]) + " should shift the top (head) sprite's y-coordinate by " + str(heights[0] - heights[1]) + ", not " + str(tile.top_.position.y - top_pos))
        self.assertEqual(tile.center_.position.y - center_pos, heights[0] - heights[1], "Resetting tile's height from " + str(heights[0]) + " to " + str(heights[1]) + " should shift the center sprite's y-position by " + str(heights[0] - heights[1]) + ", not " + str(tile.center_.position.y - center_pos))
        self.assertEqual(tile.center_.texture_rectangle.size.y - center_height, heights[1] - heights[0], "Resetting tile's height from " + str(heights[0]) + " to " + str(heights[1]) + " should shift the center sprite's y-position by " + str(heights[1] - heights[0]) + ", not " + str(tile.center_.texture_rectangle.size.y - center_height))
                    
    #--------------------------------------------------------------------------------
    def test_sprite_tile_03_continuous(self):
    #--------------------------------------------------------------------------------
        tile = SpriteTile(self.texture, 0, 0, 0, True)
        
        self.assertEqual(tile.bottom_, None, "Continuous tile should have no bottom (floor) sprite")
        self.assertEqual(tile.center_.texture_rectangle.size.y, self.texture.get_maximum_size(), "Continuous tile should have a center (body) sprite with maximum possible height, not " + str(tile.center_.texture_rectangle.size.y))

        height = random.randint(1, 1000)
        tile.reset_height(height)
        self.assertEqual(tile.center_.texture_rectangle.size.y, self.texture.get_maximum_size(), "Continuous tile should have a center (body) sprite with maximum possible height, not " + str(tile.center_.texture_rectangle.size.y) + " after height reset")

    texture = None