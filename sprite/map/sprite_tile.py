import sfml as sf

#================================================================================
class SpriteTile(sf.TransformableDrawable):
#================================================================================
# A sprite of a single (continuous or discrete) tile column.
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Tile Sprite Contructor
    #----------------------------------------------------------------------------
    # * texture : the bitmap containing the image data for the tile.
    # * width : width in pixels; 0 to fit automatically to texture
    # * length : width in pixels; 0 to fit automatically to texture
    # * height : height in pixels
    # * continuous : TRUE if the tile's sprite continues infinitely downward
    #----------------------------------------------------------------------------
    def __init__(self, texture, width = 0, length = 0, height = 0, continous = False):
        sf.TransformableDrawable.__init__(self)
        
        self.width = width
        self.length = length
        self.height = height
        self.continuous = continous

        if width <= 0 or width > texture.width / 2:
            self.width = texture.width / 2        
        if length <= 0 or length > texture.height / 2:
            self.length = texture.height / 2
        if height < 0:
            self.height = 0
                
        texture.repeated = True        
            
        self.top_ = sf.Sprite(texture)
        self.top_.texture_rectangle = sf.Rectangle((0, 0), (self.width, self.length))
        self.top_.position = sf.Vector2(-1 * self.width / 2, -1 * self.length / 2 - self.height)
        self.center_ = sf.Sprite(texture)        
        self.center_.position = sf.Vector2(-1 * self.width / 2, -1 * self.height)

        if not self.continuous:
            self.bottom_ = sf.Sprite(texture)
            self.bottom_.texture_rectangle = sf.Rectangle((0, self.length), (self.width, self.length))
            self.bottom_.position = sf.Vector2(-1 * self.width / 2, -1 * self.length / 2)
            self.center_.texture_rectangle = sf.Rectangle((self.width, 0), (self.width, self.height))
        else:
            self.center_.texture_rectangle = sf.Rectangle((self.width, 0), (self.width, texture.get_maximum_size()))
            
    #----------------------------------------------------------------------------
    # - Reset Height
    #----------------------------------------------------------------------------            
    # * height : new height of the tile sprite
    # Recompute sub-sprite widths and positions for a new virtual height.
    #----------------------------------------------------------------------------            
    def reset_height(self, height):
        self.height = height
        if height < 0:
            self.height = 0

        self.top_.position = sf.Vector2(-1 * self.width / 2, -1 * self.length / 2 - self.height)
        self.center_.position = sf.Vector2(-1 * self.width / 2, -1 * self.height)
        
        if not self.continuous:
            self.center_.texture_rectangle = sf.Rectangle((self.width, 0), (self.width, self.height))

    #----------------------------------------------------------------------------
    # - Draw (Overload)
    #----------------------------------------------------------------------------
    def draw(self, target, states):
        states.transform.combine(self.transform)
        
        if self.bottom_ is not None:
            target.draw(self.bottom_, states)
        target.draw(self.center_, states)
        target.draw(self.top_, states)
    
# Members    
    width = 0
    length = 0
    height = 0
    continuous = False
    
    top_ = None
    center_ = None
    bottom_ = None
#================================================================================
