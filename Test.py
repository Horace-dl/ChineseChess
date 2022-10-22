import wx
app = wx.App(False) #创建1个APP，禁用stdout/stderr重定向
frame = wx.Frame(None, wx.ID_ANY, "Hello, World!")  #这是一个顶层的window
frame.Show(True)    #显示这个frame
app.MainLoop()