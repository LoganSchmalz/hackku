import wx
from typing import Tuple
from tray_icon import TaskBarIcon

class Overlay2(wx.Frame):
    def __init__(self, screen_width, screen_height, key_phrases, get_new_text_callback):
        self.get_new_text_callback = get_new_text_callback
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.key_phrases = key_phrases
        dimensions: Tuple[int, int] = (int(screen_width/4), int(screen_height/5))
        coordinates: Tuple[int, int] = (
        int(self.screen_width/20),
        int(self.screen_height / 2 - self.dimensions[1] / 2)
         )
        style = ( wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                  wx.NO_BORDER | wx.FRAME_SHAPED )
        
        wx.Frame.__init__(self, None, title='Fancy', style = style)
        self.SetTransparent(128)
        self.Show(True)
        self.SetPosition(wx.Point(coordinates[0], coordinates[1]))
        self.SetSize(wx.Size(dimensions[0], dimensions[1]))
        self.SetBackgroundColour((0,0,0))
        
        self.st = wx.TextCtrl(self, value="", style = (wx.TE_READONLY | wx.TE_MULTILINE), size=(dimensions[0],dimensions[1]))
        self.st.Enable(False)
        self.st.SetScrollPos(wx.VERTICAL, self.st.GetScrollRange(wx.VERTICAL))
        self.st.SetInsertionPoint(-1)
        font = self.st.GetFont()
        font.PointSize = 12
        self.st.SetFont(font)
        self.st.SetForegroundColour((255,255,255))
        self.st.SetBackgroundColour((0,0,0))
        #self.st.Wrap(self.Size[0])

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_label, self.timer)
        self.timer.Start(2000)

        self.tb = TaskBarIcon(self.screen_width, self.screen_height, self.change_position, self.change_size)

    def update_label(self, event) -> None:
        wait_time, update_text = self.get_new_text_callback()
        self.check_transcript(update_text, self.key_phrases, None)
        self.st.SetValue("\n".join(update_text))
        self.st.SetScrollPos(wx.VERTICAL, self.st.GetScrollRange(wx.VERTICAL))
        self.st.SetInsertionPoint(-1)
    
    def check_transcript(self, update_text, key_phrases, event):
        words_list = [] #list of current words in the updated text
        phrases_list = [] #list of phrases that actually appear in the updated text

        for i in update_text:
            words_list.extend(i.split())

        for i in words_list:
            for j in key_phrases.split():
                if (i.lower() == j.lower()):
                    phrases_list.append(i)

        print(phrases_list)

        return phrases_list


    def change_position(self, pos, event):
        self.SetPosition(wx.Point(pos[0], pos[1]))

    def change_size(self, size, event):
        self.SetSize(wx.Size(size[0], size[1]))