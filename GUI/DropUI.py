'''
Created on 30 juil. 2014

@author: ludovicl
'''
import wx
import sys
import plistlib
from Publisher import Publish
import threading
import os
import imp
import mimetypes


def main_is_frozen() :
    return (hasattr(sys, "frozen") or  # new py2exe
        hasattr(sys, "importers")  # old py2exe
        or imp.is_frozen("__main__"))  # tools/freeze

def get_main_dir() :
    if main_is_frozen() :
        return os.path.dirname("../Resources/images/")
    return "Resources/images/"  # os.path.dirname(sys.argv[0] + "/../Resources/images/")


class FileDrop(wx.FileDropTarget) :
    def __init__(self, window, content_to_upload, files_to_upload) :

        self.files_to_upload = []
        self.content_to_upload = []
        self.files_to_upload = files_to_upload
        self.content_to_upload = content_to_upload

        wx.FileDropTarget.__init__(self)
        self.win = window
        self.il = wx.ImageList(64, 64)
        self.win.SetImageList(self.il, wx.IMAGE_LIST_SMALL)


    def OnDropFiles(self, x, y, filenames):

        for name in filenames:
            try:

                type = mimetypes.guess_type(name)

                if type[0] is not None :
                    if type[0][:5] == "image" :
                        bitmap = wx.Image(get_main_dir() + "/imgicon64.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
                        self.files_to_upload.append(name)
                    else :  # if it's not a image it's a text
                        self.content_to_upload.append(name)
                        bitmap = wx.Image(get_main_dir() + "/texticon64.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
                else :  # if type is not recognized it's a text
                    self.content_to_upload.append(name)
                    bitmap = wx.Image(get_main_dir() + "/texticon64.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()

                file_name = os.path.split(''.join(name))
                self.idx1 = self.il.Add(bitmap)
                self.win.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
                self.win.InsertImageStringItem(0, file_name[1], self.idx1)

            except IOError, error:
                dlg = wx.MessageDialog(None, 'Error opening file\n' + str(error))
                dlg.ShowModal()
            except UnicodeDecodeError, error:
                dlg = wx.MessageDialog(None, 'Cannot open non ascii files\n' + str(error))
                dlg.ShowModal()


class DropFile(wx.Frame) :

    def __init__(self, parent, id, title) :
        self.files_to_upload = []
        self.content_to_upload = []

        wx.Frame.__init__(self, parent, id, title, style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX, size=(450, 400))

        ####Menu bar######
        menu_bar = wx.MenuBar()
        help_menu = wx.Menu()

        pref = help_menu.Append(wx.ID_PREFERENCES, "&Preferences")
        abt = help_menu.Append(wx.ID_ABOUT, "&About")

        self.Bind(wx.EVT_MENU, self.OnAbout, abt)
        self.Bind(wx.EVT_MENU, self.OnPrefs, pref)

        menu_bar.Append(help_menu, '&Help')
        self.SetMenuBar(menu_bar)
        ###################

        self.panel = wx.Panel(self)
        self.list = wx.ListCtrl(self.panel, size=(450, 330), style=wx.LC_REPORT | wx.LC_NO_HEADER)

        self.btn_publish = wx.Button(self.panel, 1, "Publish", pos=(350, 337))
        self.btn_publish.Bind(wx.EVT_BUTTON, self.OnButtonPublish)

        print get_main_dir()
        img = wx.Image(get_main_dir() + "/DragHere.png", wx.BITMAP_TYPE_PNG)
        wx.StaticBitmap(self.panel, -1, wx.BitmapFromImage(img), pos=(200, 333))

        self.btn_delete = wx.Button(self.panel, wx.ID_DELETE, pos=(2, 337))
        self.btn_delete.Bind(wx.EVT_BUTTON, self.OnButtonDelete)

        self.list.InsertColumn(0, '')
        self.list.SetColumnWidth(0, 450)
        dt = FileDrop(self.list, self.content_to_upload, self.files_to_upload,)
        self.list.SetDropTarget(dt)

        self.Centre()
        self.Show(True)


    def OnPrefs(self, event):
        self.dlg_prefs = wx.Dialog(self, -1, "Informations", size=(300, 200))

        panel = wx.Panel(self.dlg_prefs, -1)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        box_url = wx.BoxSizer(wx.HORIZONTAL)
        box_login = wx.BoxSizer(wx.HORIZONTAL)
        box_pwd = wx.BoxSizer(wx.HORIZONTAL)
        box_btn = wx.BoxSizer(wx.HORIZONTAL)

        url, login, pwd = self._get_url_log_pwd()

        url_label = wx.StaticText(panel, -1, "WP blog URL :")
        self.url_text = wx.TextCtrl(panel, -1, url, size=(75, -1))

        login_label = wx.StaticText(panel, -1, "Login :")
        self.login_text = wx.TextCtrl(panel, -1, login, size=(75, -1))

        pwd_label = wx.StaticText(panel, -1, "Password :")
        self.pwd_text = wx.TextCtrl(panel, -1, pwd, size=(75, -1), style=wx.TE_PASSWORD)

        btn_ok = wx.Button(panel, label='Ok')
        btn_cancel = wx.Button(panel, label='Cancel')

        btn_ok.Bind(wx.EVT_BUTTON, self.OnButtonOkPrefs)
        btn_cancel.Bind(wx.EVT_BUTTON, self.OnButtonCancelPrefs)

        box_url.Add(url_label, 0, wx.ALL, 5)
        box_url.Add(self.url_text, wx.ALL , wx.ALL, 5)
        box_login.Add(login_label, 0, wx.ALL, 5)
        box_login.Add(self.login_text, wx.ALL , wx.ALL, 5)
        box_pwd.Add(pwd_label, 0, wx.ALL, 5)
        box_pwd.Add(self.pwd_text, wx.ALL, wx.ALL, 5)
        box_btn.Add(btn_ok, wx.ALIGN_CENTER, wx.ALL, 5)
        box_btn.Add(btn_cancel, wx.ALIGN_CENTER, wx.ALL, 5)

        main_sizer.Add(box_url, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(box_login, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(box_pwd, 0, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(box_btn, 0, wx.ALL | wx.EXPAND, 5)

        panel.SetSizer(main_sizer)
        self.dlg_prefs.ShowModal()


    def OnAbout(self, event):
        import wx.html
        about_dial = wx.Dialog(self, -1, "About", size=(300, 200))
        panel = wx.Panel(about_dial, -1)
        html = wx.html.HtmlWindow(panel)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        html.SetStandardFonts()
        html.SetPage("<center> <b> Drag&Drop </b>"
                "<br> <br>  Developper : Ludovic Lardies"
                "<br> <br>Contact : <a href=\"ludovic@lardies.fr\">ludovic@lardies.fr</a>"
                "</center>")

        main_sizer.Add(html, 1, wx.EXPAND, 10)
        panel.SetSizer(main_sizer)
        about_dial.ShowModal()


    def OnButtonOkPrefs(self, event):
        if sys.platform == 'darwin' :
            pwx_data = plistlib.Data(str(self.pwd_text.GetValue()))
            plistlib.writePlist([self.url_text.GetValue(), self.login_text.GetValue(), pwx_data], 'Drag&Press')
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
        self.upld_prog_label = wx.StaticText(self.panel, 1, "Upload in progress", pos=(0, 330), size=(450, 80), style=wx.ALIGN_CENTRE)
        self.upld_prog_label.SetBackgroundColour((118, 238, 198))
        self.btn_publish.Show(False)
        self.btn_delete.Show(False)

        thread_publi = threading.Thread(target=self.publish_post)

        thread_publi.start()


    def publish_post(self) :
        try :
            url, login, pwd = self._get_url_log_pwd()
            publi = Publish.Publish(url, login, pwd);
            return_val = publi.post_article(self.content_to_upload, self.files_to_upload)
        except Exception :
            return_val = 'Check your website, login, password in preferences '

        wx.CallAfter(self.box_result_post, return_val)

    def box_result_post(self, return_val):
        if return_val == 'Post successful!':
            wx.MessageBox(return_val, 'Success',
                          wx.OK | wx.ICON_INFORMATION)
        else :
            wx.MessageBox(return_val, 'Error !',
                          wx.OK | wx.ICON_INFORMATION)

        self.upld_prog_label.Hide()
        self.btn_publish.Show(True)
        self.btn_delete.Show(True)

    def _get_url_log_pwd(self) :
        if sys.platform == 'darwin' :
            try :
                url_login_pwd = plistlib.readPlist('Drag&Press')
                url = url_login_pwd[0]
                login = url_login_pwd[1]
                pwd = url_login_pwd[2].data
            except Exception:
                url = "http://mydomain"
                login = "login"
                pwd = "password"
            return url, login, pwd


class DragPressApp(wx.App) :
    def OnInit(self):
        df = DropFile(None, -1, 'Drag&Press')
        df.Show(True)
        df.Centre()
        return True
