import sfml as sf, copy, sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../container")
from zlist import ZList

#================================================================================
class Map(sf.TransformableDrawable):
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
    # * scale : unit scale vector which describes pixels per unit distance for
    #       width (x), length (y) and height (z)
    #----------------------------------------------------------------------------
    def __init__(self, width = 10, length = 10, scale = sf.Vector3(32, 24, 8)):
        sf.Drawable.__init__(self)
        
        # Sanitization
        if int(width) < 1 : width = 1
        if int(length) < 1 : length = 1
        ux = scale.x
        uy = scale.y
        uz = scale.z
        if ux < 1: ux = 1
        if uy < 1: uy = 1
        if uz < 1: uz = 1
        
        self.width = width
        self.length = length
        
        self.tiles_ = []
        for y in range(self.length):
            self.tiles_.append([])
            for x in range(self.width):
                self.tiles_[y].append([])
                
        self.images_ = ZList()
        self.scale_ = sf.Vector3(ux, uy, uz)
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
        elif not self.tiles_[y][x]:
            return False
            
        if z == None:
            return self.tiles_[y][x][-1]        
        else:
            i = 0            
            # If z is specified, try to get the tile whose z -> height region contains
            # z. If z is above the top-most tile, return the top-most.
            while z > self.tiles_[y][x][i].position.z + self.tiles_[y][x][i].get_height() and i < len(self.tiles_[y][x]) - 1:
                i += 1
                
            return self.tiles_[y][x][i]     
            
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
            z = self.tiles_[y][x][-1].position.z + self.tiles_[y][x][-1].get_height()
            tile.occupant = self.tiles_[y][x][-1].occupant
            self.tiles_[y][x][-1].occupant = tile
            
            if tile.occupant != None:
                tile.occupant.rise(tile.get_height())
            
        tile.position = sf.Vector3(x, y, z)
        
        self.tiles_[y][x].append(tile)
        self.images_.add(tile)

        return True
        
    #----------------------------------------------------------------------------
    # - Insert Tile
    #----------------------------------------------------------------------------
    # * tile : a tile to be placed on the top-most layer
    # * x : x-coordinate to insert the new tile at
    # * y : y-coordinate to insert the new tile at
    # * layer : layer (index) to insert the tile at
    #----------------------------------------------------------------------------
    def insert(self, tile, x, y, layer):
        if x < 0 or x >= self.width or y < 0 or y >= self.length:
            return False
        elif not self.tiles_[y][x] or layer < 0 or layer >= len(self.tiles_[y][x]):
            return False
        
        z = 0
        
        if layer > 0:
            z = self.tiles_[y][x][layer - 1].position.z + self.tiles_[y][x][layer - 1].get_height()
            self.tiles_[y][x][layer - 1].occupant = tile
                        
        tile.occupant = self.tiles_[y][x][layer]
        tile.occupant.rise(tile.get_height())
        tile.position = sf.Vector3(x, y, z)
        
        self.tiles_[y][x].insert(layer, tile)
        self.images_.add(tile)           

        return True
        
    #----------------------------------------------------------------------------
    # - Override Tile
    #----------------------------------------------------------------------------
    # * tile : the tile that will replace another
    # * x : x-coordinate of the tile to be replaced
    # * y : y-coordinate of the tile to be replaced
    # * layer : layer (index) of the tile to be replaced
    #----------------------------------------------------------------------------
    def replace(self, tile, x, y, layer):
        if x < 0 or x >= self.width or y < 0 or y >= self.length:
            return False
        elif not self.tiles_[y][x] or layer < 0 or layer >= len(self.tiles_[y][x]):
            return False
                
        if layer > 0:            
            self.tiles_[y][x][layer - 1].occupant = tile

        tile.occupant = self.tiles_[y][x][layer].occupant
            
        if tile.occupant != None:
            difference = tile.get_height() - self.tiles_[y][x][layer].get_height()
            
            if difference > 0:
                tile.occupant.rise(difference)
            elif difference < 0:
                tile.occupant.lower(difference * -1)
            
        tile.position = copy.copy(self.tiles_[y][x][layer].position)
        
        self.tiles_[y][x][layer] = tile
        self.images_.add(tile)

        return True
        
    #----------------------------------------------------------------------------
    # - Remove Tile
    #----------------------------------------------------------------------------
    # * x : x-coordinate of the tile to be removed
    # * y : y-coordinate of the tile to be removed
    # * layer : layer (index) of the tile to be removed
    #----------------------------------------------------------------------------
    def remove(self, x, y, layer):
        if x < 0 or x >= self.width or y < 0 or y >= self.length:
            return False
        elif not self.tiles_[y][x] or layer < 0 or layer >= len(self.tiles_[y][x]):
            return False
                
        if layer > 0:            
            self.tiles_[y][x][layer - 1].occupant = self.tiles_[y][x][layer].occupant
            
        if self.tiles_[y][x][layer].occupant != None:
            self.tiles_[y][x][layer].occupant.lower(self.tiles_[y][x][layer].get_height())
                
        del self.tiles_[y][x][layer]
        
        return True                   

    #----------------------------------------------------------------------------
    # - Set Unit Scale
    #----------------------------------------------------------------------------
    # * scale : unit scale vector which describes pixels per unit distance for
    #       width (x), length (y) and height (z)
    #----------------------------------------------------------------------------
    def set_unit_scale(self, scale):
        ux = scale.x
        uy = scale.y
        uz = scale.z
        if ux < 1: ux = 1
        if uy < 1: uy = 1
        if uz < 1: uz = 1
        
        self.scale_ = sf.Vector3(ux, uy, uz)

    #----------------------------------------------------------------------------
    # Get Isometric Transform
    #----------------------------------------------------------------------------
    # * local : 3-D position in local coordinate system, which is used to compute
    #       the 2-D isometric transform for graphic coordinates.
    #----------------------------------------------------------------------------
    def get_isometric_transform(self, local):
        transform = sf.Transform()
        
        # Update with the map's transform
        transform.combine(self.transform)
        
        #Translate to isometric coordinates        
        x = 0.5 * self.scale_.x * (local.x - local.y);
        y = 0.5 * self.scale_.y * (local.x + local.y) - self.scale_.z * local.z;	    
        
        transform.translate(sf.Vector2(x, y))
        
        return transform

    #----------------------------------------------------------------------------
    # Get Height
    #----------------------------------------------------------------------------
    # * x : x-coordinate of position by which to query the map height.
    # * y : y-coordinate of position by which to query the map height.
    #----------------------------------------------------------------------------
    def height(self, x, y):
        x_i = int(round(x))
        y_i = int(round(y))

        tile = self.at(x_i, y_i)

        if tile: return tile.position.z + tile.get_height(sf.Vector2(x - x_i, y - y_i))
        else: return None

    #----------------------------------------------------------------------------
    # - Draw (Overload)
    #----------------------------------------------------------------------------
    def draw(self, target, states):        
        image = self.images_.front()
        
        while(image is not None):
            local_states = sf.RenderStates(states.blend_mode, states.transform * self.get_isometric_transform(image.target.position), states.texture, states.shader)
            target.draw(image.target.sprite, local_states)
            image = image.next
        
# Members    
    tiles_ = []
    width = 0
    length = 0
    images_ = None
    scale_ = None
#================================================================================
    