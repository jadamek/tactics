from zlist import *
import unittest, random, copy

#------------------------------------------------------------------------------------
class DummyObject(ZObject):
#------------------------------------------------------------------------------------
# - Simple Z-Object with an integer ID for testing purposes.
#------------------------------------------------------------------------------------        
    id = 1
    
    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id
        
    def __le__(self, other):
        return not self.__gt__(other)
        
    def __ge__(self, other):
        return not self.__lt__(other)
        
#------------------------------------------------------------------------------------
class TestZList(unittest.TestCase):
#------------------------------------------------------------------------------------
    def setUp(self):
        self.zlist = ZList()
        
    def tearDown(self):
        self.zlist.clear()
        
    #--------------------------------------------------------------------------------
    def test_zlist_00_list_initialization(self):
    #--------------------------------------------------------------------------------        
        self.assertEqual(self.zlist.head.target, "head", "List initialized without a 'head' pseudo-node.")
        self.assertEqual(self.zlist.front(), None, "List initialized with a real front node.")
        self.assertTrue(self.zlist.empty(), "List initialized with no head node, but list is not empty.")
        
    #--------------------------------------------------------------------------------
    def test_zlist_01_zobject_initial_addition(self):
    #--------------------------------------------------------------------------------
        zobj = DummyObject()
        self.assertEqual(zobj.id, 1, "Failed to create a dummy z-object with ID 1.")
        
        # Add to list
        self.zlist.add(zobj)
        self.assertFalse(self.zlist.empty(), "Added object to list, list is still empty.")
        
        # Test that a node was properly created
        self.assertEqual(self.zlist.front().target.id, 1, "Added object to empty list, but head node's target does not have the correct ID.")
        self.assertEqual(self.zlist.front().prev, self.zlist.head, "Added object to front of list, but front node's left neighbor is not 'head'.")
        self.assertEqual(self.zlist.front().next, None, "Added object to empty list, but front node has a right neighbor.")        

    #--------------------------------------------------------------------------------
    def test_zlist_02_zobject_compound_addition(self):
    #--------------------------------------------------------------------------------
        zobj1 = DummyObject()
        zobj2 = DummyObject()
        zobj2.id = 2
        zobj3 = DummyObject()
        zobj3.id = 3
                
        # Add to list
        self.zlist.add(zobj3)
        self.zlist.add(zobj2)
        self.assertFalse(self.zlist.empty(), "Added objects to list, list is still empty.")
        
        # Test that a new head node was properly inserted
        self.assertEqual(self.zlist.front().target.id, 2, "Added object to front of list, but front node's target does not have the correct ID.")
        self.assertEqual(self.zlist.front().prev, self.zlist.head, "Added object to front of list, but front node's left neighbor is not 'head'.")
        self.assertEqual(self.zlist.front().next.target.id, 3, "Added object to front of list, but front node's right neighbor is not object with ID => 3.")
        
        # Add to list
        self.zlist.add(zobj1)
        
        # Test that a new head node was properly inserted
        self.assertEqual(self.zlist.front().target.id, 1, "Added object to front of list, but front node's target does not have the correct ID.")
        self.assertEqual(self.zlist.front().prev, self.zlist.head, "Added object to front of list, but front node's left neighbor is not 'head'.")
        self.assertEqual(self.zlist.front().next.target.id, 2, "Added object to front of list, but front node's right neighbor is not object with ID => 2.") 
        
        # List should now be: 1, 2, 3
        current = self.zlist.front()
        currentID = 1
        
        while current != None:
            self.assertEqual(current.target.id, currentID, "Object should have current id of " + str(currentID) + ", but has ID " + str(current.target.id) + " instead.")
            current = current.next
            currentID += 1
            
    #--------------------------------------------------------------------------------
    def test_zlist_03_clear(self):
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
        
    #--------------------------------------------------------------------------------
    def test_zlist_04_sorts_properly_on_insert(self):
    #--------------------------------------------------------------------------------
        # Randomly generate 100 nodes with random IDs to populate the list
        for i in range(100):
            obj = DummyObject()
            obj.id = random.randint(1, 100000)

            self.zlist.add(obj)
            
        # List should contain 100 elements sorted by ascending ID
        current = self.zlist.front()
        count = 0
        
        while current != None:
            if current.prev.target != "head":
                self.assertTrue(current.prev.target.id <= current.target.id, "Node<" + str(current.prev.target.id) + "> not <= Node<" + str(current.target.id) + ">")

            if current.next != None:
                self.assertTrue(current.target.id <= current.next.target.id, "Node<" + str(current.target.id) + "> not <= Node<" + str(current.next.target.id) + ">")

            current = current.next
            count += 1
            
        self.assertEqual(count, 100, "List should contain 100 elements, but contains " + str(count) + " instead.")
        
    #--------------------------------------------------------------------------------
    def test_zlist_05_update_indexing(self):
    #--------------------------------------------------------------------------------
        # Randomly generate 10 nodes with random IDs (1~100) to populate the list
        for i in range(10):
            obj = DummyObject()
            obj.id = random.randint(1, 100)

            self.zlist.add(obj)
            
        # Add an object with random ID that is also 1~100
        discontent = DummyObject
        discontent.id = random.randint(1, 100)
        
        self.zlist.add(discontent)
        node = discontent.handler
        
        if node.prev.target != "head":
            self.assertTrue(node.prev.target.id <= node.target.id, "Node<" + str(node.prev.target.id) + "> not <= Node<" + str(node.target.id) + ">")

        if node.next != None:
            self.assertTrue(node.target.id <= node.next.target.id, "Node<" + str(node.target.id) + "> not <= Node<" + str(node.next.target.id) + ">")
        
        # Perturb to lower than the lowest possible node in the list.
        discontent.id -= 100
        
        # Should not be sorted *yet*
        if node.prev.target != "head":
            self.assertFalse(node.prev.target.id <= node.target.id, "Node<" + str(node.prev.target.id) + "> <= Node<" + str(node.target.id) + ">")
            
        # Report the perturbation - should reside at front of list
        node.sortDown()
        self.assertEqual(node, self.zlist.front(), "Node with ID => " + str(discontent.id) + " is not at the front of the list")
        self.assertTrue(node.target.id <= node.next.target.id, "Node<" + str(node.target.id) + "> not <= Node<" + str(node.next.target.id) + ">")
        
        # Perturb to higher than the highest possible node in the list.
        discontent.id += 200
        
        # Should not be sorted *yet*
        self.assertFalse(node.target.id <= node.next.target.id, "Node<" + str(node.target.id) + "> <= Node<" + str(node.next.target.id) + ">")
            
        # Report the perturbation - should reside at end of list
        node.sortUp()
        self.assertEqual(node.next, None, "Node with ID => " + str(discontent.id) + " is not at the end of the list")
        self.assertTrue(node.prev.target.id <= node.target.id, "Node<" + str(node.prev.target.id) + "> not <= Node<" + str(node.target.id) + ">")
        
        # Perturn to just 1 higher than the front node. Should reside around 2nd place
        discontent.id = self.zlist.front().target.id + 1
        node.sortDown()
        self.assertTrue(node.prev.target.id <= node.target.id, "Node<" + str(node.prev.target.id) + "> not <= Node<" + str(node.target.id) + ">")
        self.assertTrue(node.target.id <= node.next.target.id, "Node<" + str(node.target.id) + "> not <= Node<" + str(node.next.target.id) + ">")
        
    zlist = None
    
    #--------------------------------------------------------------------------------
    def test_zlist_06_zobject_ordering(self):
    #--------------------------------------------------------------------------------
        obj1 = ZObject()
        obj2 = ZObject()
        
        obj1.position.x = random.randint(-100, 100)
        obj1.position.y = random.randint(-100, 100)
        obj1.position.z = random.randint(-100, 100)

        # Equivalent points are reflexive
        obj2.position = copy.copy(obj1.position)        
        self.assertEqual(obj1 < obj2, obj1 > obj2, "Objects with positions <" + str(obj1.position) + "> and <" + str(obj2.position) + "> were not found to reflexively compare.")
        
        # Higher z is higher priority
        obj2.position.z += 50
        self.assertGreater(obj2, obj1, "Object with position <" + str(obj2.position) + "> was not found greater than <" + str(obj1.position) + ">")
        
        # Higher x + y sum is higher priority, and supercedes any comparison of z-coordinate
        obj1.position.y += 50
        self.assertGreater(obj1, obj2, "Object with position <" + str(obj1.position) + "> was not found greater than <" + str(obj2.position) + ">")        
        obj2.position.x += 80
        self.assertGreater(obj2, obj1, "Object with position <" + str(obj2.position) + "> was not found greater than <" + str(obj1.position) + ">")
#================================================================================
 
if __name__ == "__main__":
    unittest.main(verbosity = 2)