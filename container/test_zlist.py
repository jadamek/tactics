from zlist import *
import unittest, sfml as sf

#------------------------------------------------------------------------------------
class DummyObject(ZObject):
#------------------------------------------------------------------------------------
# - Simple Z-Object with an integer ID for testing purposes.
#------------------------------------------------------------------------------------        
    id = 1

#------------------------------------------------------------------------------------
class TestZList(unittest.TestCase):
#------------------------------------------------------------------------------------
    def setUp(self):
        self.zlist = ZList()                
        
    #--------------------------------------------------------------------------------
    def test_00_zlist_list_initialization(self):
    #--------------------------------------------------------------------------------        
        self.assertEqual(self.zlist.head, None, "List initialized with some head node.")
        self.assertTrue(self.zlist.empty(), "List initialized with no head node, but list is not empty.")
        
    #--------------------------------------------------------------------------------
    def test_01_zlist_zobject_initial_addition(self):
    #--------------------------------------------------------------------------------
        zobj = DummyObject()
        self.assertEqual(zobj.id, 1, "Failed to create a dummy z-object with ID 1.")
        
        # Add to list
        self.zlist.add(zobj)
        self.assertFalse(self.zlist.empty(), "Added object to list, list is still empty.")
        
        # Test that a node was properly created
        self.assertEqual(self.zlist.head.target.id, 1, "Added object to empty list, but head node's target does not have the correct ID.")
        self.assertEqual(self.zlist.head.prev, None, "Added object to empty list, but head node has a left neighbor.")
        self.assertEqual(self.zlist.head.next, None, "Added object to empty list, but head node has a right neighbor.")        

    #--------------------------------------------------------------------------------
    def test_02_zlist_zobject_compound_addition(self):
    #--------------------------------------------------------------------------------
        zobj1 = DummyObject()
        zobj2 = DummyObject()
        zobj2.id = 2
        zobj3 = DummyObject()
        zobj3.id = 3
                
        # Add to list
        self.zlist.add(zobj1)
        self.zlist.add(zobj2)
        self.assertFalse(self.zlist.empty(), "Added objects to list, list is still empty.")
        
        # Test that a new head node was properly inserted
        self.assertEqual(self.zlist.head.target.id, 2, "Added object to front of list, but head node's target does not have the correct ID.")
        self.assertEqual(self.zlist.head.prev, None, "Added object to front of list, but head node has a left neighbor.")
        self.assertEqual(self.zlist.head.next.target.id, 1, "Added object to front of list, but head node's right neighbor is not object with ID => 1.")
        
        # Add to list
        self.zlist.add(zobj3)
        
        # Test that a new head node was properly inserted
        self.assertEqual(self.zlist.head.target.id, 3, "Added object to front of list, but head node's target does not have the correct ID.")
        self.assertEqual(self.zlist.head.prev, None, "Added object to front of list, but head node has a left neighbor.")
        self.assertEqual(self.zlist.head.next.target.id, 2, "Added object to front of list, but head node's right neighbor is not object with ID => 2.")  
        
        # List should now be: 3, 2, 1
        current = self.zlist.head
        currentID = 3
        
        while current != None:
            self.assertEqual(current.target.id, currentID, "Object should have current id of " + str(currentID) + ", but has ID " + str(current.target.id) + " instead.")
            current = current.next
            currentID -= 1
            
    #--------------------------------------------------------------------------------
    def test_03_zlist_clear(self):
    #--------------------------------------------------------------------------------
        zobj1 = DummyObject()
        zobj2 = DummyObject()
        zobj2.id = 2
        zobj3 = DummyObject()
        zobj3.id = 3
                
        # Add to list
        self.zlist.add(zobj1)
        self.zlist.add(zobj2)
        self.zlist.add(zobj3)
        self.assertFalse(self.zlist.empty(), "Added objects to list, list is still empty.")
        
        # Clear list
        self.zlist.clear()
        self.assertTrue(self.zlist.empty(), "Cleared list, but list is not empty.")
        
    zlist = None
        
if __name__ == "__main__":
    unittest.main(verbosity = 2)