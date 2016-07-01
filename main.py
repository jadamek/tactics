import sfml as sf, random
from sprite.map.sprite_tile import SpriteTile
from map.map import Map
from map.tile import Tile
from objects.mobile_object import MobileObject
from objects.actor import Actor
from rectangle import Rectangle
from screen.view_ex import ViewEx

dirt_texture = sf.Texture.from_file('resources/graphics/Tile.png')
grass_texture = sf.Texture.from_file('resources/graphics/GrassTile.png')

# Generate map
map = Map(10, 10)

for x in range(map.width):
    for y in range(map.length):
        # Dirt layer
        height = random.randint(3, 5) / 2.0

        tile_sprite = SpriteTile(dirt_texture, map.scale_.x, map.scale_.y, map.scale_.z * height)
        tile = Tile(tile_sprite, height)
        tile.name_ = "g-%d-%d" % (x, y)
                
        map.place(tile, x, y)

        # Grass layer        
        height = random.randint(1, 2) / 2.0

        tile_sprite = SpriteTile(grass_texture, map.scale_.x, map.scale_.y, map.scale_.z * height)
        tile = Tile(tile_sprite, height)
        tile.name_ = "f1-%d-%d" % (x, y)

        map.place(tile, x, y)

# Add object
soul_texture = sf.Texture.from_file('resources/graphics/Soul.png')
soul_sprite = sf.Sprite(soul_texture)
soul_sprite.move(sf.Vector2(-12, -40))

soul = Actor(soul_sprite, map)
soul.name_ = "soul"
map.add_object(soul)
#soul.moveAlong([sf.Vector2(map.width - 1, 0), sf.Vector2(map.width - 1, map.length - 1), sf.Vector2(0, map.length - 1), sf.Vector2(0, 0)])

#print map.at(0, 0).name_, "<=", map.at(1, 0, 0).name_, "?", map.at(0, 0) <= map.at(1, 0, 0)
#print map.at(1, 0, 0).name_, ">", map.at(0, 0).name_, "?", map.at(1, 0, 0) > map.at(0, 0)

#Place (0, 0, 0) cursor        
target = sf.Texture.from_file('resources/graphics/Target.png')
cursor = sf.Sprite(target)
cursor.move(sf.Vector2(-8,-8))

window = sf.RenderWindow(sf.VideoMode(640, 480), 'Tactics!')
window.framerate_limit = 60

path = [sf.Vector2(80, 60), sf.Vector2(-60, 80), sf.Vector2(-80, -60), sf.Vector2(60, -80)]
p = 0

view = ViewEx(sf.Rectangle((-320, -240), (640, 480)))
window.view = view
clock = sf.Clock()
elapsed = 0.0

while window.is_open:
    for event in window.events:
        if type(event) is sf.CloseEvent:
            window.close()

    if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):
        if sf.Keyboard.is_key_pressed(sf.Keyboard.L_SHIFT):
            if not view.scrolling():
                view.scroll(sf.Vector2(-32, 0), 0.5)
        elif not soul.moving():
            soul.moveTo(soul.position + sf.Vector3(-1.0, 0, 0))

    elif sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):
        if sf.Keyboard.is_key_pressed(sf.Keyboard.L_SHIFT):
            if not view.scrolling():
                view.scroll(sf.Vector2(32, 0), 0.5)
        elif not soul.moving():
            soul.moveTo(soul.position + sf.Vector3(1.0, 0, 0))

    elif sf.Keyboard.is_key_pressed(sf.Keyboard.UP):
        if sf.Keyboard.is_key_pressed(sf.Keyboard.L_SHIFT):
            if not view.scrolling():
                view.scroll(sf.Vector2(0, -24), 0.5)
        elif not soul.moving():
            soul.moveTo(soul.position + sf.Vector3(0.0, -1.0, 0))

    elif sf.Keyboard.is_key_pressed(sf.Keyboard.DOWN):
        if sf.Keyboard.is_key_pressed(sf.Keyboard.L_SHIFT):
            if not view.scrolling():
                view.scroll(sf.Vector2(0, 24), 0.5)
        elif not soul.moving():
            soul.moveTo(soul.position + sf.Vector3(0, 1.0, 0))

    elif sf.Keyboard.is_key_pressed(sf.Keyboard.ESCAPE):
        window.close()

        view.scroll(path[p], 3)
        p = (p + 1) % 4

    elapsed = clock.restart().seconds
    soul.update(elapsed)
    view.update(elapsed)
    window.clear()
    window.draw(map)
    window.draw(cursor)
    window.display()

