import sfml as sf

#================================================================================
class Rectangle(sf.Rectangle):
#================================================================================
# Overload for SFML Rectangle class which contains a bug
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # Rectangle constructor (Overload)
    #----------------------------------------------------------------------------
    def __init__(self, x, y, w, h):
        sf.Rectangle.__init__(self, sf.Vector2(x, y), sf.Vector2(w, h))

    #----------------------------------------------------------------------------
    # Compute Intersection
    #----------------------------------------------------------------------------
    # * rectangle : a rectangle by which to compare intersecting areas with
    # Returns the rectangle intersection of this rectangle and another, or None
    #----------------------------------------------------------------------------
    def intersects(self, rectangle):
        # make sure the rectangle is a rectangle (to get its right/bottom border)
        l, t, w, h = rectangle
        rectangle = Rectangle(l, t, w, h)

        # compute the intersection boundaries
        left = max(self.left, rectangle.left)
        top = max(self.top, rectangle.top)
        right = min(self.right, rectangle.right)
        bottom = min(self.bottom, rectangle.bottom)

        # if the intersection is valid (positive non zero area), then
        # there is an intersection
        if left < right and top < bottom:
            return Rectangle(left, top, right-left, bottom-top)
#================================================================================
