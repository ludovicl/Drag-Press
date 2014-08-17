'''
Created on 30 juil. 2014

@author: ludovicl
'''
import wx._core
import wx.html
import sys
from Publisher import Publish
import threading
import os
import imp
import mimetypes
from DataStore.PrefStore import PrefStore
from unidecode import unidecode

def main_is_frozen() :
    return (hasattr(sys, "frozen") or  # new py2exe
        hasattr(sys, "importers")  # old py2exe
        or imp.is_frozen("__main__"))  # tools/freeze

def get_main_dir() :
    if main_is_frozen() :
        return os.path.dirname("../Resources/images/")
    return "Resources/images/"  # os.path.dirname(sys.argv[0] + "/../Resources/images/")


class FileDrop(wx._core.FileDropTarget) :
    def __init__(self, window, content_to_upload, files_to_upload) :

        self.files_to_upload = []
        self.content_to_upload = []
        self.files_to_upload = files_to_upload
        self.content_to_upload = content_to_upload

        wx._core.FileDropTarget.__init__(self)
        self.win = window
        self.il = wx._core.ImageList(64, 64)
        self.win.SetImageList(self.il, wx._core.IMAGE_LIST_SMALL)


    def OnDropFiles(self, x, y, filenames):

        for name in filenames:
            try:

                type = mimetypes.guess_type(name)

                if type[0] is not None :
                    if type[0][:5] == "image" :
                        bitmap = wx._core.Image(get_main_dir() + "/imgicon64.png", wx._core.BITMAP_TYPE_PNG).ConvertToBitmap()
                        self.files_to_upload.append(name)
                    else :  # if it's not a image it's a text
                        self.content_to_upload.append(name)
                        bitmap = wx._core.Image(get_main_dir() + "/texticon64.png", wx._core.BITMAP_TYPE_PNG).ConvertToBitmap()
                else :  # if type is not recognized it's a text
                    self.content_to_upload.append(name)
                    bitmap = wx._core.Image(get_main_dir() + "/texticon64.png", wx._core.BITMAP_TYPE_PNG).ConvertToBitmap()

                file_name = os.path.split(''.join(name))
                self.idx1 = self.il.Add(bitmap)
                self.win.SetImageList(self.il, wx._core.IMAGE_LIST_SMALL)
                self.win.InsertImageStringItem(0, file_name[1], self.idx1)

            except IOError, error:
                dlg = wx._core.MessageDialog(None, 'Error opening file\n' + str(error))
                dlg.ShowModal()
            except UnicodeDecodeError, error:
                dlg = wx._core.MessageDialog(None, 'Cannot open non ascii files\n' + str(error))
                dlg.ShowModal()


class DropFile(wx._core.Frame) :

    def __init__(self, parent, id, title) :
        self.files_to_upload = []
        self.content_to_upload = []

        if sys.platform == 'darwin':
            wx._core.Frame.__init__(self, parent, id, title, style=wx._core.SYSTEM_MENU | wx._core.CAPTION | wx._core.CLOSE_BOX, size=(450, 400))
        else :
            wx._core.Frame.__init__(self, parent, id, title, style=wx._core.SYSTEM_MENU | wx._core.CAPTION | wx._core.CLOSE_BOX, size=(450, 420))

        ####Menu bar######
        menu_bar = wx._core.MenuBar()
        info_menu = wx._core.Menu()

        menu_bar.Append(info_menu, '&Information')

        pref = info_menu.Append(wx._core.ID_PREFERENCES, "&Preferences")
        abt = info_menu.Append(wx._core.ID_ABOUT, "&About")


        self.Bind(wx._core.EVT_MENU, self.OnAbout, abt)
        self.Bind(wx._core.EVT_MENU, self.OnPrefs, pref)

        self.SetMenuBar(menu_bar)
        ###################

        self.panel = wx._core.Panel(self)
        self.list = wx._core.ListCtrl(self.panel, size=(460, 330), style=wx._core.LC_REPORT | wx._core.LC_NO_HEADER)

        self.btn_publish = wx._core.Button(self.panel, 1, "Publish", pos=(350, 337))
        self.btn_publish.Bind(wx._core.EVT_BUTTON, self.OnButtonPublish)

        print get_main_dir()
        self.drag_here_img = wx._core.Image(get_main_dir() + "/DragHere.png", wx._core.BITMAP_TYPE_PNG)
        wx._core.StaticBitmap(self.panel, -1, wx._core.BitmapFromImage(self.drag_here_img), pos=(200, 333))

        self.btn_delete = wx._core.Button(self.panel, wx._core.ID_DELETE, pos=(2, 337))
        self.btn_delete.Bind(wx._core.EVT_BUTTON, self.OnButtonDelete)

        self.list.InsertColumn(0, '')
        self.list.SetColumnWidth(0, 450)
        dt = FileDrop(self.list, self.content_to_upload, self.files_to_upload,)
        self.list.SetDropTarget(dt)

        self.Centre()
        self.Show(True)


    def OnPrefs(self, event):
        self.dlg_prefs = wx._core.Dialog(self, -1, "Informations", size=(300, 200))

        panel = wx._core.Panel(self.dlg_prefs, -1)

        main_sizer = wx._core.BoxSizer(wx._core.VERTICAL)
        box_url = wx._core.BoxSizer(wx._core.HORIZONTAL)
        box_login = wx._core.BoxSizer(wx._core.HORIZONTAL)
        box_pwd = wx._core.BoxSizer(wx._core.HORIZONTAL)
        box_btn = wx._core.BoxSizer(wx._core.HORIZONTAL)

        url, login, pwd = PrefStore.get_data_stored()

        url_label = wx._core.StaticText(panel, -1, "WP blog URL :")
        self.url_text = wx._core.TextCtrl(panel, -1, url, size=(75, -1))

        login_label = wx._core.StaticText(panel, -1, "Login :")
        self.login_text = wx._core.TextCtrl(panel, -1, login, size=(75, -1))

        pwd_label = wx._core.StaticText(panel, -1, "Password :")
        self.pwd_text = wx._core.TextCtrl(panel, -1, pwd, size=(75, -1), style=wx._core.TE_PASSWORD)

        btn_ok = wx._core.Button(panel, label='Ok')
        btn_cancel = wx._core.Button(panel, label='Cancel')

        btn_ok.Bind(wx._core.EVT_BUTTON, self.OnButtonOkPrefs)
        btn_cancel.Bind(wx._core.EVT_BUTTON, self.OnButtonCancelPrefs)

        box_url.Add(url_label, 0, wx._core.ALL, 5)
        box_url.Add(self.url_text, wx._core.ALL , wx._core.ALL, 5)
        box_login.Add(login_label, 0, wx._core.ALL, 5)
        box_login.Add(self.login_text, wx._core.ALL , wx._core.ALL, 5)
        box_pwd.Add(pwd_label, 0, wx._core.ALL, 5)
        box_pwd.Add(self.pwd_text, wx._core.ALL, wx._core.ALL, 5)
        box_btn.Add(btn_ok, wx._core.ALIGN_CENTER, wx._core.ALL, 5)
        box_btn.Add(btn_cancel, wx._core.ALIGN_CENTER, wx._core.ALL, 5)

        main_sizer.Add(box_url, 0, wx._core.ALL | wx._core.EXPAND, 5)
        main_sizer.Add(box_login, 0, wx._core.ALL | wx._core.EXPAND, 5)
        main_sizer.Add(box_pwd, 0, wx._core.ALL | wx._core.EXPAND, 5)
        main_sizer.Add(box_btn, 0, wx._core.ALL | wx._core.EXPAND, 5)

        panel.SetSizer(main_sizer)
        self.dlg_prefs.ShowModal()


    def OnAbout(self, event):
        about_dial = wx._core.Dialog(self, -1, "About", size=(300, 200))
        panel = wx._core.Panel(about_dial, -1)
        html = wx.html.HtmlWindow(panel)
        main_sizer = wx._core.BoxSizer(wx._core.VERTICAL)

        html.SetStandardFonts()
        html.SetPage("<center> <b> Drag&Drop </b>"
                "<br> <br>  Developper : Ludovic Lardies"
                "<br> <br>Contact : <a href=\"ludovic@lardies.fr\">ludovic@lardies.fr</a>"
                "</center>")

        main_sizer.Add(html, 1, wx._core.EXPAND, 10)
        panel.SetSizer(main_sizer)
        about_dial.ShowModal()


    def OnButtonOkPrefs(self, event):
        PrefStore.set_data_to_stored(self.url_text.GetValue(), self.login_text.GetValue(), str(self.pwd_text.GetValue()))
        self.dlg_prefs.Close()


    def OnButtonCancelPrefs(self, event):
        self.dlg_prefs.Close()


    def OnButtonDelete(self, event):
        try :
            itm_selected = self.list.GetFocusedItem()
            itm_to_delete = self.list.GetItem(itm_selected, 0)
            str_itm_to_delete = itm_to_delete.GetText()

            for f in self.files_to_upload :
                if f.find(str_itm_to_delete) :
                    self.files_to_upload.remove(f)

            for f in self.content_to_upload :
                if f.find(str_itm_to_delete) :
                    self.content_to_upload.remove(f)

            if itm_selected != -1 :
                self.list.DeleteItem(itm_selected)
        except Exception :
            pass


    def OnButtonPublish(self, event) :
        self.upld_prog_label = wx._core.StaticText(self.panel, 1, "Upload in progress", pos=(0, 330), size=(450, 80), style=wx._core.ALIGN_CENTRE)
        self.upld_prog_label.SetBackgroundColour((118, 238, 198))
        self.btn_publish.Show(False)
        self.btn_delete.Show(False)
        self.drag_here_img.Show(False)

        thread_publi = threading.Thread(target=self.publish_post)

        thread_publi.start()


    def publish_post(self) :
        try :
            url, login, pwd = PrefStore.get_data_stored()
            publi = Publish.Publish(url, login, pwd);
            return_val = publi.post_article(self.content_to_upload, self.files_to_upload)
        except Exception :
            return_val = 'Check your website, login, password in preferences '

        wx._core.CallAfter(self.box_result_post, return_val)

    def box_result_post(self, return_val):
        if return_val == 'Post successful!':
            wx._core.MessageBox(return_val, 'Success',
                          wx._core.OK | wx._core.ICON_INFORMATION)
        else :
            wx._core.MessageBox(return_val, 'Error !',
                          wx._core.OK | wx._core.ICON_INFORMATION)

        self.upld_prog_label.Hide()
        self.btn_publish.Show(True)
        self.btn_delete.Show(True)
        self.drag_here_img.Show(True)


class DragPressApp(wx._core.App) :
    def OnInit(self):
        df = DropFile(None, -1, 'Drag&Press')
        df.Show(True)
        df.Centre()
        return True
