# -*- coding: utf-8 -*-
'''
Created on 14 août 2014

@author: ludovicl
'''
import sys
import plistlib
import os
from appdirs import *

class PrefStore(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    @classmethod
    def set_data_to_stored(self, url, text, pwd):

        pwd_data = plistlib.Data(pwd)
        if not os.path.exists(user_data_dir("Drag&Press")):
                os.makedirs(user_data_dir("Drag&Press"))

        if sys.platform == 'darwin' :
            plistlib.writePlist([url, text, pwd_data], user_data_dir("Drag&Press/Preferences", "ludovicl"))
        elif sys.platform == 'win32':
            if not os.path.exists(user_data_dir("Drag&Press")):
                os.makedirs(user_data_dir("Drag&Press"))
    @classmethod
    def get_data_stored(self):
        if sys.platform == 'darwin' :
            try :
                url_login_pwd = plistlib.readPlist(user_data_dir("Drag&Press/Preferences", "ludovicl"))
                url = url_login_pwd[0]
                login = url_login_pwd[1]
                pwd = url_login_pwd[2].data
            except Exception:
                url = "http://mydomain"
                login = "login"
                pwd = "password"
            return url, login, pwd
