from mobile_object import MobileObject
import sfml as sf

#================================================================================
class Actor(MobileObject):
#================================================================================
# Represents an active map object
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Actor Constructor
    #----------------------------------------------------------------------------
    # * sprite : representative sprite for this actor
    #----------------------------------------------------------------------------
    def __init__(self, sprite = None, ground = None):
        MobileObject.__init__(self, ground)
        self.sprite = sprite

    #----------------------------------------------------------------------------
    # - Draw (Overload)
    #----------------------------------------------------------------------------
    def draw(self, target, states):
        if self.sprite != None:
            target.draw(self.sprite, states)

    def get_height(self, position = None):
        return 200

# Members
    sprite = None
#================================================================================
