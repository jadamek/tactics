import sfml as sf, random
from sprite.map.sprite_tile import SpriteTile
from map.map import Map
from map.tile import Tile
from objects.mobile_object import MobileObject
from objects.actor import Actor

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
                
        map.place(tile, x, y)

        # Grass layer        
        height = random.randint(1, 2) / 2.0

        tile_sprite = SpriteTile(grass_texture, map.scale_.x, map.scale_.y, map.scale_.z * height)
        tile = Tile(tile_sprite, height)

        map.place(tile, x, y)

# Add object
soul_texture = sf.Texture.from_file('resources/graphics/Soul.png')
soul_sprite = sf.Sprite(soul_texture)
soul_sprite.move(sf.Vector2(-12, -40))

soul = Actor(soul_sprite, map)
map.add_object(soul)

#Place (0, 0, 0) cursor        
target = sf.Texture.from_file('resources/graphics/Target.png')
cursor = sf.Sprite(target)
cursor.move(sf.Vector2(-8,-8))

window = sf.RenderWindow(sf.VideoMode(640, 480), 'Tactics!')
window.framerate_limit = 60

view = sf.View(sf.Rectangle((-320, -240), (640, 480)))
window.view = view
clock = sf.Clock()
elapsed = 0.0

soul.moveAlong([sf.Vector2(9, 0), sf.Vector2(9, 9), sf.Vector2(0, 9), sf.Vector2(0, 0)])
while window.is_open:
    for event in window.events:
        if type(event) is sf.CloseEvent:
            window.close()            
                    
    elapsed = clock.restart().seconds
    soul.update(elapsed)
    window.clear()
    window.draw(map)
    window.draw(cursor)
    window.display()
