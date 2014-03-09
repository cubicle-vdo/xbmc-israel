#
#      Copyright (C) 2012 Tommy Winther
#      http://tommy.winther.nu
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html

import xbmc
import xbmcaddon
import urllib
import socket 
socket.setdefaulttimeout(5) # 5 seconds 
import os
import shutil
xbmc.Player().stop


ADDON       = xbmcaddon.Addon(id = 'script.tvguidedixie.o2ri')
datapath    = xbmc.translatePath(ADDON.getAddonInfo('profile'))
addonpath   = os.path.join(ADDON.getAddonInfo('path'), 'resources')
default_ini = os.path.join(addonpath, 'addons.ini')
current_ini = os.path.join(datapath, 'addons.ini')

if not os.path.exists(current_ini):
    try: os.makedirs(datapath)
    except: pass
    shutil.copy(default_ini, current_ini)


ooOOOoo = ''
def ttTTtt(i, t1, t2=[]):
	t = ooOOOoo
	for c in t1:
	  t += chr(c)
	  i += 1
	  if i > 1:
	   t = t[:-1]
	   i = 0  
	for c in t2:
	  t += chr(c)
	  i += 1
	  if i > 1:
	   t = t[:-1]
	   i = 0
	return t

path = os.path.join(datapath, 'addons.ini')
try:
    url = 'https://dl.dropboxusercontent.com/u/5461675/addons.ini'
    urllib.urlretrieve(url, path)
except:
    pass


busy = None
try:
    import xbmcgui
    busy = xbmcgui.WindowXMLDialog('DialogBusy.xml', '')
    busy.show()

    try:    busy.getControl(10).setVisible(False)
    except: pass

except:
    busy = None

import buggalo
import gui


buggalo.GMAIL_RECIPIENT = 'mamitj@gmail.com'


try:
    w = gui.TVGuide()

    if busy:
        busy.close()
        busy = None

    w.doModal()
    del w

except Exception:
    buggalo.onExceptionRaised()