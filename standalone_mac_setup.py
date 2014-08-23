# -*- coding: utf-8 -*-
'''
Created on 9 août 2014

@author: ludovicl
'''

# use with python stanalone_mac.py py2app
# To reduce size on Mac OS X : ditto --rsrc --arch x86_64 oldapp.app newapp.app

from setuptools import setup

APP = ['Entry.py']
REMOVE_PREF = ['RemovePreferences.py']

DATA_FILES = [("images", ["Resources/images/texticon64.png", "Resources/images/imgicon64.png", "Resources/images/DragHere.png"])]

OPTIONS = dict(
            site_packages=True,
           arch='x86_64',
           strip=True,
           optimize=2,
           excludes='',
           iconfile='Resources/images/icon.icns',
           plist={
                'CFBundleName': 'Drag&Press',
                'CFBundleShortVersionString':'0.1.0',
                'CFBundleVersion': '0.1.0',
                }
          )

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    )


######################
####Remove plist######
setup(
    app=['RemovePreferences.py'],
    setup_requires=['py2app'],
    options={'py2app': dict(strip=True, optimize=2,)},

    )




