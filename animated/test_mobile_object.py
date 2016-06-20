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

        triples = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (7, 24, 25), (8, 15, 17)]
        chosen = random.sample(triples, 2)

        # Move according to a random pythagorean triple
        obj.moveTo(sf.Vector2(chosen[0][0], chosen[0][1]))

        self.assertEqual(obj.destination_, [sf.Vector2(chosen[0][0], chosen[0][1])], "Moving object to " + str(sf.Vector2(chosen[0][0], chosen[0][1])) + " set a destination of " + str(obj.destination_))
        self.assertEqual(obj.arrival_, chosen[0][2] * settings.FPS, "Moving object to " + str(sf.Vector2(chosen[0][0], chosen[0][1])) + " at " + str(settings.FPS) + " fps produced an arrival time of " + str(obj.arrival_))

