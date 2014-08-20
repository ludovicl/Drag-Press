# -*- coding: utf-8 -*-
'''
Created on 9 août 2014

@author: ludovicl
'''

# use with python stanalone_mac.py py2app
# To reduce size on Mac OS X : ditto --rsrc --arch x86_64 oldapp.app newapp.app


###############################
##############CX_FREEZE########
###############################
# from cx_Freeze import setup, Executable
#
# buildOptions = dict(
# #         compressed=True,
#         includes=["sys", "subprocess"],
# #         packages=["os", "wx"],
#         include_files=["Resources/images/texticon64.png", "Resources/images/imgicon64.png", "Resources/images/DragHere.png", "Resources/images/icon.icns"],
#         excludes=['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
#                     'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl', 'Tkconstants', 'Tkinter'],
#         optimize=2,
#         compressed=True,
#         icon='Resources/images/icon.icns',
#         include_in_shared_zip=True,
# #         site_packages=True,
# #         arch='x86_64',
#
# #         include_in_shared_zip=True,
# #         path=sys.path + ["modules"]
# )
# # OPTIONS = {'argv_emulation': True,
# #            'site_packages': True,
# #            'arch': 'x86_64',
# # #            'iconfile': 'lan.icns',  # if you want to add some ico
# #            'plist': {
# #                 'CFBundleName': 'Drag&Press',
# #                 'CFBundleShortVersionString':'1.0.0',  # must be in X.X.X format
# #                 'CFBundleVersion': '1.0.0',
# #                 'CFBundleIdentifier':'com.company.myapp',  # optional
# # #                 'NSHumanReadableCopyright': '@ Me 2013',  # optional
# # #                 'CFBundleDevelopmentRegion': 'English',  # optional - English is default
# #                 }
# #           }
#
# app = Executable(
#        # what to build
#        compress=True,
#        script="Entry.py",
#         icon='Resources/images/icon.icns',
# #        initScript=None,
# #         base="x86_64",
# #         arch="x86_64",
# #        targetDir=r"dist",
# #        strip=True,
# #        optimize=2,
#        excludes='',
#        targetName="Drag&Press.app",
# #        copyDependentFiles=True,
# #        appendScriptToExe=False,
# #        appendScriptToLibrary=False,
# #        icon=None
#        )
# #
# #
# setup(
#     name="Drag&Press",
#     version="0.1",
#     iconfile='Resources/images/icon.icns',
# #     icon='Resources/images/icon.icns',
#     description="Publish on a Wordpress blog by drag and drog",
#     options={'build_exe' : buildOptions},
#     executables=[app],
# #     icon='Resources/images/icon.icns',
# #     executables=[Executable("Entry.py", base=None)]
#
# )
#################################
#################################
#################################


############################
##############PY2APP########
############################
from setuptools import setup

APP = ['Entry.py']
DATA_FILES = [("images", ["Resources/images/texticon64.png", "Resources/images/imgicon64.png", "Resources/images/DragHere.png"])]
OPTIONS = dict(
#            argv_emulation=True,
            site_packages=True,
           arch='x86_64',
#            semi_standalone=True,
           strip=True,
           optimize=2,
           excludes='',
           iconfile='Resources/images/icon.icns',  # if you want to add some ico
#            debug_skip_macholib=True

           plist={
                'CFBundleName': 'Drag&Press',
                'CFBundleShortVersionString':'0.1.0',  # must be in X.X.X format
                'CFBundleVersion': '0.1.0',
#                 'CFBundleIdentifier':'com.company.myapp',  # optional
#                 'NSHumanReadableCopyright': '@ Me 2013',  # optional
#                 'CFBundleDevelopmentRegion': 'English',  # optional - English is default
                }
          )
setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
#################################
#################################
#################################







