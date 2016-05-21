import sfml as sf

#================================================================================
class ZList:
#================================================================================
# Represents a list of drawable objects sorted by a given z-indexing criteria
#================================================================================
# Methods
    #----------------------------------------------------------------------------
    # - Is Empty?
    #----------------------------------------------------------------------------
    def empty(self):
        return self.head == None

    #----------------------------------------------------------------------------
    # - Add Object
    #----------------------------------------------------------------------------
    # * drawable : Z-Object to be added to this index-sorting list
    # Adds a Z-Object to the list into its sorted placement.
    #----------------------------------------------------------------------------
    def add(self, drawable):
        node = ZNode(drawable)
        
        if self.head != None:
            node.attach(None, self.head)            
        self.head = node
        # TODO: SORT

    #----------------------------------------------------------------------------
    # - Clear List
    #----------------------------------------------------------------------------
    def clear(self):
        self.head = None

# Members
    head = None
#================================================================================


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
                
        if self.target != None:
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
        
# Members
    target = None
    prev = None
    next = None
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
    