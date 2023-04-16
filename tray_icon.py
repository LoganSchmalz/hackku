import wx
import wx.adv
import win32api

tray_name = 'Voice to Text'
icon = 'icon.png'

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item

class TaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, screen_width, screen_height, change_pos_callback, change_size_callback):
        super(TaskBarIcon, self).__init__()
        self.set_icon(icon)
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.placeholder)
        self.change_pos_callback = change_pos_callback
        self.change_size_callback = change_size_callback
        self.screen_height = screen_height
        self.screen_width = screen_width

    def CreatePopupMenu(self):
        menu = wx.Menu()
       
        
        size = wx.Menu()
        create_menu_item(size,"Small",self.small_menu)
        size.AppendSeparator()
        create_menu_item(size,"Medium",self.med_menu)
        size.AppendSeparator()
        create_menu_item(size,"Large",self.large_menu)

        position = wx.Menu()
        create_menu_item(position,"Top Left",self.top_left)
        position.AppendSeparator()
        create_menu_item(position,"Top Right",self.top_right)
        position.AppendSeparator()
        create_menu_item(position,"Middle Left",self.mid_left)
        position.AppendSeparator()
        create_menu_item(position,"Middle Right",self.mid_right)
        position.AppendSeparator()
        create_menu_item(position,"Bottom Left",self.bot_left)
        position.AppendSeparator()
        create_menu_item(position,"Bottom Right",self.bot_right)

        wx.Menu.AppendSubMenu(menu,size,'Overlay Size')
        menu.AppendSeparator()
        wx.Menu.AppendSubMenu(menu,position,'Overlay Position')
        menu.AppendSeparator()
        create_menu_item(menu,"Exit",self.exit)
        return menu
    
    def set_icon(self, path):
        icon = wx.Icon(wx.Bitmap(path))
        self.SetIcon(icon, tray_name)

    def small_menu(self, event):
        size = [(int(self.screen_width/10), int(self.screen_height/10))]
        self.change_size_callback(size, event)

    def med_menu(self,event):
        size = [(int(self.screen_width/20), int(self.screen_height/20))]
        self.change_size_callback(size, event)
        
    def large_menu(self,event):
        size = [(int(self.screen_width/2), int(self.screen_height/2))]
        self.change_size_callback(size, event)

    def exit(self,event):
        #wx.CallAfter(self.Destroy)
        wx.Exit()
    
    def placeholder(self,event):
        return


    
    def top_left(self,event):
        self.change_pos_callback([10,10], event)
    
    def top_right(self,event):
        return
    
    def bot_left(self,event):
        return
    
    def bot_right(self,event):
        return
    
    def mid_right(self,event):
        return
    def mid_left(self,event):
        return
    