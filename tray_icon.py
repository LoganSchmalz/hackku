import wx
import wx.adv

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
        self.dimensions = (int(self.screen_width/4), int(self.screen_height/5))
        self.location_func = self.mid_left

        self.x_pad = screen_width/30
        self.y_pad = screen_height/20

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
        self.dimensions = (int(self.screen_width/4), int(self.screen_height/8))
        self.change_size_callback(self.dimensions, event)
        self.location_func(event)

    def med_menu(self,event):
        self.dimensions = (int(self.screen_width/4), int(self.screen_height/5))
        self.change_size_callback(self.dimensions, event)
        self.location_func(event)
        
    def large_menu(self,event):
        self.dimensions = (int(self.screen_width/4), int(self.screen_height/3))
        self.change_size_callback(self.dimensions, event)
        self.location_func(event)

    def exit(self,event):
        #wx.CallAfter(self.Destroy)
        wx.Exit()
    
    def placeholder(self,event):
        return
    
    def top_left(self,event):
        pos = (
        int(self.x_pad),
        int(self.y_pad)
         )
        self.change_pos_callback(pos, event)
        self.location_func = self.top_left
    
    def top_right(self,event):
        pos = (
        int(self.screen_width - (self.dimensions[0] + self.x_pad)),
        int(self.y_pad)
        )
        self.change_pos_callback(pos,event)
        self.location_func = self.top_right
    
    def mid_left(self,event):
        pos = (
        int(self.x_pad),
        int(self.screen_height/2) - int(self.dimensions[1]/2)
        )
        self.change_pos_callback(pos, event)
        self.location_func = self.mid_left
    
    def mid_right(self,event):
        pos = (
        int(self.screen_width - (self.dimensions[0] + self.x_pad) ),
        int(self.screen_height/2) - int(self.dimensions[1]/2)
        )
        self.change_pos_callback(pos,event)
        self.location_func = self.mid_right

    def bot_left(self,event):
        pos = (
        int(self.x_pad),
        int(self.screen_height - (self.dimensions[1] + self.y_pad))
         )
        self.change_pos_callback(pos, event)
        self.location_func = self.bot_left

    
    def bot_right(self,event):
        pos = (
        int(self.screen_width - (self.dimensions[0] + self.x_pad)),
        int(self.screen_height - (self.dimensions[1] + self.y_pad))
        )
        self.change_pos_callback(pos,event)
        self.location_func = bot_right
    
