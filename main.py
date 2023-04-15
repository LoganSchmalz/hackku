from overlay import Overlay
import win32api

def get_new_text():
    print("getting new text")
    return (500, "test")

def main():
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)

    overlay = Overlay(get_new_text)
    overlay.set_x(screen_width - (int(overlay.width) + 20)) #10 pixels of padding, should also be relative to screen size in the future
    overlay.set_y(screen_height - (int(overlay.height) + 400)) #400 pixels of padding, should also be relative to screen size in the future
    overlay.run()

if __name__ == "__main__":
    main()