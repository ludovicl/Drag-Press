# -*- coding: utf-8 -*-

'''
Created on 22 août 2014

@author: ludovicl

'''
from os import remove, removedirs, path
from appdirs import user_data_dir

if __name__ == '__main__':
    print user_data_dir("Drag&Press")
    if path.exists(user_data_dir("Drag&Press")):
        remove(user_data_dir("Drag&Press/Preferences"))
        removedirs(user_data_dir("Drag&Press"))
