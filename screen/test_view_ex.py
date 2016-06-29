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
    def test_view_ex_move(self):
    #--------------------------------------------------------------------------------
        pass
        
#------------------------------------------------------------------------------------
