# -*- coding: utf-8 -*-


import wx
import os.path
import gui.icons

class GridWidget:
    """Class implementing a button with image and caption. In particular,
    it is used for generating on the flight buttons for each directory and
    file inside a path on the reMarkable cloud.
    """

    def __init__(self, app, label):
        self.icon = None
        self.action = lambda self, event: event.Skip()
        self.label = label
        self.app = app

    def create_objects(self):
        self.bWidgetSizer = wx.BoxSizer( wx.VERTICAL )

        self.mButton = wx.BitmapButton( self.app, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.BORDER_NONE|0 )
        if self.icon:
            self.mButton.SetBitmap( wx.Bitmap( self.icon, wx.BITMAP_TYPE_ANY ) )
        self.bWidgetSizer.Add( self.mButton, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )

        self.mLabel = wx.StaticText( self.app, wx.ID_ANY, self.label, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.mLabel.Wrap( -1 )
        # self.mLabel.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
        # self.mLabel.SetBackgroundColour( wx.Colour( 255, 255, 225 ) )
        self.bWidgetSizer.Add( self.mLabel, 0, wx.ALL|wx.EXPAND, 5 )

        self.app.bFilesGridSizer.Add( self.bWidgetSizer, 1, wx.EXPAND, 5 )
        self.app.Layout()

        self.mButton.Bind( wx.EVT_LEFT_DCLICK, lambda event: self.action(event, self.label))

    def __del__(self):
        try:
            self.mLabel.Destroy()
            pass
        except RuntimeError:
            pass

        try:
            # destroying this causes segfault
            # self.mButton.Destroy()
            pass
        except RuntimeError:
            pass

        try:
            self.bWidgetSizer.Destroy()
            pass
        except RuntimeError:
            pass


class DirectoryWidget(GridWidget):

    def __init__(self, app, label):
        GridWidget.__init__(self, app, label)
        self.icon = gui.icons.folder
        self.action = app.enter_directory
        self.create_objects()


class FileWidget(GridWidget):

    def __init__(self, app, label):
        GridWidget.__init__(self, app, label)
        self.icon = gui.icons.document
        self.action = app.export_file
        self.create_objects()
