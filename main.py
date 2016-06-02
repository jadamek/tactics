import sfml as sf
from sprite.map.sprite_tile import SpriteTile

window = sf.RenderWindow(sf.VideoMode(640, 480), 'Tactics!')
window.framerate_limit = 60

tile_texture = sf.Texture.from_file('resources/graphics/GrassTile.png')
tile = SpriteTile(tile_texture)
tile.move(sf.Vector2(100, 100))
#tile.rotate(30)
tile.reset_height(8)

target = sf.Texture.from_file('resources/graphics/Target.png')
cursor = sf.Sprite(target)
cursor.move(sf.Vector2(92, 92))

print str(tile.position)

while window.is_open:
    for event in window.events:
        if type(event) is sf.CloseEvent:
            window.close()
                    
    window.clear()
    window.draw(tile)
    window.draw(cursor)
    window.display()
