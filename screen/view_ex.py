import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import settings, sfml as sf, copy

#================================================================================
class ViewEx(sf.View):
#================================================================================
# Extends the SFML View to add major functionality such as zooming, scrolling,
# shaking and flashing.
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # ViewEx Constructor
    #----------------------------------------------------------------------------
    # * rectangle :  intial viewing zone, top-left corcner at x,y with view size
    #       width, height
    #----------------------------------------------------------------------------
    def __init__(self, rectangle = sf.Rectangle(sf.Vector2(), sf.Vector2(640, 480))):
        sf.View.__init__(self, rectangle)

        self.center_ = self.center
        self.rotation_ = 0.0
        self.zoom_ = 1.0
        self.clock_ = 0.0
        self.speed = 1
        self.frozen = False

        self.flash_box_ = sf.RectangleShape(sf.Vector2(2000, 2000))
        self.flash_box_.position = self.center
        self.flash_box_.fill_color = sf.Color(0, 0, 0, 0)
        self.tint_box_ = copy.copy(self.flash_box_)
        
    #----------------------------------------------------------------------------
    # - Set View Center
    #----------------------------------------------------------------------------
    # * center : a new position to center the view on
    # Functionally overrides a basic center set to include updates for attached
    # extensions, such as the flash color box
    #----------------------------------------------------------------------------
    def set_center(self, center):
        self.center = center
        self.center_ = center

    #----------------------------------------------------------------------------
    # Set View Window Size
    # * size : new width x height of the viewing window
    # Functionally overrides a basic size set to include updates for extensions
    #----------------------------------------------------------------------------
    def set_size(self, size):
        self.size = size * self.zoom_

    #----------------------------------------------------------------------------
    # - Move View Center
    #----------------------------------------------------------------------------
    # * offset : vector describing the x,y offset to change the view's center by
    #----------------------------------------------------------------------------
    def move(self, offset):
        self.center = self.center + offset
        self.center_ = self.center_ + offset
        
    #----------------------------------------------------------------------------
    # - Set View Rotation Angle
    #----------------------------------------------------------------------------
    # * angle : angle to rotate the view by
    # Functionally overrides a basic rotation set to include updates for
    # extensions
    #----------------------------------------------------------------------------
    def set_rotation(self, angle):
        self.rotation = angle
        self.rotation_ = self.rotation

    #----------------------------------------------------------------------------
    # - Rotate View (Overload)
    #----------------------------------------------------------------------------
    # * angle : angle to rotate the view by
    # Overloaded to include updates for extensions
    #----------------------------------------------------------------------------
    def rotate(self, angle):
        self.rotation += angle
        self.rotation_ += angle        

    #----------------------------------------------------------------------------
    # Scale (Zoom) Viewing Zone
    #----------------------------------------------------------------------------
    # * factor : scale factor to increase the window's view by.
    # Provides functionality of sf.View.zoom, including updates for extensions.
    #----------------------------------------------------------------------------
    def scale(self, factor):
        if factor > 0:
            size = self.size / self.zoom_
            self.zoom_ *= factor
            size *= self.zoom_            
            self.size = size

    #----------------------------------------------------------------------------
    # - Reset View (Overload)
    #----------------------------------------------------------------------------
    # * rectangle : new viewing zone, top-left corcner on x,y with region size
    #       width, height
    # Overloaded to include updates for extensions
    #----------------------------------------------------------------------------
    def reset(self, rectangle):
        super(ViewEx, self).reset(rectangle)
        self.zoom_ = 1.0
        self.set_center(self.center)
        self.set_size(rectangle.size)
        self.set_rotation(self.rotation)

    #----------------------------------------------------------------------------
    # - Draw View Overlays
    #----------------------------------------------------------------------------
    # Implements SFML Drawable.draw protocol for flash and tint boxes
    #----------------------------------------------------------------------------
    def draw(self, target, states):
        target.draw(self.tint_box_, states)
        if self.flash_length_ > 0:
            target.draw(self.flash_box_, states)

    #----------------------------------------------------------------------------
    # Increment Frame
    #----------------------------------------------------------------------------
    # Updates all active extensions, such as flashing and shaking
    #----------------------------------------------------------------------------
    def step(self):
        pass

    #----------------------------------------------------------------------------
    # Update
    #----------------------------------------------------------------------------
    # * elapsed : relative time passed since last update
    #----------------------------------------------------------------------------
    def update(self, elapsed):
        if not self.frozen:
            self.clock_ += elapsed * self.speed * settings.FPS
            while self.clock_ >= 1:
                self.step()
                self.clock_ -= 1

# Members
    center_ = None
    rotation_ = 0.0
    
    flash_peak_ = 0
    flash_length_ = 0

    tint_color_ = None
    tint_length_ = 0

    scroll_target_ = None
    scroll_length_ = 0

    shake_amp_ = 0.0
    shake_freq_= 0.0
    shake_peak_ = 0
    shake_length_ = 0
    shake_loop_ = False
    shake_dir_ = 0

    tint_box_ = None
    flash_box_ = None

    zoom_ = 1.0
    zoom_rate_ = 0.0
    zoom_length_ = 0

    spin_speed_ = 0.0
    spin_loop_ = False
    slin_length_ = 0

    frozen = False
    speed = 1
    clock_ = 0

# Shake direction named constants
    SHAKE_HORIZONTAL = 0
    SHAKE_VERTICAL = 1
#================================================================================