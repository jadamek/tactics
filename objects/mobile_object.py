import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import sfml as sf, math, settings
from container.zlist import ZObject
from functools import partial

#================================================================================
class MobileObject(ZObject):
#================================================================================
# Represents a visual object which moves per-pixel through relative time
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # Mobile Object Constructor
    #----------------------------------------------------------------------------
    # * ground : height map which the object's z-coodinate will be bound to
    #----------------------------------------------------------------------------
    def __init__(self, ground = None):
        ZObject.__init__(self)
        self.speed = 1
        self.frozen = False
        self.ground = ground
        self.destination_ = []
        self.clock_ = 0.0
        self.arrival_ = 0
        
        if ground is not None:
            self.set_position(sf.Vector3(0, 0, ground.height(0, 0)))

    #----------------------------------------------------------------------------
    # Move Linearly To Position
    #----------------------------------------------------------------------------
    # * destination : position the object will eventually arrive at
    # Sets the object's target destination to a single location
    #----------------------------------------------------------------------------
    def moveTo(self, position):
        self.destination_ = [position]
        self.arrival_ = self.compute_arrival(position)

    #----------------------------------------------------------------------------
    # Move Along a Path
    #----------------------------------------------------------------------------
    # * path : a list of consecutive destinations
    # Sets the object's destination as a path, or list of consecutive locations
    #----------------------------------------------------------------------------
    def moveAlong(self, path):
        if type(path) is list:
            self.destination_ = path
            self.arrival_ = self.compute_arrival(path[0])

    #----------------------------------------------------------------------------
    # Increment Frame
    #----------------------------------------------------------------------------
    # Propagates the object's motion along a height map, or 'ground'
    #----------------------------------------------------------------------------
    def step(self):
        if len(self.destination_) > 0:
            if self.arrival_ > 0:         
                x = self.position.x + (self.destination_[0].x - self.position.x) / float(self.arrival_)
                y = self.position.y + (self.destination_[0].y - self.position.y) / float(self.arrival_)
                z = self.ground.height(x, y) if self.ground is not None else self.position.z
                if z is None: z = self.position.z

                self.set_position(sf.Vector3(x, y, z))
                self.arrival_ -= 1

            if self.arrival_ == 0:
                self.destination_.pop(0)                    

                if len(self.destination_) > 0:
                    self.arrival_ = self.compute_arrival(self.destination_[0])

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

    #----------------------------------------------------------------------------
    # Compute Arrival (private)
    #----------------------------------------------------------------------------
    # * destination : final destination by which to compute total travel distance
    #----------------------------------------------------------------------------
    def compute_arrival(self, destination):
        distance = math.sqrt((destination.x - self.position.x) ** 2 + (destination.y - self.position.y) ** 2)
        return int(math.ceil(distance * settings.FPS))

    #----------------------------------------------------------------------------
    # Is Object Moving?
    #----------------------------------------------------------------------------
    def moving(self):
        return len(self.destination_) > 0

    #----------------------------------------------------------------------------
    # Stop Moving
    #----------------------------------------------------------------------------
    # Cancels current destination and motion
    #----------------------------------------------------------------------------
    def stop_moving(self):
        self.destination_ = []
        self.arrival_ = 0

# Members
    speed = 1
    frozen = False
    ground = None
    destination_ = None
    arrival_ = 0
    clock_ = 0
#================================================================================
