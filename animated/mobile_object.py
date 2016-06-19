import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../container")

from zlist import ZObject
import sfml as sf
import math
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
    def __init__(self):
        ZObject.__init__(self)
        self.speed = 1
        self.fps = 1
        self.frozen = False
        self.destination_ = []
        self.clock_ = 0.0
        self.arrival_ = 0

    #----------------------------------------------------------------------------
    # Move Linearly To Position
    #----------------------------------------------------------------------------
    # * destination : position the object will eventually arrive at
    #----------------------------------------------------------------------------
    def moveTo(self, position):
        self.destination_ = [position]
        self.arrival_ = self.compute_arrival(position)

    #----------------------------------------------------------------------------
    # Move Along a Path
    #----------------------------------------------------------------------------
    # * path : a list of consecutive destinations
    #----------------------------------------------------------------------------
    def moveTo(self, path):
        if type(path) is list:
            self.destination_ = path
            self.arrival_ = self.compute_arrival(path[0])

    #----------------------------------------------------------------------------
    # Increment Frame
    #----------------------------------------------------------------------------
    def step(self):
        if len(self.destination_) > 0:
            self.position = self.position + (destination[0] - self.position) / self.arrival_
            self.arrival_ -= 1

            if position is self.destination[0]:
                self.destination_.pop(0)                    

                if len(self.destination) > 0:
                    self.arrival_ = self.compute_arrival(destination[0])

    #----------------------------------------------------------------------------
    # Update
    #----------------------------------------------------------------------------
    # * elapsed : relative time passed since last update
    #----------------------------------------------------------------------------
    def update(self, elapsed):
        if not self.frozen:
            self.clock_ += elapsed
            while self.clock_ > 1.0 / fps:
                self.step()
                self.clock_ -= 1.0 / fps

    #----------------------------------------------------------------------------
    # Compute Arrival (private)
    #----------------------------------------------------------------------------
    # * destination : final destination by which to compute total travel distance
    #----------------------------------------------------------------------------
    def compute_arrival(self, destination):
        distance = math.sqrt((destination.x - self.position.x) ** 2 + (destination.y - self.position.y) ** 2)
        return int(math.ceil(distance / self.speed * self.fps))

# Members
    speed = 1
    fps = 1
    frozen = False
    destination_ = None
    arrival_ = 0
    clock_ = 0
#================================================================================
