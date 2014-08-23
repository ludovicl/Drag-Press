# -*- coding: utf-8 -*-

'''
Created on 22 août 2014

@author: ludovicl

'''
import os
from appdirs import user_data_dir

if __name__ == '__main__':
    print user_data_dir("Drag&Press")
    if os.path.exists(user_data_dir("Drag&Press")):
        os.remove(user_data_dir("Drag&Press/Preferences"))
        os.removedirs(user_data_dir("Drag&Press"))
