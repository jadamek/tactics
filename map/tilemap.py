import tile.Tile, sfml as sfml

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
        self.width = width
        self.length = length
        

    #----------------------------------------------------------------------------
    # - Place Tile
    #----------------------------------------------------------------------------
    # * z : relative height to raise this tile by.
    # Raises a tile increasing its z-position and that of any object above it.
    #----------------------------------------------------------------------------
    
# Members    
    floor_ = None
    ground_ = None
    width = 10
    length = 10