from overlay import Overlay
from sys import platform
if 'windows' in platform:
    import win32api

def get_new_text():
    return (500, "getting new text")

def main():

    if 'windows' in platform:
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)
    else:
        screen_width = 1000
        screen_height = 700
    print(screen_height)
    print(screen_width)

    overlay = Overlay((int(screen_width/2), int(screen_height/2)), get_new_text)
    overlay.font(4)
    #overlay = Overlay(get_new_text)
    overlay.set_x(screen_width - (int(overlay.width) + int(screen_width/2.1))) #10 pixels of padding, should also be relative to screen size in the future
    overlay.set_y(screen_height - (int(overlay.height) + int(screen_height/7))) #400 pixels of padding, should also be relative to screen size in the future
    overlay.run()

if __name__ == "__main__":
    main()