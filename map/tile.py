import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../container")

from zlist import *
import sfml as sf

#================================================================================
class Tile(ZObject):
#================================================================================
# Represents a single isometric tile, which occupies a 3-D space described by
# x,y,z position and height.
#================================================================================
# Methods        
    #----------------------------------------------------------------------------
    # - Tile Constructor
    #----------------------------------------------------------------------------
    def __init__(self, sprite = None, height = 1.0):
        if float(height) < 0: height = 0
        self.height = height
        self.sprite = sprite

    #----------------------------------------------------------------------------
    # - Rise
    #----------------------------------------------------------------------------
    # * z : relative height to raise this tile by.
    # Raises a tile increasing its z-position and that of any object above it.
    #----------------------------------------------------------------------------
    def rise(self, z):
        self.position.z += z
        if self.handler != None:
            self.handler.sortUp()
        
        if self.occupant != None:
            self.occupant.rise(z)
        
    #----------------------------------------------------------------------------
    # - Lower 
    #----------------------------------------------------------------------------
    # * z : relative height to lower this tile by.
    # Lowers a tile decreasing its z-position and that of any object above it.
    #----------------------------------------------------------------------------
    def lower(self, z):
        if self.position.z - z < 0:
            return False
            
        self.position.z -= z
        if self.handler != None:
            self.handler.sortDown()
            
        if self.occupant != None:
            self.occupant.lower(z)
            
    #----------------------------------------------------------------------------
    # - Draw (Overload)
    #----------------------------------------------------------------------------
    def draw(self, target, states):
        if self.sprite != None:
            target.draw(self.sprite, states)

# Members
    sprite = None
    occupant = None
    position = sf.Vector3(0, 0, 0)
    height = 1.0
#================================================================================