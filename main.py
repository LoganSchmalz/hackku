from overlay import Overlay

def get_new_text():
    print("getting new text")
    return (500, "test")

def main():
    overlay = Overlay(get_new_text)
    overlay.run()

if __name__ == "__main__":
    main()