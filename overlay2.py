import wx
from typing import Tuple

class Overlay2(wx.Frame):
    def __init__(self, dimensions: Tuple[int,int], coordinates: Tuple[int, int], get_new_text_callback):
        self.get_new_text_callback = get_new_text_callback

        style = ( wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                  wx.NO_BORDER | wx.FRAME_SHAPED  )
        
        wx.Frame.__init__(self, None, title='Fancy', style = style)
        self.SetTransparent(128)
        self.Show(True)
        self.SetPosition(wx.Point(coordinates[0], coordinates[1]))
        self.SetSize(wx.Size(dimensions[0], dimensions[1]))
        self.SetBackgroundColour((0,0,0))
        
        self.st = wx.StaticText(self, label="Test")
        font = self.st.GetFont()
        font.PointSize = 12
        self.st.SetFont(font)
        self.st.SetForegroundColour((255,255,255))

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_label, self.timer)
        self.timer.Start(500)

    def update_label(self, event) -> None:
        wait_time, update_text = self.get_new_text_callback()
        self.st.SetLabelText("\n".join(update_text))

    def change_position(self, pos, event):
        self.SetPosition(wx.Point(pos[0], pos[1]))