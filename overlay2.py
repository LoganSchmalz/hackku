import wx
from typing import Tuple
from tray_icon import TaskBarIcon

class Overlay2(wx.Frame):
    def __init__(self, screen_width, screen_height, get_new_text_callback):
        self.get_new_text_callback = get_new_text_callback
        dimensions: Tuple[int, int] = (int(screen_width/2), int(screen_height/2))
        coordinates: Tuple[int, int] = (
        screen_width - (dimensions[0] + int(screen_width/2.1)),
        screen_height - (dimensions[1] + int(screen_height/7))
         )
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
        self.st.Wrap(self.Size[0])

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_label, self.timer)
        self.timer.Start(500)

        self.tb = TaskBarIcon(self.screen_width, self.screen_height, self.change_position, self.change_size)

    def update_label(self, event) -> None:
        wait_time, update_text = self.get_new_text_callback()
        self.st.SetLabelText("\n".join(update_text))
        self.st.Wrap(self.Size[0])

    def change_position(self, pos, event):
        self.SetPosition(wx.Point(pos[0], pos[1]))

    def change_size(self, size, event):
        self.SetSize(wx.Size(size[0], size[1]))