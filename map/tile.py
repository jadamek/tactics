import sfml as sf

#================================================================================
class Tile:
#================================================================================
# Represents a single isometric tile, which occupies a 3-D space described by
# x,y,z position and height.
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Rise
    #----------------------------------------------------------------------------
    # * z : relative height to raise this tile by.
    # Raises a tile increasing its z-position and that of any object above it.
    #----------------------------------------------------------------------------
    def rise(self, z):
        self.position.z += z
        if self.occupant != None:
            self.occupant.rise(z)
        
    #----------------------------------------------------------------------------
    # - Lower 
    #----------------------------------------------------------------------------
    # * z : relative height to lower this tile by.
    # Lowers a tile decreasing its z-position and that of any object above it.
    #----------------------------------------------------------------------------
    def lower(self, z):
        self.position.z -= z
        if self.occupant != None:
            self.occupant.lower(z)

# Members
    occupant = None
    position = sf.Vector3(0, 0, 0)
    height = 1.0
#================================================================================
    