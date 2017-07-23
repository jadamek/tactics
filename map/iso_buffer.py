from sfml import sf
import sys, os, math

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
import settings

#================================================================================
class IsometricNode:
#================================================================================
# Represents a single node in the isometric ordering container
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # -  Isometric Node Contructor
    #----------------------------------------------------------------------------
    # * target : Drawable Isometric Object this node handles
    # * left : Isometric Node to the left (lower priority) of this one
    # * right : Isometric Node to the right (higher priority) of this one 
    #----------------------------------------------------------------------------
    def __init__(self, target, container):
        self.target = target
        self.container = container
        self.dirty = False

        if target != None:
            self.target.handler = self

    #----------------------------------------------------------------------------
    # -  Isometric Node Destructor
    #----------------------------------------------------------------------------
    def __del__(self):
        # Remove this node from its buffer, and any reference its target has
        self.detach()

    #----------------------------------------------------------------------------
    # - Detach
    #----------------------------------------------------------------------------
    # Detaches this Isometric Node from its parents and children
    #----------------------------------------------------------------------------
    def detach(self):
        pass
               
# Members
    target = None
    container = None
    dirty = False
#================================================================================

#================================================================================
class IsometricBuffer:
#================================================================================
# Represents a depth buffer of drawable isometric objects
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # -  Isometric Buffer Constructor
    #----------------------------------------------------------------------------
    def __init__(self):
        self.buffer = set([])
        self.images = []

    #----------------------------------------------------------------------------
    # - Add Object
    #----------------------------------------------------------------------------
    # * drawable : Isometric Object to be added to the buffer.
    # Adds an Isometric Object to the buffer in each x-y index matching the
    # object's own coordinates, then sorted by its z-coordinate.
    #----------------------------------------------------------------------------
    def add(self, drawable):
        self.images.append(drawable)        


# Members
    buffer = None
    images = None
#================================================================================

#================================================================================
class IsometricObject(sf.Drawable):
#================================================================================
# Represents a drawable object in the isometric space.
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Isometric Object Contructor
    #----------------------------------------------------------------------------
    def __init__(self):
        sf.Drawable.__init__(self)
        self.position = sf.Vector3()
    
    #----------------------------------------------------------------------------
    # - Isometric Object Destructor
    #----------------------------------------------------------------------------
    def __del__(self):
        # Detach this object from any IsometricBuffer it was a part of.
        if self.handler != None:
            self.handler.detach()
            del self.handler
 
    #----------------------------------------------------------------------------
    # - Set Position
    #----------------------------------------------------------------------------
    # * position : new 3-D position of the object
    # Sets the position of the object to a new location, and sorts appropriately
    #----------------------------------------------------------------------------
    def set_position(self, position):
        # Retain old x and y coordinates, and compute the change in z (height)       
        self.position = position
        self.handler.dirty = True
    
    #----------------------------------------------------------------------------
    # - Get Height
    #----------------------------------------------------------------------------
    # * position : (x,y) position relative to the center of the tile
    #----------------------------------------------------------------------------
    def get_height(self, position = sf.Vector2()):
        return 1.0

# Members
    handler = None
    position = None
#================================================================================