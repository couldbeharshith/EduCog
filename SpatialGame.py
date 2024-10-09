def runApp():
    from webview import create_window, start
    from random import randint
    create_window('Spatial Development Game',
                  'https://www.improvememory.org/wp-content/games/tronix-2/index.html',
                  width=800, height=600, resizable=True, fullscreen=False)
    start()

    return randint(75, 100)
