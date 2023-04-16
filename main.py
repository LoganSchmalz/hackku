from time import sleep
#from overlay import Overlay
from overlay2 import Overlay2
from audio_processor import AudioProcessor
from audio_bridge import AudioBridge
from sys import platform
import wx
import re
if 'windows' in platform:
    import win32api

def main():
    key_phrases = " ".join([
            "spawn", "CT", "T", "A", "B", "mid", "middle", "default", "main", "cubby", "link", "connector", "heaven", "hell", "lobby", "bottom", "top", "site", "cite"
            "Raina", "Astra", "Breach", "Brimstone", "Chamber", "Cypher", "Jett", "KO", "Killjoy", "Neon", "Omen", "Phoenix", "Raise", "Sage", "Sky", "Soba", "Viper", "Yoru", 
            "plant", "defuse", "defusing", "sticking", "stick", "planting", "bomb", "spike", 
            "lit", "one shot", "1", "low",
            "boat", "boathouse", "market", "pizza", "garden", "tree", "window", "rafters", "tree", "cat", "dice", "generator", "Jen", "door", "wine", "courtyard", "cat", "catwalk", "Subrosa", 
            ])
    #highlight key words
    def highlight(get_new_text, key_phrases):
        replacement = lambda match: "<mark>" + match.group() + "</mark>"
    text = re.sub("|".join(map(re.escape, key_phrases)), replacement, text, flags=re.I)

    highlight(get_new_text, key_phrases)
    
    speakers = AudioBridge()
    ap = AudioProcessor(source=speakers, phrases=key_phrases)

    def get_new_text():
        ap.update_transcript()
        return (500, ap.transcription)
        #return (500,"a")

    if 'windows' in platform:
        screen_width = win32api.GetSystemMetrics(0)
        screen_height = win32api.GetSystemMetrics(1)
    else:
        screen_width = 1000
        screen_height = 700

    # app_dimensions: Tuple[int, int] = (int(screen_width/2), int(screen_height/2))
    # app_coordinates: Tuple[int, int] = (
    #     screen_width - (app_dimensions[0] + int(screen_width/2.1)),
    #     screen_height - (app_dimensions[1] + int(screen_height/7))
    # )
    
    app = wx.App()
    overlay = Overlay2(screen_width, screen_height, get_new_text)
    app.MainLoop()

    # overlay = Overlay((int(screen_width/2), int(screen_height/2)), get_new_text)
    # overlay.font(4)
    # #overlay = Overlay(get_new_text)
    # overlay.set_x(screen_width - (int(overlay.width) + int(screen_width/2.1))) #10 pixels of padding, should also be relative to screen size in the future
    # overlay.set_y(screen_height - (int(overlay.height) + int(screen_height/7))) #400 pixels of padding, should also be relative to screen size in the future
    # overlay.run()

if __name__ == "__main__":
    main()

