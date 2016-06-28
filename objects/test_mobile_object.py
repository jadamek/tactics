import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import unittest, sfml as sf, random, settings
from mobile_object import MobileObject
from map.map import Map
from map.tile import Tile

#------------------------------------------------------------------------------------
class TestMobileObject(unittest.TestCase):
#------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------
    def test_mobile_object_00_move_to(self):
    #--------------------------------------------------------------------------------
        obj = MobileObject()

        chosen = random.choice(self.triples)

        # Move according to a random pythagorean triple
        obj.moveTo(sf.Vector2(chosen[0], chosen[1]))

        self.assertEqual(obj.destination_, [sf.Vector2(chosen[0], chosen[1])], "Moving object to " + str(sf.Vector2(chosen[0], chosen[1])) + " set a destination of " + str(obj.destination_))
        self.assertEqual(obj.arrival_, chosen[2] * settings.FPS, "Moving object to " + str(sf.Vector2(chosen[0], chosen[1])) + " at " + str(settings.FPS) + " fps produced an arrival time of " + str(obj.arrival_))

        # Travel half distance
        obj.update(chosen[2] / 2.0)
        self.assertEqual(obj.destination_, [sf.Vector2(chosen[0], chosen[1])], "Moving object to " + str(sf.Vector2(chosen[0], chosen[1])) + " at " + str(obj.position) + " now has a destination of " + str(obj.destination_))
        
        # Complete travel - overshoot by a fraction to account for float issues.
        obj.update(chosen[2] / 1.9)
        self.assertEqual(obj.destination_, [], "Travelled object at " + str(obj.position) + " still has a destination of " + str(obj.destination_))                
    
    #--------------------------------------------------------------------------------
    def test_mobile_object_01_move_along(self):
    #--------------------------------------------------------------------------------
        obj = MobileObject()

        x = random.randint(1, 100)
        y = random.randint(1, 100)
        path = [sf.Vector2(x, 0), sf.Vector2(x, y)]

        # Move according to a pair of random aligned points (an L shape)
        obj.moveAlong(path)

        self.assertEqual(obj.destination_, path, "Moving object along " + str(path) + " set a destination of " + str(obj.destination_))
        self.assertEqual(obj.arrival_, x * settings.FPS, "Moving object along " + str(path) + " from " + str(obj.position) + " at " + str(settings.FPS) + " fps produced an arrival time of " + str(obj.arrival_) + ", not " + str(x * settings.FPS))

        # Stop just short
        obj.update((obj.arrival_ - 1) / settings.FPS)
        self.assertEqual(obj.destination_, path, "Moving object along " + str(path) + " at " + str(obj.position) + " now has a destination of " + str(obj.destination_))
        
        # Finish Journey
        obj.update(1 / settings.FPS)
        self.assertEqual(obj.destination_, path, "Moving object along " + str(path) + " set a destination of " + str(obj.destination_))
        self.assertEqual(obj.destination_, path, "Moving object along " + str(path) + " after passing first point, at " + str(obj.position) + " now has a destination of " + str(obj.destination_))
        self.assertEqual(obj.arrival_, y * settings.FPS, "Moving object along " + str(path) + " from " + str(obj.position) + " at " + str(settings.FPS) + " fps produced an arrival time of " + str(obj.arrival_) + ", not " + str(y * settings.FPS))

#--------------------------------------------------------------------------------
    def test_mobile_object_02_speed(self):
    #--------------------------------------------------------------------------------
        obj = MobileObject()
        chosen = random.choice(self.triples)

        # Move according to a random pythagorean triple
        obj.moveTo(sf.Vector2(chosen[0], chosen[1]))
        obj.update(chosen[2] + 0.1)

        # Faster Journey
        obj.moveTo(sf.Vector2())
        obj.speed = float(random.randint(1, 5))
        
        self.assertEqual(obj.destination_, [sf.Vector2()], "Moving object back to %s with a speed of %f set a destination of %s" % (sf.Vector2(), obj.speed, obj.destination_))
        self.assertEqual(obj.arrival_, chosen[2] * settings.FPS, "Moving object back to %s with a speed of %f at %f fps produced an arrival time of %d" % (sf.Vector2(), obj.speed, settings.FPS, obj.arrival_))
        
        # Stop just short
        obj.update(chosen[2] / obj.speed - 0.1)
        self.assertEqual(obj.destination_, [sf.Vector2()], "Moving object to %s with a speed of %f at %s now has a destination of %s" % (sf.Vector2(chosen[0], chosen[1]), obj.speed, obj.position, obj.destination_))
        
        # Finish Journey
        obj.update(0.2)
        self.assertEqual(obj.destination_, [], "Arrived object at %s with speed %f still has a destination of %s" % (obj.position, obj.speed, obj.destination_))

        # Move back to chosen spot
        obj.speed = 1.0
        obj.moveTo(sf.Vector2(chosen[0], chosen[1]))
        obj.update(chosen[2] + 0.1)

        # Slower Journey
        obj.moveTo(sf.Vector2())
        obj.speed = random.choice([0.5, 0.25, 0.2, 0.125]) #1/2, 1/4, 1/5, 1/8
        
        # Stop short
        obj.update(chosen[2] / obj.speed - 1)
        self.assertEqual(obj.destination_, [sf.Vector2()], "Moving object to %s with a speed of %f at %s now has a destination of %s" % (sf.Vector2(chosen[0], chosen[1]), obj.speed, obj.position, obj.destination_))
        
        # Finish Journey
        obj.update(1.2)
        self.assertEqual(obj.destination_, [], "Arrived object at %s with speed %f still has a destination of %s" % (obj.position, obj.speed, obj.destination_))

    #--------------------------------------------------------------------------------
    def test_mobile_object_03_grounded(self):
    #--------------------------------------------------------------------------------
        obj = MobileObject()

        # Default ground is None
        self.assertEqual(obj.ground, None, "Default constructed mobile object has ground %s" % (obj.ground))

        x = random.randint(1, 100)
        z = random.randint(-100, 100)
        obj.set_position(sf.Vector3(0, 0, z))

        # An object with no ground should retain the same z throughout motion
        obj.moveTo(sf.Vector2(x, 0))
        for i in range(x * 10 + 1):
            self.assertEqual(obj.position.z, z, "Floating object changed its z from %f to %f at %s" % (z, obj.position.z, obj.position))
            obj.update(0.1)

        map = Map(2, 2)

        # Setup map of three tiles 
        tile1 = Tile(None, 5)
        tile2 = Tile(None, 3)
        tile3 = Tile(None, 10)
        
        map.place(tile1, 0, 0)
        map.place(tile2, 0, 1)
        map.place(tile3, 1, 1)

        # Object initialized with ground should be start at height of 0,0 tile-space
        obj = MobileObject(map)
        self.assertEqual(obj.ground, map, "Constructed mobile object with ground map, but found %s instead" % (obj.ground))
        self.assertEqual(obj.position.z, 5, "Constructed mobile object onto tile1 with height %f, but initial z-coordinate is %f" % (tile1.height, obj.position.z))

        # Move once around the map
        obj.moveAlong([sf.Vector2(0, 1), sf.Vector2(1, 1), sf.Vector2(1, 0), sf.Vector2(0, 0)])

        # Move to first point (0, 1)
        obj.update(1.0)
        self.assertEqual(obj.position.z, 3, "Object move to ~(0, 1) with height %f, but has z-coordinate %f" % (tile2.height, obj.position.z))

        # Move to second point (1, 1)
        obj.update(1.0)
        self.assertEqual(obj.position.z, 10, "Object move to ~(0, 1) with height %f, but has z-coordinate %f" % (tile2.height, obj.position.z))

        # Move to final point (1, 0), which is blank and should cause the object to 'float' : retain its z-coordinate
        obj.update(1.0)
        self.assertEqual(obj.position.z, 10, "Object move to ~(0, 1) with height %f, but has z-coordinate %f" % (tile2.height, obj.position.z))

    #--------------------------------------------------------------------------------
    def test_mobile_object_04_stop_motion(self):
    #--------------------------------------------------------------------------------
        obj = MobileObject()
    
        self.assertFalse(obj.moving(), "Newly constructed object initialized as moving.")

        obj.moveTo(sf.Vector2(random.randint(1, 100), random.randint(1, 100)))
        self.assertTrue(obj.moving(), "Object with destination %s and arrival time %d is not moving" % (obj.destination_, obj.arrival_))

        obj.stop_moving()
        self.assertEqual(obj.destination_, [], "Recently halted object has destination %s" % (obj.destination_))
        self.assertEqual(obj.arrival_, 0, "Recently halted object has arrival %d" % (obj.arrival_))
        self.assertFalse(obj.moving(), "Recently halted object is moving.")

    # Constants
    triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (7, 24, 25), (8, 15, 17)]