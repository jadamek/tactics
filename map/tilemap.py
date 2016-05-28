import sfml as sfml, copy

#================================================================================
class Tilemap:
#================================================================================
# Represents an isometric tilemap, which consists of a 2-D jagged array of 3-D
# isometric tile blocks.
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Tilemap Constructor
    #----------------------------------------------------------------------------
    # * width : width of the map (x-axis) in tiles
    # * length : length of the map (y-axis) in tiles    
    #----------------------------------------------------------------------------
    def __init__(self, width = 10, length = 10):
        if int(width) < 1 : width = 1
        if int(length) < 1 : length = 1
        self.width = width
        self.length = length
        self.tiles_ = [[[]] * width] * length
        
    #----------------------------------------------------------------------------
    # - Place Tile
    #----------------------------------------------------------------------------
    # * tile : a tile to be placed on the top-most layer
    # * x : x-coordinate for the position to place the new tile at
    # * y : y-coordinate for the position to place the new tile at
    #----------------------------------------------------------------------------
    def place(self, tile, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.length:
            return False
                    
        z = 0
        
        # Place on the exact top of the highest tile at (x, y)
        if self.tiles_[y][x]:
            z = self.tiles_[y][x][-1].position.z + self.tiles_[y][x][-1].height
            
        tile.position = sf.Vector3(x, y, z)
        self.tiles_[y][x].append(tile)

        return True
        
    #----------------------------------------------------------------------------
    # - Get Tile At
    #----------------------------------------------------------------------------
    # * x : x-coordinate of the tile to grab
    # * y : y-coordinate of the tile to grab
    # * z : z-coordinate of the tile to grab. If ommitted, grabs top-most
    #----------------------------------------------------------------------------
    def at(self, x, y, z = None):
        if x < 0 or x >= self.width or y < 0 or y >= self.length:
            return False
        elif not self._tiles[y][x]:
            return False
            
        if z == None:
            return self.tiles_[y][x][-1]        
        else:
            i = 0            
            # If z is specified, try to get the tile whose z -> height region contains
            # z. If z is above the top-most tile, return the top-most.
            while z > self.tiles_[y][x][i].position.z + self.tiles_[y][x][i].height and i < len(self.tiles_[y][x]) - 1:
                i += 1
                
            return self.tiles_[y][x][i]            

# Members    
    tiles_ = []
    width = 0
    length = 0
    
    
tilemap = Tilemap(0, -22)
print tilemap.width, "x", tilemap.length, "\n", tilemap.tiles_