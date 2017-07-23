from sfml import sf
from screen.view_ex import ViewEx
import settings

window = sf.RenderWindow(sf.VideoMode(640, 480), 'Tactics!')
window.framerate_limit = 60

view = ViewEx(sf.Rect((-320, -240), (640, 480)))
window.view = view

clock = sf.Clock()
elapsed = 0.0

closing = False

while window.is_open:
    for event in window.events:
        if type(event) is sf.Event.CLOSED:
            window.close()

    if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):
        if sf.Keyboard.is_key_pressed(sf.Keyboard.L_SHIFT):
            if not view.scrolling():
                view.scroll(sf.Vector2(-32, 0), 0.5)

    elif sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):
        if sf.Keyboard.is_key_pressed(sf.Keyboard.L_SHIFT):
            if not view.scrolling():
                view.scroll(sf.Vector2(32, 0), 0.5)

    elif sf.Keyboard.is_key_pressed(sf.Keyboard.UP):
        if sf.Keyboard.is_key_pressed(sf.Keyboard.L_SHIFT):
            if not view.scrolling():
                view.scroll(sf.Vector2(0, -24), 0.5)

    elif sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN):
        if sf.Keyboard.is_key_pressed(sf.Keyboard.L_SHIFT):
            if not view.scrolling():
                view.scroll(sf.Vector2(0, 24), 0.5)

    elif sf.Keyboard.is_key_pressed(sf.Keyboard.ESCAPE) and not view.tinting():
        view.fade_out(3)
        closing = True

    elif closing and not view.tinting():
        window.close()

    elapsed = clock.restart().seconds
    view.update(elapsed)
    window.clear()
    view.draw_overlays(window)
    window.display()