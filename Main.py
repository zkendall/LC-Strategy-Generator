#--------------------------------------------------------------------------------------------
# Name:         Lending Club Strategy Generator
# Purpose:      To generate strategies to choose notes on LendingClub.com
# Author:       Zachariah Kendall
# Created:      04/01/2013
#--------------------------------------------------------------------------------------------

# Global imports
import wx, os, logging
import wx.lib.delayedresult as delayedresult

# Local imports
import Generator, Db

# Initialize Db #
db = Db.Db()

# IDs #
APP_EXIT = 1
APP_OPEN_CSV = 2
APP_OPEN_DB = 3
#APP_GENERATE = 4


class MyWindow(wx.Frame):
    """This is the GUI class"""
    global  db;
    def __init__(self, *args, **kwargs):
        super(MyWindow, self).__init__(*args, **kwargs)
        self.SetSize((250, 300))
        # Initialize User Interface #
        self.InitUI()

    def InitUI(self):
        self.currentDirectory = os.getcwd()

        # Main Panels #
        panBottom = wx.Panel(self)
        panBottom.SetBackgroundColour('#555555')
        vbox = wx.BoxSizer(wx.VERTICAL)
        # Inner
        panTop = wx.Panel(self);
        panTop.SetBackgroundColour('#eeeeee')
        vbox.Add(panTop, 1, wx.EXPAND | wx.ALL, 10)
        vbox.Add(panBottom, 1, wx.EXPAND | wx. ALL, 10)
        self.SetSizer(vbox)


        # Top Button Set
        self.btnGenerate = wx.Button(panTop, -1, "Generate")
        self.btnGenerate.Bind(wx.EVT_BUTTON, self.onGenerate)
        self.btnAbort = wx.Button(panTop, -1, "Abort")
        self.btnAbort.Bind(wx.EVT_BUTTON, self.onAbort)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.btnGenerate, 0, wx.ALL, 5)
        hsizer.Add(self.btnAbort, 0, wx.ALL, 5)
        panTop.SetSizer(hsizer)

        # File Menu #
        fileMenu = wx.Menu()
        quit_mi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
        open_csv_mi = wx.MenuItem(fileMenu, APP_OPEN_CSV, '&Open CSV')
        open_db_mi = wx.MenuItem(fileMenu, APP_OPEN_DB, '&Open DB')

        fileMenu.AppendItem(open_csv_mi)
        fileMenu.AppendItem(open_db_mi)
        fileMenu.AppendItem(quit_mi)

        self.Bind(wx.EVT_MENU, self.OnQuit, quit_mi)
        self.Bind(wx.EVT_MENU, self.onOpenCSV, open_csv_mi)
        self.Bind(wx.EVT_MENU, self.onOpenDb, open_db_mi)


        # Menu Bar #
        menubar = wx.MenuBar()
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        # Status Bar #
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')
        self.statusbar.Show()


    def OnQuit(self, e):
        print "Quitting!"
        db.close()
        self.Close()

    def onOpenCSV(self, e):
        """Create and show the Open FileDialog"""
        dlg = wx.FileDialog(
                self, message="Choose a Lending Club CSV file",
                defaultDir=self.currentDirectory,
                defaultFile="",
                wildcard="CSV file (*.csv)|*.csv|All files (*.*)|*.*",
                style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
                )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            db.buildDb(path);
        dlg.Destroy()

    def onOpenDb(self, e):
        """Create and show the Open FileDialog"""
        dlg = wx.FileDialog(
                self, message="Choose a Db file containing Lending Club loans",
                defaultDir = self.currentDirectory,
                defaultFile = "",
                wildcard = "CSV file (*.db)|*.db|All files (*.*)|*.*",
                style = wx.OPEN | wx.CHANGE_DIR
                )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            db.connectToDb(path)
        dlg.Destroy()



    def onGenerate(self, e):
        """Run Generator"""
        self.btnGenerate.Enable(False)
        self.btnAbort.Enable(True)
        self.generator_thread = Generator.MyThread(db)  # Pass in database
        self.generator_thread.start()
        
        # Other options I experimented with #
        # thread.start_new_thread(Generator.runGenerator,(db))
        # delayedresult.startWorker(self.resultConsumer, # Send finished result
        #                           Generator.runGenerator(db))


    # def resultConsumer(self, delayedresult):
    #     # reinable disabled interface.
    #     self.btnGenerate.Enable(True)
    #     self.btnAbort.Enable(False)
       

    def onAbort(self, e):
        print "Aborting generator..."
        self.generator_thread.stop();
        self.btnAbort.SetLabel("Aborting")
        self.generator_thread.join()
        self.btnGenerate.Enable(True)
        self.btnAbort.Enable(False)
        self.btnAbort.SetLabel("Abort")
        




##########################################################

class MyApp(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = MyWindow(None)
        self.frame.Show()
        #self.frame.Centre()
        self.frame.SetTitle('LendingClub Strategy Generator')

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
