# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
###########################################################################

import wx
import wx.xrc
import os.path
import gui.icons

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Remar", pos = wx.DefaultPosition, size = wx.Size( 697,463 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		# self.SetBackgroundColour( wx.Colour( 255, 255, 225 ) )
		prefix = os.path.dirname(os.path.realpath(__file__)) + "/"

		bOuterSizer = wx.BoxSizer( wx.VERTICAL )

		bTopBarSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.m_homeButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.Size( -1,-1 ), wx.BU_AUTODRAW|wx.BORDER_NONE|0 )

		self.m_homeButton.SetBitmap( wx.Bitmap( gui.icons.home, wx.BITMAP_TYPE_ANY ) )
		bTopBarSizer.Add( self.m_homeButton, 0, wx.ALL, 5 )

		self.m_folderUpButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.BORDER_NONE|0 )

		self.m_folderUpButton.SetBitmap( wx.Bitmap( gui.icons.up, wx.BITMAP_TYPE_ANY ) )
		bTopBarSizer.Add( self.m_folderUpButton, 0, wx.ALL, 5 )

		self.m_refreshButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.BORDER_NONE|0 )

		self.m_refreshButton.SetBitmap( wx.Bitmap( gui.icons.refresh, wx.BITMAP_TYPE_ANY ) )
		bTopBarSizer.Add( self.m_refreshButton, 0, wx.ALL, 5 )

		self.m_settingsButton = wx.BitmapButton( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, wx.BU_AUTODRAW|wx.BORDER_NONE|0 )

		self.m_settingsButton.SetBitmap( wx.Bitmap( gui.icons.settings, wx.BITMAP_TYPE_ANY ) )
		bTopBarSizer.Add( self.m_settingsButton, 0, wx.ALL, 5 )

		self.m_locationBar = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_READONLY )
		bTopBarSizer.Add( self.m_locationBar, 1, wx.ALL|wx.EXPAND, 5 )

		bOuterSizer.Add( bTopBarSizer, 0, wx.EXPAND, 5 )

		bContentSizer = wx.BoxSizer( wx.HORIZONTAL )

		bSidebarSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_importButton = wx.Button( self, wx.ID_ANY, u"Import", wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE|0 )
		# self.m_importButton.SetForegroundColour( wx.Colour( 0, 0, 0 ) )
		bSidebarSizer.Add( self.m_importButton, 0, wx.ALL, 5 )


		bContentSizer.Add( bSidebarSizer, 0, wx.EXPAND, 5 )

		bFilesGridSizer = wx.GridSizer( 0, 6, 0, 0 )

		bContentSizer.Add( bFilesGridSizer, 1, 0, 5 )

		bOuterSizer.Add( bContentSizer, 1, wx.EXPAND, 5 )

		self.SetSizer( bOuterSizer )
		self.Layout()
		self.m_statusBar = self.CreateStatusBar( 2, wx.STB_SIZEGRIP, wx.ID_ANY )
		# self.m_statusBar.SetBackgroundColour( wx.Colour( 212, 208, 200 ) )

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_homeButton.Bind( wx.EVT_BUTTON, self.enter_home )
		# from wxasync import AsyncBind
		# AsyncBind( wx.EVT_BUTTON, self.enter_home, self.m_homeButton)
		self.m_folderUpButton.Bind( wx.EVT_BUTTON, self.leave_directory )
		self.m_refreshButton.Bind( wx.EVT_BUTTON, self.refresh_directory )
		self.m_settingsButton.Bind( wx.EVT_BUTTON, self.settings_form )
		self.m_importButton.Bind( wx.EVT_BUTTON, self.import_file )

		# Make grid available
		self.bFilesGridSizer = bFilesGridSizer

	def __del__( self ):
		pass

	# Virtual event handlers, overide them in your derived class
	def enter_home( self, event ):
		event.Skip()

	def leave_directory( self, event ):
		event.Skip()

	def import_file( self, event ):
		event.Skip()

	def refresh_directory( self, event ):
		event.Skip()

	def settings_form( self, event ):
		event.Skip()

