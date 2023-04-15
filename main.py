from overlay import Overlay
import win32api

def get_new_text():
    print("getting new text")
    overlay.insert_msg("getting new text")

    overlay_text = "title"

    for msg in reversed(overlay.msg_q):
        overlay_text += '\n' + msg

    return (500, overlay_text)

overlay = Overlay(get_new_text)

def main():

    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)
    print(screen_height)
    print(screen_width)
    overlay.set_height(int(screen_height / 10))
    overlay.set_width(int(screen_width/ 5))
    overlay.font(4)
    #overlay = Overlay(get_new_text)
    overlay.set_x(screen_width - (int(overlay.width) + int(screen_width/100))) #10 pixels of padding, should also be relative to screen size in the future
    overlay.set_y(screen_height - (int(overlay.height) + int(screen_height/7))) #400 pixels of padding, should also be relative to screen size in the future
    overlay.run()

if __name__ == "__main__":
    main()