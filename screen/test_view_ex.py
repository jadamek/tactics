import unittest, sfml as sf, random
from view_ex import ViewEx

#------------------------------------------------------------------------------------
class TestViewEx(unittest.TestCase):
#------------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------
    def test_view_ex_00_construction(self):
    #--------------------------------------------------------------------------------
        # Default construction
        view = ViewEx()
        self.assertEqual(view.center, sf.Vector2(320, 240), "Defaultly constructed view should be centered on %s, not %s" % (sf.Vector2(320, 240), view.center))
        self.assertEqual(view.center_, sf.Vector2(320, 240), "Defaultly constructed view should be truly centered on %s, not %s" % (sf.Vector2(320, 240), view.center_))
        self.assertEqual(view.size, sf.Vector2(640, 480), "Defaultly constructed view should have a size of %s, not %s" % (sf.Vector2(640, 480), view.size))
        self.assertEqual(view.rotation, 0.0, "Defaultly constructed view should be rotated at %f degrees, not %f degrees" % (0.0, view.rotation))
        self.assertEqual(view.rotation_, 0.0, "Defaultly constructed view should be truly rotated at %f degrees, not %f degrees" % (0.0, view.rotation_))
        self.assertEqual(view.zoom_, 1.0, "Defaultly constructed view should have an initial scale/zoom factor of %f, not %f" % (1.0, view.zoom_))

        # Constructed by Rectangle
        wide_screen = sf.Rectangle(sf.Vector2(100, 100), sf.Vector2(1280, 720))
        view = ViewEx(wide_screen)
        self.assertEqual(view.center, sf.Vector2(740, 460), "View constructed with zone %s should be centered on %s, not %s" % (wide_screen, sf.Vector2(740, 460), view.center))
        self.assertEqual(view.center_, sf.Vector2(740, 460), "View constructed with zone %s should be truly centered on %s, not %s" % (wide_screen, sf.Vector2(740, 460), view.center_))
        self.assertEqual(view.size, sf.Vector2(1280, 720), "View constructed with zone %s should have a size of %s, not %s" % (wide_screen, sf.Vector2(1280, 720), view.size))

    #--------------------------------------------------------------------------------
    def test_view_ex_01_move(self):
    #--------------------------------------------------------------------------------
        view = ViewEx(sf.Rectangle(sf.Vector2(random.randint(1001, 10000), random.randint(1001, 10000)), sf.Vector2(640, 680)))        
        center = sf.Vector2(random.randint(-1000, 1000), random.randint(-1000, 1000))

        # Set center to given coordinate
        view.set_center(center)
        self.assertEqual(view.center_, center, "View set to center %s should be centered on %s, not %s" % (center, center, view.center_))
        self.assertEqual(view.center, center, "View set to center %s should be truly centered on %s, not %s" % (center, center, view.center))

        # Move center by a specified offset
        offset = sf.Vector2(random.randint(-1000, 1000), random.randint(-1000, 1000))
        view.move(offset)
        self.assertEqual(view.center_, center + offset, "Moving view by %s from %s should center it at %s, not %s" % (offset, center, center + offset, view.center_))
        self.assertEqual(view.center, center + offset, "Moving view by %s from %s should truly center it at %s, not %s" % (offset, center, center + offset, view.center))

    #--------------------------------------------------------------------------------
    def test_view_ex_02_rotate(self):
    #--------------------------------------------------------------------------------
        view = ViewEx()

        # Set to some angle within 360 degrees
        angle1 = random.randint(1, 359)
        view.set_rotation(angle1)

        self.assertEqual(view.rotation, angle1, "Setting rotation to %f should rotate it to %f degrees, not %f" % (angle1, angle1, view.rotation))
        self.assertEqual(view.rotation_, angle1, "Setting rotation to %f should truly rotate it to %f degrees, not %f" % (angle1, angle1, view.rotation_))

        # Set to a negative degree
        angle2 = random.randint(-359, -1)
        view.set_rotation(angle2)

        self.assertEqual(view.rotation, 360 + angle2, "Setting rotation to %f should rotate it to %f degrees, not %f" % (angle2, 360 + angle2, view.rotation))
        self.assertEqual(view.rotation_, 360 + angle2, "Setting rotation to %f should rotate it to %f degrees, not %f" % (angle2, 360 + angle2, view.rotation_))

        # Set to a large degree
        angle3 = random.randint(360, 719)
        view.set_rotation(angle3)

        self.assertEqual(view.rotation, angle3 - 360, "Setting rotation to %f should rotate it to %f degrees, not %f" % (angle3, angle3 - 360, view.rotation))
        self.assertEqual(view.rotation_, angle3 - 360, "Setting rotation to %f should rotate it to %f degrees, not %f" % (angle3, angle3 - 360, view.rotation_))

        # Reset rotation
        view.set_rotation(0)

        # Rotate by an offset angle
        offset1 = random.randint(1, 299)
        offset2 = random.randint(360, 420)
        view.rotate(offset1)

        self.assertEqual(view.rotation, offset1, "Rotating view by %f degrees should result in a rotation of %f, not %f" % (offset1, offset1, view.rotation))
        self.assertEqual(view.rotation_, offset1, "Rotating view by %f degrees should result in a true rotation of %f, not %f" % (offset1, offset1, view.rotation_))

        # Rotate further by a second large offset
        view.rotate(offset2)

        self.assertEqual(view.rotation, offset1 + offset2 - 360, "Rotating view by %f, then %f degrees should result in a rotation of %f, not %f" % (offset1, offset2, offset1 + offset2 - 360, view.rotation))
        self.assertEqual(view.rotation_, offset1 + offset2, "Rotating view by %f, then %f degrees should result in a true rotation of %f, not %f" % (offset1, offset2, offset1 + offset2, view.rotation_))

    #--------------------------------------------------------------------------------
    def test_view_ex_03_scale(self):
    #--------------------------------------------------------------------------------
        window_size = sf.Vector2(random.randint(1, 100) * 10, random.randint(1, 100) * 10)
        view = ViewEx(sf.Rectangle(sf.Vector2(), window_size))

        # Double screen (zoom out)
        view.scale(2.0)

        self.assertEqual(view.size, window_size * 2.0, "Scaling up view by %f should result in window dimensions of %s, not %s" % (2.0, window_size * 2, view.size))
        self.assertEqual(view.zoom_, 2.0, "Scaling up view from %f by %f should result in a total zoom of %f, not %f" % (1.0, 2.0, 2.0, view.zoom_))

        # Double screen again (zoom out)
        view.scale(2.0)

        self.assertEqual(view.size, window_size * 4.0, "Scaling up view by %f from %f should result in window dimensions of %s, not %s" % (2.0, 2.0, window_size * 4.0, view.size))
        self.assertEqual(view.zoom_, 4.0, "Scaling up view from %f by %f should result in a total zoom of %f, not %f" % (2.0, 2.0, 4.0, view.zoom_))

        # Quarter screen (zoom in)
        view.scale(0.25)

        self.assertEqual(view.size, window_size, "Scaling down view by %f from %f should result in window dimensions of %s, not %s" % (0.25, 4.0, window_size, view.size))
        self.assertEqual(view.zoom_, 1.0, "Scaling down view from %f by %f should result in a total zoom of %f, not %f" % (4.0, 0.25, 1.0, view.zoom_))

        # Scale with negative should do nothing (return None)
        self.assertEqual(view.scale(-1.0), None, "Scaling by a negative factor %f should return None" % (-1.0))
        self.assertEqual(view.size, window_size, "Scaling view by %f should retain old window dimensions of %s, not %s" % (-1.0, window_size, view.size))
        self.assertEqual(view.zoom_, 1.0, "Scaling view by %f should retain old total zoom of %f, not %f" % (-1.0, 1.0, view.zoom_))

    #--------------------------------------------------------------------------------
    def test_view_ex_04_set_size(self):
    #--------------------------------------------------------------------------------
        view = ViewEx()
        window_size = sf.Vector2(random.randint(1, 100) * 10, random.randint(1, 100) * 10)

        # Set size to new window dimensions
        view.set_size(window_size)

        self.assertEqual(view.size, window_size, "Setting view window size to %s should yield a window of %s, not %s" % (window_size, window_size, view.size))

        # Set size while zoomed; should retain factor
        view.scale(2.0)
        window_size = sf.Vector2(random.randint(1, 100) * 10, random.randint(1, 100) * 10)
        view.set_size(window_size)

        self.assertEqual(view.size, window_size * 2.0, "Setting view window size to %s with scale factor %f should retain zoom factor of %f, not %f" % (window_size, 2.0, 2.0, view.zoom_))
        self.assertEqual(view.size, window_size * 2.0, "Setting view window size to %s with scale factor %f should yield a window of %s, not %s" % (window_size, view.zoom_, window_size * 2.0, view.size))

    #--------------------------------------------------------------------------------
    def test_view_ex_05_reset(self):        
    #--------------------------------------------------------------------------------
        view = ViewEx()

        # Apply multiple random transforms
        view.move(sf.Vector2(random.randint(-1000,1000), random.randint(-1000,1000)))
        view.set_size(sf.Vector2(random.randint(1000, 10000), random.randint(1000, 10000)))
        view.scale(random.randint(1, 10))
        view.rotate(random.randint(1, 359))

        # Reset should return to base zoom factor, rotation with specified viewing zone
        view_zone = sf.Rectangle(sf.Vector2(random.randint(1001, 10000), random.randint(1001, 10000)), sf.Vector2(random.randint(1, 1000), random.randint(1, 1000)))
        view.reset(view_zone)

        self.assertEqual(view.center, view_zone.size / 2.0 + view_zone.position, "Reset view to %s should be centered on %s, not %s" % (view_zone, view_zone.size / 2.0 + view_zone.position, view.center))
        self.assertEqual(view.center_, view_zone.size / 2.0 + view_zone.position, "Reset view to %s should be truly centered on %s, not %s" % (view_zone, view_zone.size / 2.0 + view_zone.position, view.center))
        self.assertEqual(view.size, view_zone.size, "Reset view to %s should have a size of %s, not %s" % (view_zone, view_zone.size, view.size))
        self.assertEqual(view.rotation, 0.0, "Reset view to %s should be rotated at %f degrees, not %f degrees" % (view_zone, 0.0, view.rotation))
        self.assertEqual(view.rotation_, 0.0, "Reset view to %s view should be truly rotated at %f degrees, not %f degrees" % (view_zone, 0.0, view.rotation_))
        self.assertEqual(view.zoom_, 1.0, "Reset view to %s view should have an initial scale/zoom factor of %f, not %f" % (view_zone, 1.0, view.zoom_))

#------------------------------------------------------------------------------------
