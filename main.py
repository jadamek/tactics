import sfml as sf

window = sf.Window(sf.VideoMode(640, 480), 'Tactics!')
window.framerate_limit = 60

while window.is_open:
    for event in window.events:
            if type(event) is sf.CloseEvent:
                    window.close()
                    
            window.active = True
            window.display()
