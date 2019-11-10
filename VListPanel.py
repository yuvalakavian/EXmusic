import  wx

class UserListBox(wx.VListBox):
    """Simple List Box control to show a list of users"""
    def __init__(self, parent, items,info,types, pos=(0, 0), size=(400, 700)):
        """@param users: list of user names"""
        super(UserListBox, self).__init__(parent,  -1, pos=pos, size=size, style=wx.BORDER_SUNKEN)

        self.PhotoMaxSize = 150

        self.info=info

        imglist=[]
        self.bmplist = []
        self.bh=[]
        img_name_str=""
        for i in xrange(len(items)):
            if types=="ebay":
                img_name_str = "Pics\Res\image"+str(i)+".jpg"
                
            else:
                img_name_str=items[i][2]
            imglist.append(wx.Image(img_name_str, wx.BITMAP_TYPE_ANY))
            
            W = imglist[i].GetWidth()
            H = imglist[i].GetHeight()
            if W > H:
                NewW = self.PhotoMaxSize
                NewH = self.PhotoMaxSize * H / W
            else:
                NewH = self.PhotoMaxSize
                NewW = self.PhotoMaxSize * W / H
            imglist[i] = imglist[i].Scale(NewW,NewH)
            
            self.bmplist.append(wx.BitmapFromImage(imglist[i]))
            
            self.bh.append(self.bmplist[i].GetHeight())

        self.items = items
        # Setup
        self.SetItemCount(len(self.items))

    def OnMeasureItem(self, index):
        """Called to get an items height"""
        # All our items are the same so index is ignored
        return self.bh[index] + 4

    def OnDrawSeparator(self, dc, rect, index):
        """Called to draw the item separator"""
        oldpen = dc.GetPen()
        dc.SetPen(wx.Pen(wx.BLACK))
        dc.DrawLine(rect.x, rect.y,
        rect.x + rect.width,
        rect.y)
        rect.Deflate(0, 2)
        dc.SetPen(oldpen)

    def OnDrawItem(self, dc, rect, index):
        """Called to draw the item"""
        # Draw the bitmap
        dc.DrawBitmap(self.bmplist[index], rect.x + 2,
        ((rect.height - self.bh[index]) / 2) + rect.y)
        # Draw the label to the right of the bitmap
        textx = rect.x + 2 + self.bh[index] + 2
        lblrect = wx.Rect(textx, rect.y,
        rect.width - textx,
        rect.height)
        dc.DrawLabel(self.info[index], lblrect,
        wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)

        #dc.DrawButton

    def GetSelected(self):
        return self.GetSelection()


#---------------------------------------------------------

class VBListPanel(wx.Panel):
    def __init__(self, parent):

        wx.Panel.__init__(self, parent, -1)
        spacer = 50

        users = ["User1", "User2", "User3", "User4", "User5", "User6", "User7", "User8","User9","User10","User11"]
        vlb = UserListBox(self,users)
        vlb.SetItemCount(len(users))
        vlb.SetSelection(0)
        vlb.SetFocus()

        vlbSizer = wx.BoxSizer(wx.VERTICAL)
        vlbSizer.Add((spacer, spacer))
        vlbSizer.Add(wx.StaticText(self, -1, "wx.VListBox"), 0, 5, wx.ALL)
        vlbSizer.Add(vlb)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add((spacer, spacer))
        sizer.Add(vlbSizer)
        sizer.Add((spacer, spacer))


        self.SetSizer(sizer)
