#-------------------------------------------------------------------------------
# Name:         Lending Club Strategy Generator
# Purpose:      To generate note choosing strategies on LendingClub.com
# Author:       Zachariah Kendall
# Created:      04/01/2013
# Version:      0.5
#-------------------------------------------------------------------------------

# Global imports
import wx, os

# Local imports
import Generator, Db

# Initialize Db #
db = Db.Db()

# IDs #
APP_EXIT = 1
APP_OPEN_CSV = 2
APP_OPEN_DB = 3
APP_GENERATE = 4


    class MyWindow(wx.Frame):
    """This is the GUI class"""
    def __init__(self, *args, **kwargs):
        super(MyWindow, self).__init__(*args, **kwargs)
        self.SetSize((250, 300))

        self.InitUI()

        # Window Attributes #
        self.Centre()
        self.SetTitle('LendingClub Strategy Generator')
        self.Show(True)

    def InitUI(self):
        self.currentDirectory = os.getcwd()

        # Main panel #
        panel = wx.Panel(self)
        panel.SetBackgroundColour('#4f5049')
        vbox = wx.BoxSizer(wx.VERTICAL)
        # Inner
        midPan = wx.Panel(panel)
        midPan.SetBackgroundColour('#ededed')
        vbox.Add(midPan, 1, wx.EXPAND | wx.ALL, 10)
        # Top Button Set
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        btn1 = wx.Button(midPan, label='Generate')
        btn1.Bind(wx.EVT_BUTTON, Generator.runGenerator(db))
        hbox1.Add(btn1)



        panel.SetSizer(vbox)

        # File Menu #
        fileMenu = wx.Menu()
        quit_mi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
        open_csv_mi = wx.MenuItem(fileMenu, APP_OPEN_CSV, '&Open CSV')
        open_db_mi = wx.MenuItem(fileMenu, APP_OPEN_DB, '&Open DB')


        fileMenu.AppendItem(open_csv_mi)
        fileMenu.AppendItem(open_db_mi)
        fileMenu.AppendItem(quit_mi)

        self.Bind(wx.EVT_MENU, self.OnQuit, id=APP_EXIT)
        self.Bind(wx.EVT_MENU, self.onOpenCSV, id=APP_OPEN_CSV)
        self.Bind(wx.EVT_MENU, self.onOpenDb, id=APP_OPEN_DB)


        # Menu Bar #
        menubar = wx.MenuBar()
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)


    def OnQuit(self, e):
        print "Quitted!"
        db.close()
        print "Db closed"
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
            paths = dlg.GetPaths()
            Db.csvFileAddress = paths
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
            paths = dlg.GetPaths()
            Db.dbFileAddress = paths
        dlg.Destroy()


##########################################################

def main():
    ex = wx.App()
    MyWindow(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()
