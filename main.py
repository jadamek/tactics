import sfml as sf, random
from sprite.map.sprite_tile import SpriteTile
from map.map import Map
from map.tile import Tile
       
dirt_texture = sf.Texture.from_file('resources/graphics/Tile.png')
grass_texture = sf.Texture.from_file('resources/graphics/GrassTile.png')

map = Map(10, 10)

# Dirt layer
for x in range(map.width):
    for y in range(map.length):
        height = random.randint(3, 5) / 2.0

        tile_sprite = SpriteTile(dirt_texture, map.scale_.x, map.scale_.y, map.scale_.z * height)
        tile = Tile(tile_sprite, height)
                
        map.place(tile, x, y)

# Grass layer        
for x in range(map.width):
    for y in range(map.length):
        height = random.randint(1, 2) / 2.0

        tile_sprite = SpriteTile(grass_texture, map.scale_.x, map.scale_.y, map.scale_.z * height)
        tile = Tile(tile_sprite, height)
                
        map.place(tile, x, y)        
        
target = sf.Texture.from_file('resources/graphics/Target.png')
cursor = sf.Sprite(target)
cursor.move(sf.Vector2(-8,-8))

window = sf.RenderWindow(sf.VideoMode(640, 480), 'Tactics!')
window.framerate_limit = 60

view = sf.View(sf.Rectangle((-320, -240), (640, 480)))
window.view = view

while window.is_open:
    for event in window.events:
        if type(event) is sf.CloseEvent:
            window.close()
                    
    window.clear()
    window.draw(map)
    window.draw(cursor)
    window.display()
