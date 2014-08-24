# -*- coding: utf-8 -*-
'''
Created on 9 août 2014

@author: ludovicl
'''

import sys


# py2app (Mac OS X)
if sys.argv[1] == 'py2app' :

    # Module : py2app
    # usage : python standalone_setup.py py2app
    # To reduce size on Mac OS X : ditto --rsrc --arch x86_64 oldapp.app newapp.app

    from setuptools import setup


    ####Remove plist executable######
    setup(
        app=['RemovePreferences.py'],
        setup_requires=['py2app'],
        options={'py2app': dict(strip=True, optimize=2,)},
        )


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




# cx_freeze setup (GNU/Linux)
if sys.argv[1] == "install" :

    # Module : cx_freeze
    # usage : python standalone_setup.py install

    from cx_Freeze import setup, Executable

    ####Remove plist executable######
    setup(
    name="RemovePref",
    executables=[Executable(
             script="RemovePreferences.py",
             initScript=None,
             targetName="RemovePreferences",
             appendScriptToLibrary=False,
             )],
      )

    options = {
        'build_exe': {
        'compressed': True,
            'include_files':["Resources/images/texticon64.png", "Resources/images/imgicon64.png", "Resources/images/DragHere.png", "Resources/images/icon.png"],
            'excludes':['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
                        'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
                        'Tkconstants', 'Tkinter'],
        }
    }

    app = Executable(
           script="Entry.py",
           initScript=None,
           targetName="Drag&Press",
           compress=True,
           base=None,
           copyDependentFiles=True,
           appendScriptToExe=False,
           appendScriptToLibrary=False,
           icon="Resources/images/icon.png",
           )

    setup(
        name="Drag&Press",
        author='ludovicl',
        # icon =  "Resources/images/icon.png",
        version="0.1",
        description="Publish on a Wordpress blog by drag and droging",
        options=options,
        executables=[app],
    )


