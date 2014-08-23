'''
Created on 18 août 2014

@author: ludovicl
'''
import sys
if sys.platform.startswith("darwin"):
    app = BUNDLE(exe,
              appname='Drag&Press',
              version='1.0')
