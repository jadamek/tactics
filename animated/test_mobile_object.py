import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

import unittest, sfml as sf, random, settings
from mobile_object import MobileObject

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
    def test_mobile_object_01_speed(self):
    #--------------------------------------------------------------------------------
        obj = MobileObject()
        chosen = random.choice(self.triples)

        # Move according to a random pythagorean triple
        obj.moveTo(sf.Vector2(chosen[0], chosen[1]))
        obj.update(chosen[2] + 0.1)

        # Faster Journey
        obj.moveTo(sf.Vector2())
        obj.speed = float(random.randint(1, 5))
        
        self.assertEqual(obj.destination_, [sf.Vector2()], "Moving object back to " + str(sf.Vector2()) + " set a destination of " + str(obj.destination_))
        self.assertEqual(obj.arrival_, chosen[2] * settings.FPS, "Moving object back to " + str(sf.Vector2()) + " with a speed of " + str(obj.speed) + " at " + str(settings.FPS) + " fps produced an arrival time of " + str(obj.arrival_))
        
        # Stop just short
        obj.update(chosen[2] / obj.speed - 0.1)
        self.assertEqual(obj.destination_, [sf.Vector2()], "Moving object to " + str(sf.Vector2(chosen[0], chosen[1])) + " at " + str(obj.position) + " now has a destination of " + str(obj.destination_))
        
        # Finish Journey
        obj.update(0.2)
        self.assertEqual(obj.destination_, [], "Travelled object at " + str(obj.position) + " still has a destination of " + str(obj.destination_))

        # Move back to chosen spot
        obj.speed = 1.0
        obj.moveTo(sf.Vector2(chosen[0], chosen[1]))
        obj.update(chosen[2] + 0.1)

        # Slower Journey
        obj.moveTo(sf.Vector2())
        obj.speed = random.choice([0.5, 0.25, 0.2, 0.125]) #1/2, 1/4, 1/5, 1/8
        
        # Stop short
        obj.update(chosen[2] / obj.speed - 1)
        self.assertEqual(obj.destination_, [sf.Vector2()], "Moving object to " + str(sf.Vector2(chosen[0], chosen[1])) + " with a speed of " + str(obj.speed) + " at " + str(obj.position) + " now has a destination of " + str(obj.destination_))
        
        # Finish Journey
        obj.update(1.2)
        self.assertEqual(obj.destination_, [], "Travelled object at " + str(obj.position) + " still has a destination of " + str(obj.destination_))

    #--------------------------------------------------------------------------------
    def test_mobile_object_02_move_along(self):
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

    # Constants
    triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (7, 24, 25), (8, 15, 17)]