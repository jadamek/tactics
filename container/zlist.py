import sfml as sf

#================================================================================
class ZNode:
#================================================================================
# Represents a single sortable node in the Z-indexing list.
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Z-Node Contructor
    #----------------------------------------------------------------------------
    # * target : Z-Object this node handles
    # * left : Z-Node to the left (lower priority) of this one
    # * right : Z-Node to the right (higher priority) of this one 
    #----------------------------------------------------------------------------
    def __init__(self, target = None, left = None, right = None):
        self.target = target
        self.prev = left
        self.next = right
                
        if self.target != None and target != "head":
            self.target.handler = self
            
    #----------------------------------------------------------------------------
    # - Attach
    #----------------------------------------------------------------------------
    # * left : Z-Node to become the left (lower priority) of this one
    # * right : Z-Node to become the right (higher priority) of this one
    # Inserts a this Z-Node between a pair of two other Z-Nodes.
    #----------------------------------------------------------------------------
    def attach(self, left = None, right = None):
        self.prev = left
        self.next = right

        if self.prev != None:
            self.prev.next = self
            
        if self.next != None:
            self.next.prev = self
            
    #----------------------------------------------------------------------------
    # - Detach
    #----------------------------------------------------------------------------
    # Detaches this Z-Node from its two neighboring Z-Nodes.
    #----------------------------------------------------------------------------
    def detach(self):
        if self.prev != None:
            self.prev.next = self.next
            
        if self.next != None:
            self.next.prev = self.prev
    
        self.prev = None
        self.next = None
               
    #----------------------------------------------------------------------------
    # - Reattach
    #----------------------------------------------------------------------------
    # * left : Z-Node to become the left (lower priority) of this one
    # * right : Z-Node to become the right (higher priority) of this one
    # Inserts a this Z-Node between a pair of two other Z-Nodes after detaching
    # it from its two currently neighboring Z-Nodes.    
    #----------------------------------------------------------------------------
    def reattach(self, left = None, right = None):
        self.detach()
        self.attach(left, right)

    #----------------------------------------------------------------------------
    # - Sort Up (Right)
    #----------------------------------------------------------------------------
    # Iterates rightward, attaching this node to the first with a higher priority
    #----------------------------------------------------------------------------
    def sortUp(self):
        seeker = self.next

        if seeker != None:
            while True:
                if self.target <= seeker.target:
                    if seeker is not self.next:
                        self.reattach(seeker.prev, seeker)                                
                    break
                elif seeker.next is None:
                    self.reattach(seeker)
                    break
                else:
                    seeker = seeker.next
                    
    #----------------------------------------------------------------------------
    # - Sort Down (left)
    #----------------------------------------------------------------------------
    # Iterates leftward, attaching this node to the first with a lower priority
    #----------------------------------------------------------------------------
    def sortDown(self):
        seeker = self.prev

        while seeker.prev != None:
            if self.target >= seeker.target:
                break
            seeker = seeker.prev
            
        if seeker is not self.prev:
            self.reattach(seeker, seeker.next)        

# Members
    target = None
    prev = None
    next = None
#================================================================================

#================================================================================
class ZList:
#================================================================================
# Represents a list of drawable objects sorted by a given z-indexing criteria
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Front
    #----------------------------------------------------------------------------
    # Retrieves the first real node of the list, which is always next neighbor of
    # the head node.
    #----------------------------------------------------------------------------
    def front(self):
        return self.head.next
        
    #----------------------------------------------------------------------------
    # - Is Empty?
    #----------------------------------------------------------------------------
    def empty(self):
        return self.head.next == None

    #----------------------------------------------------------------------------
    # - Add Object
    #----------------------------------------------------------------------------
    # * drawable : Z-Object to be added to this index-sorting list
    # Adds a Z-Object to the list into its sorted placement.
    #----------------------------------------------------------------------------
    def add(self, drawable):
        node = ZNode(drawable, self.head, self.front())                
        node.attach(self.head, self.front())
        self.front().sortUp()

    #----------------------------------------------------------------------------
    # - Clear List
    #----------------------------------------------------------------------------
    def clear(self):
        self.head.next = None

# Members
    head = ZNode("head")
#================================================================================

#================================================================================
class ZObject(sf.Drawable):
#================================================================================
# Represents a drawable object in the Z-indexing space.
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Z-Object Contructor
    #----------------------------------------------------------------------------
    def __init__(self):
        sf.Drawable.__init__(self)
    
    #----------------------------------------------------------------------------
    # - Z-Object Destructor
    #----------------------------------------------------------------------------
    def __del__(self):
        # Detach this object from any ZList it was a part of.
        if self.handler != None:
            self.handler.detach()
            self.handler = None            
    
# Members
    handler = None
#================================================================================
    