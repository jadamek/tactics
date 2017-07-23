import sys, os
from sfml import sf
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
import settings, copy, math

#================================================================================
class ViewEx(sf.View):
#================================================================================
# Extends the SFML View to add major functionality such as zooming, scrolling,
# shaking and flashing.
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - ViewEx Constructor
    #----------------------------------------------------------------------------
    # * Rect :  intial viewing zone, top-left corcner at x,y with view size
    #       width, height
    #----------------------------------------------------------------------------
    def __init__(self, Rect = sf.Rect(sf.Vector2(), sf.Vector2(640, 480))):
        sf.View.__init__(self, Rect)

        self.center_ = self.center
        self.rotation_ = 0.0
        self.zoom_ = 1.0
        self.clock_ = 0.0
        self.speed = 1
        self.frozen = False

        self.flash_box_ = sf.RectangleShape(sf.Vector2(1000, 1000))
        self.flash_box_.fill_color = sf.Color(0, 0, 0, 0)
        self.tint_box_ = sf.RectangleShape(sf.Vector2(1000, 1000))
        self.tint_box_.fill_color = sf.Color(0, 0, 0, 0)
        
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
    # - Set View Window Size
    #----------------------------------------------------------------------------
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
    # - Scale (Zoom) Viewing Zone
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
    # - Scroll
    #----------------------------------------------------------------------------
    # * distance : the offset vector to scroll along
    # * duration : time in seconds the scroll will be completed in    
    # Starts the scrolling process by setting and computing a frame-wise time
    # length from the duration in seconds.
    #----------------------------------------------------------------------------
    def scroll(self, offset, duration):
        self.scroll_target_ = self.center_ + offset
        self.scroll_length_ = math.floor(duration * settings.FPS)

    #----------------------------------------------------------------------------
    # - Scroll to Point
    #----------------------------------------------------------------------------
    # * target : screen position to scroll to
    # * duration : time in seconds the scroll will be completed in    
    #----------------------------------------------------------------------------
    def scrollTo(self, target, duration):
        self.scroll_target_ = target
        self.scroll_length_ = math.floor(duration * settings.FPS)

    #----------------------------------------------------------------------------
    # - Is Scrolling?
    #----------------------------------------------------------------------------
    # Returns whether the view is currently scrolling
    #----------------------------------------------------------------------------
    def scrolling(self):
        return self.scroll_length_ > 0

    #----------------------------------------------------------------------------
    # - Stop Scrolling
    #----------------------------------------------------------------------------
    # Ceases any scroll motion by setting the duration to 0.
    #----------------------------------------------------------------------------
    def stop_scrolling(self):
        self.scroll_length_ = 0

    #----------------------------------------------------------------------------
    # - Shake
    #----------------------------------------------------------------------------
    # * magnitude : amplitude of the vibrational motion in pixels
    # * frequency : amplitude of the vibrational motion in periods/second
    # * duration : time in seconds the shake will last. A duration less than 1 is
    #       an looping (infinite) shake
    # * direction : direction of the vibration; may be horizontal (0) or vertical
    #       (1), and defaults to horizontal otherwise
    #----------------------------------------------------------------------------
    def shake(self, magnitude, frequency, duration = 0, direction = 0):
        if magnitude is not 0 and frequency > 0:
            self.shake_amp_ = magnitude
            self.shake_freq_ = frequency

            if duration > 0:
                self.shake_peak_ = math.floor(duration * settings.FPS)
                self.shake_length_ = self.shake_peak_
            self.shake_loop_ = duration <= 0

            if direction is not self.SHAKE_HORIZONTAL and direction is not self.SHAKE_VERTICAL:
                direction = self.SHAKE_HORIZONTAL
            self.shake_dir_ = direction

    #----------------------------------------------------------------------------
    # - Is Shaking?
    #----------------------------------------------------------------------------
    # Returns whether the view is currently shaking
    #----------------------------------------------------------------------------
    def shaking(self):
        return self.shake_loop_ or self.shake_length_ > 0

    #----------------------------------------------------------------------------
    # - Stop Shaking
    #----------------------------------------------------------------------------
    # Ceases any shaking motion currently active, returning the screen to its
    # true center
    #----------------------------------------------------------------------------
    def stop_shaking(self):
        self.shake_length_ = 0
        self.shake_loop_ = False
        self.center = self.center_

    #----------------------------------------------------------------------------
    # - Zoom
    #----------------------------------------------------------------------------
    # * factor : amount by which to change the view current zoom factor. A
    #       factor < 0 is a zoom in, > 0 is a zoom out.
    # * duration : time in seconds the gradual zoom will be complete
    #----------------------------------------------------------------------------
    def zoom(self, factor, duration):
        if self.zoom_ + factor > 0 and duration > 0:
            self.zoom_rate_ = factor * self.zoom_ / duration / settings.FPS;
            self.zoom_length_ = math.floor(duration * settings.FPS)

    #----------------------------------------------------------------------------
    # - Is Zooming?
    #----------------------------------------------------------------------------
    # Returns whether the view is currently zooming in or out
    #----------------------------------------------------------------------------
    def zooming(self):
        return self.zoom_length_ > 0

    #----------------------------------------------------------------------------
    # - Stop Zooming
    #----------------------------------------------------------------------------
    # Ceases any zooming currently active
    #----------------------------------------------------------------------------
    def stop_zooming(self):
        self.zoom_length_ = 0

    #----------------------------------------------------------------------------
    # - Spin
    #----------------------------------------------------------------------------
    # * rps : the number of revolutions/second (angular speed)
    # * revolutions : number of revolutions to complete. 0 is looping (inf)
    # * direction : may be clockwise (-1) or counter-clockwise (1)
    # Causes the view so spin at a constant rate
    #----------------------------------------------------------------------------
    def spin(self, rps, revolutions = 0, direction = -1.0):        
        if rps > 0:
            if direction is not self.SPIN_CLOCKWISE and direction is not self.SPIN_COUNTER_CLOCKWISE:
                direction = self.SPIN_CLOCKWISE
            self.spin_speed_ = rps * 360.0 / settings.FPS * direction
            self.spin_length_ = math.floor(revolutions / rps * settings.FPS)
            self.spin_loop_ = revolutions <= 0

    #----------------------------------------------------------------------------
    # - Is Spinning?
    #----------------------------------------------------------------------------
    # Returns whether the view is currently spinning
    #----------------------------------------------------------------------------
    def spinning(self):
        return self.spin_length_ > 0 or self.spin_loop_

    #----------------------------------------------------------------------------
    # - Stop Spinning
    #----------------------------------------------------------------------------
    # Ceases any spinning currently active, returning the view to its true
    # rotation
    #----------------------------------------------------------------------------
    def stop_spinning(self):
        self.spin_length_ = 0
        self.spin_loop_ = False
        self.rotation = self.rotation_

    #----------------------------------------------------------------------------
    # - Tint
    #----------------------------------------------------------------------------
    # * color : destination RGB tint; uses additive blending
    # * duration : time in seconds to complete the tint
    # Gradually transitions the screen to a target tinting color
    #----------------------------------------------------------------------------
    def tint(self, color, duration):
        if self.tint_box_.fill_color != color and duration > 0:
            self.tint_color_ = color
            self.tint_length_ = math.floor(duration * settings.FPS)

    #----------------------------------------------------------------------------
    # - Fade In
    #----------------------------------------------------------------------------
    # * duration : time in seconds the fade-in will last
    # * source : initial color to fade-in from; made fully opaque
    # * destination : destination color to fade into, also settings the tint
    # Uses the screen tint functionality to mirror a fade-in from color to color
    #----------------------------------------------------------------------------
    def fade_in(self, duration, source = sf.Color(0, 0, 0, 255), destination = sf.Color(0, 0, 0, 0)):
        if duration > 0:
            source.a = 255
            self.tint_box_.fill_color = source
            self.tint(destination, duration)

    #----------------------------------------------------------------------------
    # - Fade Out
    #----------------------------------------------------------------------------
    # * duration : time in seconds the fade-out will last
    # * color : destination color to fade out to; made fully opaque
    # Uses the screen tint functionality to mirror a fade-out to color
    #----------------------------------------------------------------------------
    def fade_out(self, duration, color = sf.Color(0, 0, 0, 255)):
        color.a = 255
        self.tint(color, duration)

    #----------------------------------------------------------------------------
    # - Is Tinting
    #----------------------------------------------------------------------------
    # Returns whether the screen tint is currently transitioning
    #----------------------------------------------------------------------------
    def tinting(self):
        return self.tint_length_ > 0

    #----------------------------------------------------------------------------
    # - Flash
    #----------------------------------------------------------------------------
    # * duration : time in seconds the flashing will last, reaching peak at 1/2 t
    # * color : RGB color to flash on screen, from 0 alpha to 255 at peak, then
    #       back to zero
    #----------------------------------------------------------------------------
    def flash(self, duration, color = sf.Color(255, 255, 255, 255)):
        if duration > 0:
            color.a = 0
            self.flash_box_.fill_color = color
            self.flash_length_ = math.floor(duration * settings.FPS)
            self.flash_peak_ = math.ceil(self.flash_length_ / 2)

    #----------------------------------------------------------------------------
    # - Is Flashing
    #----------------------------------------------------------------------------
    # Returns whether the screen is currently flashing
    #----------------------------------------------------------------------------
    def flashing(self):
        return self.flash_length_ > 0

    #----------------------------------------------------------------------------
    # - Reset View (Overload)
    #----------------------------------------------------------------------------
    # * Rect : new viewing zone, top-left corcner on x,y with region size
    #       width, height
    # Overloaded to include updates for extensions, returning the screen to its
    # true center, rotation and 1.0 zoom factor, as well as ceasing any active
    # extended actions such as spinning or shaking.
    #----------------------------------------------------------------------------
    def reset(self, Rect):
        super(ViewEx, self).reset(Rect)
        self.zoom_ = 1.0
        self.set_center(self.center)
        self.set_size(Rect.size)
        self.set_rotation(self.rotation)
        self.stop_scrolling()
        self.stop_shaking()
        self.stop_spinning()
        self.stop_zooming()

    #----------------------------------------------------------------------------
    # - Draw View Overlays
    #----------------------------------------------------------------------------
    # Temporarily replaces the render window's view with a view designed to fit
    # the tint and flash screens, and draws them on the window
    #----------------------------------------------------------------------------
    def draw_overlays(self, window):
        original_view = window.view
        window.view = sf.View()

        window.draw(self.tint_box_)
        if self.flash_length_ > 0:
            window.draw(self.flash_box_)

        window.view = original_view

    #----------------------------------------------------------------------------
    # - Increment Frame
    #----------------------------------------------------------------------------
    # Updates all active screen actions, such as flashing and shaking
    #----------------------------------------------------------------------------
    def step(self):
        # Update Scrolling
        if self.scroll_length_ > 0:
            self.center_ += (self.scroll_target_ - self.center_) / self.scroll_length_
            self.center = self.center_
            self.scroll_length_ -= 1

        # Update Shaking
        if self.shake_length_ > 0 or self.shake_loop_:
            wave = self.shake_amp_ * math.sin(2 * math.pi / settings.FPS * self.shake_freq_ * self.shake_length_)
            self.shake_length_ -= 1

            # Attenuate if finite
            if not self.shake_loop_:
                wave *= self.shake_length_ / self.shake_peak_

            self.center = self.center_ + sf.Vector2(wave * (1 - self.shake_dir_), wave * self.shake_dir_)            

        # Update Zooming
        if self.zoom_length_ > 0:
            size = self.size / self.zoom_
            self.zoom_ += self.zoom_rate_
            size *= self.zoom_

            self.size = size
            self.zoom_length_ -= 1

        # Update Spinning
        if self.spin_length_ > 0 or self.spin_loop_:
            self.rotation += self.spin_speed_

            if not self.spin_loop_:
                self.spin_length_ -= 1
                if self.spin_length_ <= 0:
                    self.stop_spinning()

        # Update Tinting
        if self.tint_length_ > 0:
            increment = self.tint_box_.fill_color
            increment.r += (self.tint_color_.r - increment.r) / self.tint_length_
            increment.g += (self.tint_color_.g - increment.g) / self.tint_length_
            increment.b += (self.tint_color_.b - increment.b) / self.tint_length_
            increment.a += (self.tint_color_.a - increment.a) / self.tint_length_
            self.tint_box_.fill_color = increment
            self.tint_length_ -= 1

        # Update Flashing
        if self.flash_length_ > 0:
            flash = self.flash_box_.fill_color
            flash.a = (255.0 * (1 - abs(self.flash_length_ - self.flash_peak_) / self.flash_peak_))
            self.flash_box_.fill_color = flash
            self.flash_length_ -= 1
            
    #----------------------------------------------------------------------------
    # - Update
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

    tint_box_ = None
    flash_box_ = None

    scroll_target_ = None
    scroll_length_ = 0

    shake_amp_ = 0.0
    shake_freq_= 0.0
    shake_peak_ = 0
    shake_length_ = 0
    shake_loop_ = False
    shake_dir_ = 0

    zoom_ = 1.0
    zoom_rate_ = 0.0
    zoom_length_ = 0

    spin_speed_ = 0.0
    spin_loop_ = False
    spin_length_ = 0

    frozen = False
    speed = 1
    clock_ = 0

# Shake direction named constants
    SHAKE_HORIZONTAL = 0
    SHAKE_VERTICAL = 1
    SPIN_CLOCKWISE = -1
    SPIN_COUNTER_CLOCKWISE = 1
#================================================================================
