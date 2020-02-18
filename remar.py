#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import wx 
from backend.rmapi import rMAPIException, rMAPIWrapper
from gui.grid_elements import DirectoryWidget, FileWidget
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
from asyncio.events import get_event_loop
import asyncio
import gui.main
import gui.settings
from random import randint
import wx.lib.newevent
import os.path
import os
import configparser


LoadingEvent, EVT_LOADING = wx.lib.newevent.NewEvent()


class SettingsDialog(gui.settings.SettingsDialog):
    def __init__(self, parent):
        gui.settings.SettingsDialog.__init__(self, parent)
        self.parent = parent
        self.rMAPI_binary = self.parent.config["DEFAULT"].get("rMAPI_path", "rmapi")
        self.m_rmapiFilePicker.SetPath(self.rMAPI_binary)

    def rmapi_binary_changed( self, event ):
        self.rMAPI_binary = event.GetPath()
        event.Skip()

    def apply_settings( self, event ):
        if self.parent.loading:
            self.parent.error("Busy loading")
            return

        # first, verify that the binary exists
        if not os.path.isfile(self.rMAPI_binary):
            self.parent.error("Binary doesn't exist.")
            return

        # and is executable
        if not os.access(self.rMAPI_binary, os.X_OK):
            self.parent.error("Binary is not executable.")
            return

        # and it's not this file (to avoid a loop)
        if self.rMAPI_binary == os.path.realpath(__file__):
            self.parent.error("Wrong rMAPI binary.")
            return

        # then, save setting and reload config
        self.parent.config["DEFAULT"]["rMAPI_path"] = self.rMAPI_binary
        with open(self.parent.config_file, 'w') as configfile:
            self.parent.config.write(configfile)

        self.parent.rmapi.set_binary(self.rMAPI_binary)

        event.Skip()


class AppFrame(gui.main.MainFrame):

    def __init__(self,parent):
        gui.main.MainFrame.__init__(self,parent)
        self.grid_content = []
        self.current_dir = ""
        self.error_count = 0

        # load settings
        self.config_file = os.path.expanduser("~") + "/.remar"
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

        # load api
        # TODO: have both rMAPI and rmapy options
        rmapi_binary = self.config["DEFAULT"].get("rMAPI_path", "rmapi")
        self.rmapi = rMAPIWrapper(rmapi_binary)

        # Deal with "loading" feedback in the status bar
        self.loading = False
        AsyncBind(EVT_LOADING, self.loading_status, self)

        # List the root directory
        StartCoroutine(self.open_directory("/"), self)

    def error(self, message):
        """Provide error messages on the status bar.
        """
        self.error_count += 1
        # wx.LogError(message)
        self.m_statusBar.SetStatusText("Error %d: %s" % (self.error_count, message), i=0)

    async def loading_status(self, event):
        """Provide visual feedback of 'loading happening' in the status bar.
        """
        periods = 0
        self.loading = True
        while self.loading:
            self.m_statusBar.SetStatusText("Loading%s" % ("." * periods), i=1)
            periods = (periods + 1) % 4
            await asyncio.sleep(1)
        self.m_statusBar.SetStatusText("", i=1)

    async def open_directory(self, path):
        """Navigate to the given directory and list the contents in the main window.

        :param path:    remote directory path
        """
        try:
            wx.PostEvent(self, LoadingEvent())
            self.m_statusBar.SetStatusText("Opening %s" % path, i=0)
            await self._populate_grid(path)
            self.current_dir = path
            self.m_locationBar.Value = path
            self.m_statusBar.SetStatusText("Opened %s" % path, i=0)
        except rMAPIException as e:
            self.error(str(e))
        finally:
            self.loading = False

    async def _populate_grid(self, path):
        directories, files = await self.rmapi.ls(path)

        # clear list of grid entries
        for _ in range(len(self.grid_content)-1, -1, -1):
            self.bFilesGridSizer.Hide(_)
            self.bFilesGridSizer.Remove(_)

        self.grid_content = []
        
        # clear sizer of grid
        self.bFilesGridSizer.Clear()

        # populate grid
        for entry in directories:
            self._add_directory_widget(entry)
        for entry in files:
            self._add_file_widget(entry)

    def _add_directory_widget(self, label):
        obj = DirectoryWidget(self, label)
        self.grid_content.append(obj)

    def _add_file_widget(self, label):
        obj = FileWidget(self, label)
        self.grid_content.append(obj)

    def enter_directory( self, event, label):
        """On a DirectoryWidget click, it navigates to the corresponding subdirectory.
        """
        directory = label
        path = os.path.normpath(self.current_dir + "/" + directory)
        # corner case: normpath("//") == "//"
        if path[:2] == '//':
            path = path[1:]
        StartCoroutine(self.open_directory(path), self)
        event.Skip()

    def export_file( self, event, label ):
        """Use the OS's directory picking dialog to choose a directory to save
        the remote file to.
        """
        if self.loading:
            self.error("Busy loading")
            return

        with wx.DirDialog (None, "Choose output directory", "",
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            try:
                # download the file
                wx.PostEvent(self, LoadingEvent())
                self.m_statusBar.SetStatusText("Exporting %s to %s" % (label, pathname), i=0)
                StartCoroutine(self.rmapi.geta(
                    "%s/%s" % (self.current_dir if self.current_dir != "/" else "", label), 
                    directory=pathname, 
                    cb=self.file_exported_cb
                ), self)
            except IOError:
                e = "Cannot save current data in file '%s'." % pathname
                self.error(e)
        event.Skip()

    def import_file( self, event ):
        """Use the OS's file picking dialog to choose a PDF file to upload to
        the current remote directory.
        """
        if self.loading:
            self.error("Busy loading")
            return

        with wx.FileDialog(
            self, "Open PDF file", wildcard="PDF files (*.pdf)|*.pdf",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r'):
                    # if the file exists, upload it
                    wx.PostEvent(self, LoadingEvent())
                    self.m_statusBar.SetStatusText("Uploading %s" % pathname, i=0)
                    StartCoroutine(self.rmapi.put(
                        pathname, directory=self.current_dir, cb=self.file_uploaded_cb
                    ), self)
            except IOError:
                e = "Cannot open file '%s'." % pathname
                self.error(e)
            event.Skip()

    def file_uploaded_cb(self, pathname):
        """File upload callback. Updates status bar, unlocks the gui, and 
        refreshes the current directory listing.
        """
        self.m_statusBar.SetStatusText("Uploaded %s" % pathname, i=0)
        self.loading = False
        self.refresh_directory(None)

    def file_exported_cb(self, label, pathname):
        """File export callback. Updates the status bar, and unlocks the gui.
        """
        self.m_statusBar.SetStatusText("Exported %s to %s" % (label, pathname), i=0)
        self.loading = False

    def enter_home( self, event ):
        """Opens the root directory.
        """
        StartCoroutine(self.open_directory('/'), self)
        event.Skip()

    def refresh_directory( self, event ):
        """Refreshes the current directory listing.
        """
        StartCoroutine(self.open_directory(self.current_dir), self)
        if event:
            event.Skip()

    def leave_directory( self, event ):
        """Loads the parent directory.
        """
        if self.current_dir not in ['/', '']:
            path = "/".join(self.current_dir.split('/')[:-1])
            if path == "":
                path = "/"
            StartCoroutine(self.open_directory(path), self)
        event.Skip()

    def settings_form( self, event ):
        dialog = SettingsDialog(self)
        dialog.Show(True)
        event.Skip()


if __name__ == "__main__":
    app = WxAsyncApp(False)
    frame = AppFrame(None)
    frame.Show(True)

    # start the application
    loop = get_event_loop()
    loop.run_until_complete(app.MainLoop())
