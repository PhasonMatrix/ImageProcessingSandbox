from MainWindow import MainWindow
import wx
import math



if __name__=="__main__":
    app = wx.PySimpleApp()
    frame = MainWindow(parent = None, id = -1)
    frame.Show()
    app.MainLoop()








