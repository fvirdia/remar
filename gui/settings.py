# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class SettingsDialog
###########################################################################


class SettingsDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 510,266 ), style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bOuterSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_notebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_generalPanel = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText3 = wx.StaticText( self.m_generalPanel, wx.ID_ANY, u"Cloud API backend", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		bSizer10.Add( self.m_staticText3, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer10.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		m_backendChoiceChoices = [ u"rMAPI", u"rmapy" ]
		self.m_backendChoice = wx.Choice( self.m_generalPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_backendChoiceChoices, 0 )
		self.m_backendChoice.SetSelection( 0 )
		self.m_backendChoice.Enable( False )

		bSizer10.Add( self.m_backendChoice, 0, wx.ALL, 5 )


		bSizer9.Add( bSizer10, 0, wx.EXPAND, 5 )

		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self.m_generalPanel, wx.ID_ANY, u"Enable destructive operations (BEWARE, NO WARRANTY)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer11.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer11.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_destructiveCheckBox = wx.CheckBox( self.m_generalPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_destructiveCheckBox.Enable( False )

		bSizer11.Add( self.m_destructiveCheckBox, 0, wx.ALL, 5 )


		bSizer9.Add( bSizer11, 0, wx.EXPAND, 5 )

		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_generalPanel, wx.ID_ANY, u"rMAPI options" ), wx.VERTICAL )

		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText5 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"rMAPI binary", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer13.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer13.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_rmapiFilePicker = wx.FilePickerCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, u"rmapi", u"Select the rMAPI binary", u"*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST|wx.FLP_OPEN|wx.FLP_SMALL|wx.FLP_USE_TEXTCTRL )
		bSizer13.Add( self.m_rmapiFilePicker, 0, wx.ALL, 5 )


		sbSizer1.Add( bSizer13, 0, wx.EXPAND, 5 )


		bSizer9.Add( sbSizer1, 0, wx.EXPAND|wx.RIGHT|wx.LEFT, 5 )


		bSizer9.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )


		bSizer14.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_applyButton = wx.Button( self.m_generalPanel, wx.ID_ANY, u"Apply", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_applyButton, 0, wx.ALL|wx.ALIGN_BOTTOM, 5 )


		bSizer9.Add( bSizer14, 0, wx.EXPAND, 5 )


		self.m_generalPanel.SetSizer( bSizer9 )
		self.m_generalPanel.Layout()
		bSizer9.Fit( self.m_generalPanel )
		self.m_notebook.AddPage( self.m_generalPanel, u"Settings", True )
		self.m_aboutPanel = wx.Panel( self.m_notebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer12 = wx.BoxSizer( wx.VERTICAL )


		self.m_aboutPanel.SetSizer( bSizer12 )
		self.m_aboutPanel.Layout()
		bSizer12.Fit( self.m_aboutPanel )
		self.m_notebook.AddPage( self.m_aboutPanel, u"About", False )

		bOuterSizer.Add( self.m_notebook, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bOuterSizer )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_rmapiFilePicker.Bind( wx.EVT_FILEPICKER_CHANGED, self.rmapi_binary_changed )
		self.m_applyButton.Bind( wx.EVT_BUTTON, self.apply_settings )


	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def rmapi_binary_changed( self, event ):
		event.Skip()


	def apply_settings( self, event ):
		event.Skip()


