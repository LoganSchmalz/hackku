import oGUI, win32api

oGUI.init()

rect = oGUI.Rect(oGUI.darkgray, 100, 100, 300, 500)
button = oGUI.Button(oGUI.gray, oGUI.orange, 120, 200, 30, 30)
button2 = oGUI.Button(oGUI.darkgray, oGUI.lightgray, 368, 103, 30, 35)

myText = oGUI.Text(oGUI.orange, 195, 110, 30, "oGUI Demo")
myText2 = oGUI.Text(oGUI.orange, 155, 152, 25, "Checkbox")
myText3 = oGUI.Text(oGUI.orange, 155, 208, 25, "Button")
myText4 = oGUI.Text(oGUI.black, 375, 105, 30, "X")

width = win32api.GetSystemMetrics(0)
height = win32api.GetSystemMetrics(1)

string = "Checkbox"

while True:
    string += "a"
    myText2 = oGUI.Text(oGUI.orange, 155, 152, 25, string)

    button.is_hovered(oGUI.lightgray)
    button2.is_hovered(oGUI.gray)

    myText.font('Roboto') #Setting Text Object's font
    myText2.font('Roboto')
    myText3.font('Roboto')

    myText.dropShadow(oGUI.black, 2) #Setting Text Object's DropShadow
    myText2.dropShadow(oGUI.black, 2)
    myText3.dropShadow(oGUI.black, 2)

    oGUI.startLoop() #Start of Draw Loop

    rect.draw() #Drawing Rectangle, Box, Checkbox, and Button
    button.draw()
    button2.draw()

    myText.draw() #Drawing Text
    myText2.draw()
    myText3.draw()
    myText4.draw()

    oGUI.endLoop() #End of Draw Loop
    
    if button.is_enabled(): #Do something if the button is enabled/pressed
        print('Button was pressed')

    if button2.is_enabled(): #Exit Button
        exit(0)