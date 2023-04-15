import oGUI, win32api
import numpy as np

oGUI.init()

width = win32api.GetSystemMetrics(0)
height = win32api.GetSystemMetrics(1)

rect = oGUI.Rect(oGUI.darkgray, width-400, height-600, 300, 500)
button2 = oGUI.Button(oGUI.white, oGUI.lightgray, 368, 103, 30, 35)

myText = oGUI.Text(oGUI.orange, width-155, height-152, 30, "oGUI Demo")

string = "Checkbox"

while True:
    if t > 500:
        string = " "
        t = 0
    elif t_wait > 100:
        string = " "
        t_wait = 0
    
    add = np.random.randint(10)
    if add < 7:
        t_wait += 1
    
    string += "a"
    #myText = oGUI.Text(oGUI.orange, width-155, height-152, 25, string)
    myText.updateText(string)

    button2.is_hovered(oGUI.gray)

    myText.font('Roboto') #Setting Text Object's font

    #myText.dropShadow(oGUI.black, 2) #Setting Text Object's DropShadow

    oGUI.startLoop() #Start of Draw Loop

    rect.draw() #Drawing Rectangle, Box, Checkbox, and Button
    button2.draw()

    myText.draw() #Drawing Text

    oGUI.endLoop() #End of Draw Loop

    if button2.is_enabled(): #Exit Button
        exit(0)