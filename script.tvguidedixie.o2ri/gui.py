#
#      Copyright (C) 2013 Tommy Winther
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
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import datetime
import threading
import time
import xbmc
import xbmcgui

import source as src
from notification import Notification
from strings import *
import buggalo

import streaming
import xbmcaddon
import xbmc
import os
import shutil

# addon        = xbmcaddon.Addon()
# addonid      = addon.getAddonInfo('id')
# addonversion = addon.getAddonInfo('version')

ADDON        = xbmcaddon.Addon(id = 'script.tvguidedixie.o2ri')
MASHMODE     = (ADDON.getSetting('mashmode') == 'true')
SKIN         = ADDON.getSetting('dixie.skin')
SKINSVERSION = '1'
datapath     = xbmc.translatePath(ADDON.getAddonInfo('profile'))
extras       = os.path.join(datapath, 'extras')
skinfolder   = os.path.join(datapath, extras, 'skins')
mashpath     = os.path.join(skinfolder, 'Mash Up')
skinpath     = os.path.join(skinfolder, SKIN)
mashfile     = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.movie25/Dixie/mashup.ini'))
version      = os.path.join(skinfolder, 'skinsversion.txt')

# print '*********** IS MASHMODE ON? ************'
# print addonid, addonversion
print '********* LATEST SKINS VERSION *********'
print SKINSVERSION


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

try:
    if not os.path.exists(mashpath):
        print '************* MASH MISSING *************'
        Path = extras
        import urllib, dxmnew
        try: os.makedirs(Path)
        except: pass
        Url  = 'https://dl.dropboxusercontent.com/u/5461675/skins.zip'
        LocalName = 'skins.zip'
        LocalFile = xbmc.translatePath(os.path.join(Path, LocalName))
        try: urllib.urlretrieve(Url,LocalFile)
        except:xbmc.executebuiltin("XBMC.Notification(TV Guide Dixie,Skin download failed,3000)")
        if os.path.isfile(LocalFile):
            print '********* SKINS ARE INSTALLING *********'
            extractFolder = Path
            pluginsrc = xbmc.translatePath(os.path.join(extractFolder))
            dxmnew.unzipAndMove(LocalFile,extractFolder,pluginsrc)
            try: os.remove(LocalFile)
            except: pass
except: pass

try:
    #load skin version from file
    with open (version, 'r') as f:
        local = f.readline()
        print '******** EXISTING SKINS VERSION ********'
        print local
        f.write(version)
        if not local == SKINSVERSION:
            Path = extras
            import urllib, dxmnew
            try: os.makedirs(Path)
            except: pass
            Url  = 'https://dl.dropboxusercontent.com/u/5461675/skins.zip'
            LocalName = 'skins.zip'
            LocalFile = xbmc.translatePath(os.path.join(Path, LocalName))
            try: urllib.urlretrieve(Url,LocalFile)
            except:xbmc.executebuiltin("XBMC.Notification(TV Guide Dixie,Skin download failed,3000)")
            if os.path.isfile(LocalFile):
                print '********** SKINS ARE UPDATING **********'
                extractFolder = Path
                pluginsrc = xbmc.translatePath(os.path.join(extractFolder))
                dxmnew.unzipAndMove(LocalFile,extractFolder,pluginsrc)
                try: os.remove(LocalFile)
                except: pass
        f.closed
except: pass


if MASHMODE:
    PATH  = mashpath
else:
    PATH  = skinpath


ADDON.setSetting('mashmode', 'false')


xml_file = os.path.join('script-tvguide-main.xml')
if os.path.join(SKIN, 'extras', 'skins', 'Default', '720p', xml_file):
    XML  = xml_file

print '*************** SKIN IS ****************'
print SKIN

DEBUG = False

MODE_EPG = 'EPG'
MODE_TV = 'TV'
MODE_OSD = 'OSD'

ACTION_LEFT = 1
ACTION_RIGHT = 2
ACTION_UP = 3
ACTION_DOWN = 4
ACTION_PAGE_UP = 5
ACTION_PAGE_DOWN = 6
ACTION_SELECT_ITEM = 7
ACTION_PARENT_DIR = 9
ACTION_PREVIOUS_MENU = 10
ACTION_SHOW_INFO = 11
ACTION_NEXT_ITEM = 14
ACTION_PREV_ITEM = 15

ACTION_MOUSE_WHEEL_UP = 104
ACTION_MOUSE_WHEEL_DOWN = 105
ACTION_MOUSE_MOVE = 107

KEY_NAV_BACK = 92
KEY_CONTEXT_MENU = 117
KEY_HOME = 159

CHANNELS_PER_PAGE = 8

HALF_HOUR = datetime.timedelta(minutes = 30)


try:
    #load cfg from file
    f   = open(os.path.join(PATH, 'epg.cfg'))
    cfg = f.readlines()
    f.close()
  
    for l in cfg:
        l = l.strip()
        #sanity check on text
        pts = l.split('=')
        if len(pts) == 2:
            exec(l)
except:
    pass

def debug(s):
    if DEBUG: xbmc.log(str(s), xbmc.LOGDEBUG)

class Point(object):
    def __init__(self):
        self.x = self.y = 0

    def __repr__(self):
        return 'Point(x=%d, y=%d)' % (self.x, self.y)

class EPGView(object):
    def __init__(self):
        self.top = self.left = self.right = self.bottom = self.width = self.cellHeight = 0

class ControlAndProgram(object):
    def __init__(self, control, program):
        self.control = control
        self.program = program

class TVGuide(xbmcgui.WindowXML):
    C_MAIN_DATE = 4000
    C_MAIN_TITLE = 4020
    C_MAIN_TIME = 4021
    C_MAIN_DESCRIPTION = 4022
    C_MAIN_IMAGE = 4023
    C_MAIN_LOGO = 4024
    C_MAIN_TIMEBAR = 4100
    C_MAIN_LOADING = 4200
    C_MAIN_LOADING_PROGRESS = 4201
    C_MAIN_LOADING_TIME_LEFT = 4202
    C_MAIN_LOADING_CANCEL = 4203
    C_MAIN_MOUSE_CONTROLS = 4300
    C_MAIN_MOUSE_HOME = 4301
    C_MAIN_MOUSE_LEFT = 4302
    C_MAIN_MOUSE_UP = 4303
    C_MAIN_MOUSE_DOWN = 4304
    C_MAIN_MOUSE_RIGHT = 4305
    C_MAIN_MOUSE_EXIT = 4306
    C_MAIN_BACKGROUND = 4600
    C_MAIN_EPG = 5000
    C_MAIN_EPG_VIEW_MARKER = 5001
    C_MAIN_OSD = 6000
    C_MAIN_OSD_TITLE = 6001
    C_MAIN_OSD_TIME = 6002
    C_MAIN_OSD_DESCRIPTION = 6003
    C_MAIN_OSD_CHANNEL_LOGO = 6004
    C_MAIN_OSD_CHANNEL_TITLE = 6005
    C_MAIN_BLACKOUT = 9999

    def __new__(cls):
        return super(TVGuide, cls).__new__(cls, XML, PATH)

    def __init__(self):
        super(TVGuide, self).__init__()
        self.initialized = False
        self.notification = None
        self.redrawingEPG = False
        self.timebarVisible = False
        self.isClosing = False
        self.controlAndProgramList = list()
        self.ignoreMissingControlIds = list()
        self.channelIdx = 0
        self.focusPoint = Point()
        self.epgView = EPGView()
        self.streamingService = streaming.StreamsService()
        self.player = xbmc.Player()
        self.database = None
        self.categoriesList = ADDON.getSetting('categories').split('|')
        if self.categoriesList[0] == '':
           self.categoriesList = []
        self.mode = MODE_EPG
        self.currentChannel = None

        self.osdEnabled = ADDON.getSetting('enable.osd') == 'true' and ADDON.getSetting('alternative.playback') != 'true'
        self.alternativePlayback = ADDON.getSetting('alternative.playback') == 'true'
        self.osdChannel = None
        self.osdProgram = None

        # SJP - set self.touch to True to enable Touch Screen mode
        # you can try to do this automatically (iPad/iPhone) or add a setting
        # I'll leave that bit up to you
        # self.prevCtrl is used to store the id of the last control click, so we
        # can then determine if the user has clicked on the same one
        # or a new one
        self.touch    = False
        self.prevCtrl = -1   

        #this will detect an iPad / iPhone automatically
        #ATV2 = xbmc.getCondVisibility("System.Platform.ATV2") == 1
        #IOS  = xbmc.getCondVisibility("System.Platform.IOS")  == 1
        #self.touch = IOS and not ATV2

        #you will need to add a boolean setting for this bit
        if ADDON.getSetting('enable.touch') == 'true':
            self.touch = True

        # find nearest half hour
        self.viewStartDate = datetime.datetime.today()
        self.viewStartDate -= datetime.timedelta(minutes = self.viewStartDate.minute % 30, seconds = self.viewStartDate.second)


        
    def getControl(self, controlId):
        try:
            return super(TVGuide, self).getControl(controlId)
        except:
            if controlId in self.ignoreMissingControlIds:
                return None
            if not self.isClosing:
                xbmcgui.Dialog().ok(buggalo.getRandomHeading(), strings(SKIN_ERROR_LINE1), strings(SKIN_ERROR_LINE2), strings(SKIN_ERROR_LINE3))
                self.close()
            return None

    def close(self):
        try:
    		self.timer.cancel()
    		del self.timer
    	except:
    		pass

        if not self.isClosing:
            self.isClosing = True
            if self.player.isPlaying():
                self.player.stop()
            if self.database:
                self.database.close(super(TVGuide, self).close)
            else:
                super(TVGuide, self).close()

    @buggalo.buggalo_try_except({'method' : 'TVGuide.onInit'})
    def onInit(self):
        if self.initialized:
            # onInit(..) is invoked again by XBMC after a video addon exits after being invoked by XBMC.RunPlugin(..)
            xbmc.log("[script.tvguidedixie] TVGuide.onInit(..) invoked, but we're already initialized!")
            return
        self.initialized = True
        self._hideControl(self.C_MAIN_MOUSE_CONTROLS, self.C_MAIN_OSD)
        self._showControl(self.C_MAIN_EPG, self.C_MAIN_LOADING)
        self._showControl(self.C_MAIN_BLACKOUT)
        self.setControlLabel(self.C_MAIN_LOADING_TIME_LEFT, strings(BACKGROUND_UPDATE_IN_PROGRESS))
        self.setFocusId(self.C_MAIN_LOADING_CANCEL)

        control = self.getControl(self.C_MAIN_EPG_VIEW_MARKER)
        if control:
            left, top = control.getPosition()
            self.focusPoint.x = left
            self.focusPoint.y = top
            self.epgView.left = left
            self.epgView.top = top
            self.epgView.right = left + control.getWidth()
            self.epgView.bottom = top + control.getHeight()
            self.epgView.width = control.getWidth()
            self.epgView.cellHeight = 50

        try:
            self.database = src.Database(CHANNELS_PER_PAGE)
        except src.SourceNotConfiguredException:
            self.onSourceNotConfigured()
            self.close()
            return
        self.database.initialize(self.onSourceInitialized, self.isSourceInitializationCancelled)
        self.updateTimebar()

    @buggalo.buggalo_try_except({'method' : 'TVGuide.onAction'})
    def onAction(self, action):
        debug('Mode is: %s' % self.mode)

        if self.mode == MODE_TV:
            self.onActionTVMode(action)
        elif self.mode == MODE_OSD:
            self.onActionOSDMode(action)
        elif self.mode == MODE_EPG:
            self.onActionEPGMode(action)

    def onActionTVMode(self, action):
        if action.getId() == ACTION_PAGE_UP:
            self._channelUp()

        elif action.getId() == ACTION_PAGE_DOWN:
            self._channelDown()

        elif not self.osdEnabled:
            pass # skip the rest of the actions

        elif action.getId() in [ACTION_PARENT_DIR, KEY_NAV_BACK, KEY_CONTEXT_MENU, ACTION_PREVIOUS_MENU]:
            self.viewStartDate = datetime.datetime.today()
            self.viewStartDate -= datetime.timedelta(minutes = self.viewStartDate.minute % 30, seconds = self.viewStartDate.second)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)

        elif action.getId() == ACTION_SHOW_INFO:
            self._showOsd()

    def onActionOSDMode(self, action):
        if action.getId() == ACTION_SHOW_INFO:
            self._hideOsd()
            

        elif action.getId() in [ACTION_PARENT_DIR, KEY_NAV_BACK, KEY_CONTEXT_MENU, ACTION_PREVIOUS_MENU]:
            self._hideOsd()
            self.viewStartDate = datetime.datetime.today()
            self.viewStartDate -= datetime.timedelta(minutes = self.viewStartDate.minute % 30, seconds = self.viewStartDate.second)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)

        elif action.getId() == ACTION_SELECT_ITEM:
            if self.playChannel(self.osdChannel):
                self._hideOsd()

        elif action.getId() == ACTION_PAGE_UP:
            self._channelUp()
            self._showOsd()

        elif action.getId() == ACTION_PAGE_DOWN:
            self._channelDown()
            self._showOsd()

        elif action.getId() == ACTION_UP:
            self.osdChannel = self.database.getPreviousChannel(self.osdChannel)
            self.osdProgram = self.database.getCurrentProgram(self.osdChannel)
            self._showOsd()

        elif action.getId() == ACTION_DOWN:
            self.osdChannel = self.database.getNextChannel(self.osdChannel)
            self.osdProgram = self.database.getCurrentProgram(self.osdChannel)
            self._showOsd()

        elif action.getId() == ACTION_LEFT:
            previousProgram = self.database.getPreviousProgram(self.osdProgram)
            if previousProgram:
                self.osdProgram = previousProgram
                self._showOsd()

        elif action.getId() == ACTION_RIGHT:
            nextProgram = self.database.getNextProgram(self.osdProgram)
            if nextProgram:
                self.osdProgram = nextProgram
                self._showOsd()

    def onActionEPGMode(self, action):
        if action.getId() in [ACTION_PARENT_DIR, KEY_NAV_BACK, ACTION_PREVIOUS_MENU]:
            self.close()
            return

        elif action.getId() == ACTION_MOUSE_MOVE:
            self._showControl(self.C_MAIN_MOUSE_CONTROLS)
            return

        elif action.getId() == KEY_CONTEXT_MENU:
            if self.player.isPlaying():
                self._hideEpg()

        controlInFocus = None
        currentFocus = self.focusPoint
        try:
            controlInFocus = self.getFocus()
            if controlInFocus in [elem.control for elem in self.controlAndProgramList]:
                (left, top) = controlInFocus.getPosition()
                currentFocus = Point()
                currentFocus.x = left + (controlInFocus.getWidth() / 2)
                currentFocus.y = top + (controlInFocus.getHeight() / 2)
        except Exception:
            control = self._findControlAt(self.focusPoint)
            if control is None and len(self.controlAndProgramList) > 0:
                control = self.controlAndProgramList[0].control
            if control is not None:
                self.setFocus(control)
                return

        if action.getId() == ACTION_LEFT:
            self._left(currentFocus)
        elif action.getId() == ACTION_RIGHT:
            self._right(currentFocus)
        elif action.getId() == ACTION_UP:
            self._up(currentFocus)
        elif action.getId() == ACTION_DOWN:
            self._down(currentFocus)
        elif action.getId() == ACTION_NEXT_ITEM:
            self._nextDay()
        elif action.getId() == ACTION_PREV_ITEM:
            self._previousDay()
        elif action.getId() == ACTION_PAGE_UP:
            self._moveUp(CHANNELS_PER_PAGE)
        elif action.getId() == ACTION_PAGE_DOWN:
            self._moveDown(CHANNELS_PER_PAGE)
        elif action.getId() == ACTION_MOUSE_WHEEL_UP:
            self._moveUp(scrollEvent = True)
        elif action.getId() == ACTION_MOUSE_WHEEL_DOWN:
            self._moveDown(scrollEvent = True)
        elif action.getId() == KEY_HOME:
            self.viewStartDate = datetime.datetime.today()
            self.viewStartDate -= datetime.timedelta(minutes = self.viewStartDate.minute % 30, seconds = self.viewStartDate.second)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)
        elif action.getId() in [KEY_CONTEXT_MENU] and controlInFocus is not None:
            program = self._getProgramFromControl(controlInFocus)
            if program is not None:
                self._showContextMenu(program)


    @buggalo.buggalo_try_except({'method' : 'TVGuide.onClick'})
    def onClick(self, controlId):
        if controlId in [self.C_MAIN_LOADING_CANCEL, self.C_MAIN_MOUSE_EXIT]:
            self.close()
            return

        if self.isClosing:
            return

        if controlId == self.C_MAIN_MOUSE_HOME:
            self.viewStartDate = datetime.datetime.today()
            self.viewStartDate -= datetime.timedelta(minutes = self.viewStartDate.minute % 30, seconds = self.viewStartDate.second)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)
            return
        elif controlId == self.C_MAIN_MOUSE_LEFT:
            self.viewStartDate -= datetime.timedelta(hours = 2)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)
            return
        elif controlId == self.C_MAIN_MOUSE_UP:
            self._moveUp(count = CHANNELS_PER_PAGE)
            return
        elif controlId == self.C_MAIN_MOUSE_DOWN:
            self._moveDown(count = CHANNELS_PER_PAGE)
            return
        elif controlId == self.C_MAIN_MOUSE_RIGHT:
            self.viewStartDate += datetime.timedelta(hours = 2)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)
            return

        # SJP
        # store last control in a local variable
        # store current one in member variable (self.prevCtrl)
        # then if we are in touch screen mode and it is a different control
        # just return
        prevCtrl      = self.prevCtrl
        self.prevCtrl = controlId
        if self.touch:
            if prevCtrl != self.prevCtrl:
                return

        program = self._getProgramFromControl(self.getControl(controlId))
        if program is None:
            return

        # SJP
        # we must have clicked the same program twice so show the
        # context menu
        if self.touch:
            self._showContextMenu(program)
            return

        # SJP
        # I have move this code into a new method (tryProgram) 
        # because I want to call it from 2 different places now
        self.tryProgram(program)

    # SJP
    # this used to be in the method above
    # I have also added a return if in touch screen mode
    # this is so if you select to play a non-playable stream from the menu
    # when in touch screen mode it doesn't show the menu again 
    def tryProgram(self, program):
        if self.playChannel(program.channel):
            return
        result = self.streamingService.detectStream(program.channel)        
        if not result:         
            #SJP
            if self.touch:
                return
            # could not detect stream, show context menu
            self._showContextMenu(program)
        elif type(result) == str:
            # one single stream detected, save it and start streaming
            self.database.setCustomStreamUrl(program.channel, result)
            self.playChannel(program.channel)

        else:
            # multiple matches, let user decide

            d = ChooseStreamAddonDialog(result)
            d.doModal()
            if d.stream is not None:
                self.database.setCustomStreamUrl(program.channel, d.stream)
                self.playChannel(program.channel)


    def _showContextMenu(self, program):
        self._hideControl(self.C_MAIN_MOUSE_CONTROLS)
        # SJP added self.touch parameter
        d = PopupMenu(self.database, program, not program.notificationScheduled, self.touch)
        d.doModal()
        buttonClicked = d.buttonClicked
        del d

        if buttonClicked == PopupMenu.C_POPUP_REMIND:
            if program.notificationScheduled:
                self.notification.removeNotification(program)
            else:
                self.notification.addNotification(program)

            self.onRedrawEPG(self.channelIdx, self.viewStartDate)

        elif buttonClicked == PopupMenu.C_POPUP_CHOOSE_STREAM:
            d = StreamSetupDialog(self.database, program.channel)
            d.doModal()
            del d

        elif buttonClicked == PopupMenu.C_POPUP_PLAY:
            # SJP if user clicked play and we are in touch screen mode
            # reposnd the same way as if they had clicked a program in non-touch screen mode
            # otherwise do as before, ie playChannel
            if self.touch:
                self.tryProgram(program)
            else:
                self.playChannel(program.channel)

        elif buttonClicked == PopupMenu.C_POPUP_CHANNELS:
            d = ChannelsMenu(self.database)
            d.doModal()
            del d
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)
            
        elif buttonClicked == PopupMenu.C_POPUP_CATEGORIES:
            d = CategoriesMenu(self.database, self.categoriesList)
            d.doModal()
            self.categoriesList = d.currentCategories
            del d
            ADDON.setSetting('categories', '|'.join(self.categoriesList))
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)

        elif buttonClicked == PopupMenu.C_POPUP_QUIT:
            self.close()

    def setFocusId(self, controlId):
        control = self.getControl(controlId)
        if control:
            self.setFocus(control)

    def setFocus(self, control):
        debug('setFocus %d' % control.getId())
        if control in [elem.control for elem in self.controlAndProgramList]:
            debug('Focus before %s' % self.focusPoint)
            (left, top) = control.getPosition()
            if left > self.focusPoint.x or left + control.getWidth() < self.focusPoint.x:
                self.focusPoint.x = left
            self.focusPoint.y = top + (control.getHeight() / 2)
            debug('New focus at %s' % self.focusPoint)

        super(TVGuide, self).setFocus(control)

    @buggalo.buggalo_try_except({'method' : 'TVGuide.onFocus'})
    def onFocus(self, controlId):
        try:
            controlInFocus = self.getControl(controlId)
        except Exception:
            return

        program = self._getProgramFromControl(controlInFocus)
        if program is None:
            return

        self.setControlLabel(self.C_MAIN_TITLE, '[B]%s[/B]' % program.title)
        self.setControlLabel(self.C_MAIN_TIME, '[B]%s - %s[/B]' % (self.formatTime(program.startDate), self.formatTime(program.endDate)))
        if program.description:
            description = program.description
        else:
            description = strings(NO_DESCRIPTION)
        self.setControlText(self.C_MAIN_DESCRIPTION, description)

        if program.channel.logo is not None:
            self.setControlImage(self.C_MAIN_LOGO, program.channel.logo)
        if program.imageSmall is not None:
            self.setControlImage(self.C_MAIN_IMAGE, program.imageSmall)

        if ADDON.getSetting('program.background.enabled') == 'true' and program.imageLarge is not None:
            self.setControlImage(self.C_MAIN_BACKGROUND, program.imageLarge)

        if not self.osdEnabled and self.player.isPlaying():
            self.player.stop()

    def _left(self, currentFocus):
        control = self._findControlOnLeft(currentFocus)
        if control is not None:
            self.setFocus(control)
        elif control is None:
            self.viewStartDate -= datetime.timedelta(hours = 2)
            self.focusPoint.x = self.epgView.right
            self.onRedrawEPG(self.channelIdx, self.viewStartDate, focusFunction=self._findControlOnLeft)

    def _right(self, currentFocus):
        control = self._findControlOnRight(currentFocus)
        if control is not None:
            self.setFocus(control)
        elif control is None:
            self.viewStartDate += datetime.timedelta(hours = 2)
            self.focusPoint.x = self.epgView.left
            self.onRedrawEPG(self.channelIdx, self.viewStartDate, focusFunction=self._findControlOnRight)

    def _up(self, currentFocus):
        currentFocus.x = self.focusPoint.x
        control = self._findControlAbove(currentFocus)
        if control is not None:
            self.setFocus(control)
        elif control is None:
            self.focusPoint.y = self.epgView.bottom
            self.onRedrawEPG(self.channelIdx - CHANNELS_PER_PAGE, self.viewStartDate, focusFunction=self._findControlAbove)

    def _down(self, currentFocus):
        currentFocus.x = self.focusPoint.x
        control = self._findControlBelow(currentFocus)
        if control is not None:
            self.setFocus(control)
        elif control is None:
            self.focusPoint.y = self.epgView.top
            self.onRedrawEPG(self.channelIdx + CHANNELS_PER_PAGE, self.viewStartDate, focusFunction=self._findControlBelow)

    def _nextDay(self):
        self.viewStartDate += datetime.timedelta(days = 1)
        self.onRedrawEPG(self.channelIdx, self.viewStartDate)

    def _previousDay(self):
        self.viewStartDate -= datetime.timedelta(days = 1)
        self.onRedrawEPG(self.channelIdx, self.viewStartDate)

    def _moveUp(self, count = 1, scrollEvent = False):
        if scrollEvent:
            self.onRedrawEPG(self.channelIdx - count, self.viewStartDate)
        else:
            self.focusPoint.y = self.epgView.bottom
            self.onRedrawEPG(self.channelIdx - count, self.viewStartDate, focusFunction = self._findControlAbove)

    def _moveDown(self, count = 1, scrollEvent = False):
        if scrollEvent:
            self.onRedrawEPG(self.channelIdx + count, self.viewStartDate)
        else:
            self.focusPoint.y = self.epgView.top
            self.onRedrawEPG(self.channelIdx + count, self.viewStartDate, focusFunction=self._findControlBelow)

    def _channelUp(self):
        channel = self.database.getNextChannel(self.currentChannel)
        self.playChannel(channel)

    def _channelDown(self):
        channel = self.database.getPreviousChannel(self.currentChannel)
        self.playChannel(channel)

    def playChannel(self, channel):
        self.currentChannel = channel
        wasPlaying = self.player.isPlaying()
        url = self.database.getStreamUrl(channel)
        if url:
            if not wasPlaying:
                self._hideControl(self.C_MAIN_BLACKOUT)
            path = os.path.join(ADDON.getAddonInfo('path'), 'player.py')
            xbmc.executebuiltin('XBMC.RunScript(%s,%s,%d)' % (path, url, self.osdEnabled))

            if not wasPlaying:
                self._hideEpg()

        threading.Timer(5, self.waitForPlayBackStopped).start()
        self.osdProgram = self.database.getCurrentProgram(self.currentChannel)

        return url is not None

    def waitForPlayBackStopped(self):
        for retry in range(0, 100):
            time.sleep(0.1)
            if self.player.isPlaying():
                break
                
        self._showControl(self.C_MAIN_BLACKOUT)
        while self.player.isPlaying() and not xbmc.abortRequested and not self.isClosing:
            time.sleep(0.5)

        self.onPlayBackStopped()

    def _showOsd(self):
        if not self.osdEnabled:
            return

        if self.mode != MODE_OSD:
            self.osdChannel = self.currentChannel

        if self.osdProgram is not None:
            self.setControlLabel(self.C_MAIN_OSD_TITLE, '[B]%s[/B]' % self.osdProgram.title)
            self.setControlLabel(self.C_MAIN_OSD_TIME, '[B]%s - %s[/B]' % (self.formatTime(self.osdProgram.startDate), self.formatTime(self.osdProgram.endDate)))
            self.setControlText(self.C_MAIN_OSD_DESCRIPTION, self.osdProgram.description)
            self.setControlLabel(self.C_MAIN_OSD_CHANNEL_TITLE, self.osdChannel.title)
            if self.osdProgram.channel.logo is not None:
                self.setControlImage(self.C_MAIN_OSD_CHANNEL_LOGO, self.osdProgram.channel.logo)
            else:
                self.setControlImage(self.C_MAIN_OSD_CHANNEL_LOGO, '')

        self.mode = MODE_OSD
        self._showControl(self.C_MAIN_OSD)

    def _hideOsd(self):
        self.mode = MODE_TV
        self._hideControl(self.C_MAIN_OSD)

    def _hideEpg(self):
        self._hideControl(self.C_MAIN_EPG)
        self.mode = MODE_TV
        self._clearEpg()

    def onRedrawEPG(self, channelStart, startTime, focusFunction = None):
        if self.redrawingEPG or (self.database is not None and self.database.updateInProgress) or self.isClosing:
            debug('onRedrawEPG - already redrawing')
            return # ignore redraw request while redrawing
        debug('onRedrawEPG')

        self.redrawingEPG = True
        self.mode = MODE_EPG
        self._showControl(self.C_MAIN_EPG)
        self.updateTimebar(scheduleTimer = False)

        # show Loading screen
        self.setControlLabel(self.C_MAIN_LOADING_TIME_LEFT, strings(CALCULATING_REMAINING_TIME))
        self._showControl(self.C_MAIN_LOADING)
        self.setFocusId(self.C_MAIN_LOADING_CANCEL)
        self.hideTimebar()
        
        # remove existing controls
        self._clearEpg()

        try:
            self.channelIdx, channels, programs = self.database.getEPGView(channelStart, startTime, self.onSourceProgressUpdate, clearExistingProgramList = False, categories = self.categoriesList, nmrChannels = CHANNELS_PER_PAGE)
        except src.SourceException:
            self.onEPGLoadError()
            return

        channelsWithoutPrograms = list(channels)

        # date and time row
        self.setControlLabel(self.C_MAIN_DATE, self.formatDate(self.viewStartDate))
        for col in range(1, 5):
            self.setControlLabel(4000 + col, self.formatTime(startTime))
            startTime += HALF_HOUR

        if programs is None:
            self.onEPGLoadError()
            return

        # set channel logo or text
        for idx in range(0, CHANNELS_PER_PAGE):
            if idx >= len(channels):
                self.setControlImage(4110 + idx, ' ')
                self.setControlLabel(4010 + idx, ' ')
            else:
                channel = channels[idx]
                self.setControlLabel(4010 + idx, channel.title)
                if channel.logo is not None:
                    self.setControlImage(4110 + idx, channel.logo)
                else:
                    self.setControlImage(4110 + idx, ' ')

        for program in programs:
            idx = channels.index(program.channel)
            if program.channel in channelsWithoutPrograms:
                channelsWithoutPrograms.remove(program.channel)

            startDelta = program.startDate - self.viewStartDate
            stopDelta = program.endDate - self.viewStartDate

            cellStart = self._secondsToXposition(startDelta.seconds)
            if startDelta.days < 0:
                cellStart = self.epgView.left
            cellWidth = self._secondsToXposition(stopDelta.seconds) - cellStart
            if cellStart + cellWidth > self.epgView.right:
                cellWidth = self.epgView.right - cellStart

            if cellWidth > 1:
                if program.notificationScheduled:
                    noFocusTexture = 'tvguide-program-red.png'
                    focusTexture = 'tvguide-program-red-focus.png'
                else:
                    noFocusTexture = 'tvguide-program-grey.png'
                    focusTexture = 'tvguide-program-grey-focus.png'

                if cellWidth < 25:
                    title = '' # Text will overflow outside the button if it is too narrow
                else:
                    title = program.title

                control = xbmcgui.ControlButton(
                    cellStart,
                    self.epgView.top + self.epgView.cellHeight * idx,
                    cellWidth - 2,
                    self.epgView.cellHeight - 2,
                    title,
                    noFocusTexture = noFocusTexture,
                    focusTexture = focusTexture
                )

                self.controlAndProgramList.append(ControlAndProgram(control, program))

        for channel in channelsWithoutPrograms:
            idx = channels.index(channel)

            control = xbmcgui.ControlButton(
                self.epgView.left,
                self.epgView.top + self.epgView.cellHeight * idx,
                (self.epgView.right - self.epgView.left) - 2,
                self.epgView.cellHeight - 2,
                strings(NO_PROGRAM_AVAILABLE),
                noFocusTexture='tvguide-program-grey.png',
                focusTexture='tvguide-program-grey-focus.png'
            )

            now  = datetime.datetime.today()
            then = now + datetime.timedelta(minutes = 24*60)
            program = src.Program(channel, strings(NO_PROGRAM_AVAILABLE), now, then, "", "")
            self.controlAndProgramList.append(ControlAndProgram(control, program))

        # add program controls
        if focusFunction is None:
            focusFunction = self._findControlAt
        focusControl = focusFunction(self.focusPoint)
        controls = [elem.control for elem in self.controlAndProgramList]
        self.addControls(controls)
        if focusControl is not None:
            debug('onRedrawEPG - setFocus %d' % focusControl.getId())
            self.setFocus(focusControl)

        self.ignoreMissingControlIds.extend([elem.control.getId() for elem in self.controlAndProgramList])

        if focusControl is None and len(self.controlAndProgramList) > 0:
            self.setFocus(self.controlAndProgramList[0].control)

        self._hideControl(self.C_MAIN_LOADING)
        self.showTimebar()
        self.redrawingEPG = False
                    
    def _clearEpg(self):
        controls = [elem.control for elem in self.controlAndProgramList]
        try:
            self.removeControls(controls)
        except RuntimeError:
            for elem in self.controlAndProgramList:
                try:
                    self.removeControl(elem.control)
                except RuntimeError:
                    pass # happens if we try to remove a control that doesn't exist
        del self.controlAndProgramList[:]

    def onEPGLoadError(self):
        self.redrawingEPG = False
        self._hideControl(self.C_MAIN_LOADING)
        xbmcgui.Dialog().ok(strings(LOAD_ERROR_TITLE), strings(LOAD_ERROR_LINE1), strings(LOAD_ERROR_LINE2))
        self.close()


    def onSourceNotConfigured(self):
        self.redrawingEPG = False
        self._hideControl(self.C_MAIN_LOADING)
        xbmcgui.Dialog().ok(strings(LOAD_ERROR_TITLE), strings(LOAD_ERROR_LINE1), strings(CONFIGURATION_ERROR_LINE2))
        self.close()

    def isSourceInitializationCancelled(self):
        return xbmc.abortRequested or self.isClosing

    def onSourceInitialized(self, success):
        if success:
            self.notification = Notification(self.database, ADDON.getAddonInfo('path'))
            self.onRedrawEPG(0, self.viewStartDate)

    def onSourceProgressUpdate(self, percentageComplete):
        control = self.getControl(self.C_MAIN_LOADING_PROGRESS)
        if percentageComplete < 1:
            if control:
                control.setPercent(1)
            self.progressStartTime = datetime.datetime.now()
            self.progressPreviousPercentage = percentageComplete
        elif percentageComplete != self.progressPreviousPercentage:
            if control:
                control.setPercent(percentageComplete)
            self.progressPreviousPercentage = percentageComplete
            delta = datetime.datetime.now() - self.progressStartTime

            if percentageComplete < 20:
                self.setControlLabel(self.C_MAIN_LOADING_TIME_LEFT, strings(CALCULATING_REMAINING_TIME))
            else:
                secondsLeft = int(delta.seconds) / float(percentageComplete) * (100.0 - percentageComplete)
                if secondsLeft > 30:
                    secondsLeft -= secondsLeft % 10
                self.setControlLabel(self.C_MAIN_LOADING_TIME_LEFT, strings(TIME_LEFT) % secondsLeft)

        return not xbmc.abortRequested and not self.isClosing

    def onPlayBackStopped(self):
        if not self.player.isPlaying() and not self.isClosing:
            self._hideControl(self.C_MAIN_OSD)
            self.viewStartDate = datetime.datetime.today()
            self.viewStartDate -= datetime.timedelta(minutes = self.viewStartDate.minute % 30, seconds = self.viewStartDate.second)
            self.onRedrawEPG(self.channelIdx, self.viewStartDate)
            return

    def _secondsToXposition(self, seconds):
        return self.epgView.left + (seconds * self.epgView.width / 7200)

    def _findControlOnRight(self, point):
        distanceToNearest = 10000
        nearestControl = None

        for elem in self.controlAndProgramList:
            control = elem.control
            (left, top) = control.getPosition()
            x = left + (control.getWidth() / 2)
            y = top + (control.getHeight() / 2)

            if point.x < x and point.y == y:
                distance = abs(point.x - x)
                if distance < distanceToNearest:
                    distanceToNearest = distance
                    nearestControl = control

        return nearestControl


    def _findControlOnLeft(self, point):
        distanceToNearest = 10000
        nearestControl = None

        for elem in self.controlAndProgramList:
            control = elem.control
            (left, top) = control.getPosition()
            x = left + (control.getWidth() / 2)
            y = top + (control.getHeight() / 2)

            if point.x > x and point.y == y:
                distance = abs(point.x - x)
                if distance < distanceToNearest:
                    distanceToNearest = distance
                    nearestControl = control

        return nearestControl

    def _findControlBelow(self, point):
        nearestControl = None

        for elem in self.controlAndProgramList:
            control = elem.control
            (leftEdge, top) = control.getPosition()
            y = top + (control.getHeight() / 2)

            if point.y < y:
                rightEdge = leftEdge + control.getWidth()
                if(leftEdge <= point.x < rightEdge
                   and (nearestControl is None or nearestControl.getPosition()[1] > top)):
                    nearestControl = control

        return nearestControl

    def _findControlAbove(self, point):
        nearestControl = None
        for elem in self.controlAndProgramList:
            control = elem.control
            (leftEdge, top) = control.getPosition()
            y = top + (control.getHeight() / 2)

            if point.y > y:
                rightEdge = leftEdge + control.getWidth()
                if(leftEdge <= point.x < rightEdge
                   and (nearestControl is None or nearestControl.getPosition()[1] < top)):
                    nearestControl = control

        return nearestControl

    def _findControlAt(self, point):
        for elem in self.controlAndProgramList:
            control = elem.control
            (left, top) = control.getPosition()
            bottom = top + control.getHeight()
            right = left + control.getWidth()

            if left <= point.x <= right and  top <= point.y <= bottom:
                return control

        return None


    def _getProgramFromControl(self, control):
        for elem in self.controlAndProgramList:
            if elem.control == control:
                return elem.program
        return None

    def _hideControl(self, *controlIds):
        """
        Visibility is inverted in skin
        """
        for controlId in controlIds:
            control = self.getControl(controlId)
            if control:
                control.setVisible(True)

    def _showControl(self, *controlIds):
        """
        Visibility is inverted in skin
        """
        for controlId in controlIds:
            control = self.getControl(controlId)
            if control:
                control.setVisible(False)

    def formatTime(self, timestamp):
        format = xbmc.getRegion('time').replace(':%S', '').replace('%H%H', '%H')
        return timestamp.strftime(format)

    def formatDate(self, timestamp):
        format = xbmc.getRegion('dateshort')
        return timestamp.strftime(format)

    def setControlImage(self, controlId, image):
        control = self.getControl(controlId)
        if control:
            control.setImage(image.encode('utf-8'))

    def setControlLabel(self, controlId, label):
        control = self.getControl(controlId)
        if control and label:
            control.setLabel(label)

    def setControlText(self, controlId, text):
        control = self.getControl(controlId)
        if control:
            control.setText(text)

    def hideTimebar(self):
        try:
            self.timebarVisible = False
            self.getControl(self.C_MAIN_TIMEBAR).setVisible(self.timebarVisible)
        except:
            pass

    def showTimebar(self):
        try:
            self.timebarVisible = True
            self.getControl(self.C_MAIN_TIMEBAR).setVisible(self.timebarVisible)
        except:
            pass
            

    def updateTimebar(self, scheduleTimer = True):
        try:
            # move timebar to current time
            timeDelta = datetime.datetime.today() - self.viewStartDate
            control = self.getControl(self.C_MAIN_TIMEBAR)
            if control:
                (x, y) = control.getPosition()
                try:
                    # Sometimes raises:
                    # exceptions.RuntimeError: Unknown exception thrown from the call "setVisible"
                    control.setVisible(timeDelta.days == 0 and self.timebarVisible)
                except:
                    pass
                control.setPosition(self._secondsToXposition(timeDelta.seconds), y)

            if scheduleTimer and not xbmc.abortRequested and not self.isClosing:
                threading.Timer(1, self.updateTimebar).start()
        except Exception:
            buggalo.onExceptionRaised()


class PopupMenu(xbmcgui.WindowXMLDialog):
    C_POPUP_PLAY = 4000
    C_POPUP_CHOOSE_STREAM = 4001
    C_POPUP_REMIND = 4002
    C_POPUP_CHANNELS = 4003
    C_POPUP_QUIT = 4004
    C_POPUP_CHANNEL_LOGO = 4100
    C_POPUP_CHANNEL_TITLE = 4101
    C_POPUP_PROGRAM_TITLE = 4102
    C_POPUP_CATEGORIES = 4005
    C_POPUP_HOME = 4006
    


    #SJP added touch parameter
    def __new__(cls, database, program, showRemind, touch):
        xml_file = os.path.join('script-tvguide-menu.xml')
        if os.path.join(SKIN, 'extras', 'skins', 'Default', '720p', xml_file):
            XML = xml_file
            
        return super(PopupMenu, cls).__new__(cls, XML, PATH)

    #SJP added touch parameter
    def __init__(self, database, program, showRemind, touch):
        """

        @type database: source.Database
        @param program:
        @type program: source.Program
        @param showRemind:
        """
        super(PopupMenu, self).__init__()
        self.database = database
        self.program = program
        self.showRemind = showRemind
        self.buttonClicked = None
        #SJP
        self.touch = touch

    @buggalo.buggalo_try_except({'method' : 'PopupMenu.onInit'})
    def onInit(self):
        playControl = self.getControl(self.C_POPUP_PLAY)
        remindControl = self.getControl(self.C_POPUP_REMIND)
        channelLogoControl = self.getControl(self.C_POPUP_CHANNEL_LOGO)
        channelTitleControl = self.getControl(self.C_POPUP_CHANNEL_TITLE)
        programTitleControl = self.getControl(self.C_POPUP_PROGRAM_TITLE)

        playControl.setLabel(strings(WATCH_CHANNEL, self.program.channel.title))
        if not self.program.channel.isPlayable():
            playControl.setEnabled(False)
            self.setFocusId(self.C_POPUP_CHOOSE_STREAM)
        # SJP - if in touch screen mode always enable Play button and
        # set focus to it
        if self.touch or self.program.title == strings(NO_PROGRAM_AVAILABLE):
            playControl.setEnabled(True)
            self.setFocusId(self.C_POPUP_PLAY)        
        if self.database.getCustomStreamUrl(self.program.channel):
            chooseStrmControl = self.getControl(self.C_POPUP_CHOOSE_STREAM)
            chooseStrmControl.setLabel(strings(REMOVE_STRM_FILE))

        if self.program.channel.logo is not None:
            channelLogoControl.setImage(self.program.channel.logo)
            channelTitleControl.setVisible(False)
        else:
            channelTitleControl.setLabel(self.program.channel.title)
            channelLogoControl.setVisible(False)

        programTitleControl.setLabel(self.program.title)

        if self.showRemind:
            remindControl.setLabel(strings(REMIND_PROGRAM))
        else:
            remindControl.setLabel(strings(DONT_REMIND_PROGRAM))

    @buggalo.buggalo_try_except({'method' : 'PopupMenu.onAction'})
    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_NAV_BACK, KEY_CONTEXT_MENU]:
            self.close()
            return

    @buggalo.buggalo_try_except({'method' : 'PopupMenu.onClick'})
    def onClick(self, controlId):
        if controlId == self.C_POPUP_CHOOSE_STREAM and self.database.getCustomStreamUrl(self.program.channel):
            self.database.deleteCustomStreamUrl(self.program.channel)
            chooseStrmControl = self.getControl(self.C_POPUP_CHOOSE_STREAM)
            chooseStrmControl.setLabel(strings(CHOOSE_STRM_FILE))

            if not self.program.channel.isPlayable():
                playControl = self.getControl(self.C_POPUP_PLAY)
                playControl.setEnabled(False)

        else:
            self.buttonClicked = controlId
            self.close()

    def onFocus(self, controlId):
        pass

class ChannelsMenu(xbmcgui.WindowXMLDialog):
    C_CHANNELS_LIST = 6000
    C_CHANNELS_SELECTION_VISIBLE = 6001
    C_CHANNELS_SELECTION = 6002
    C_CHANNELS_SAVE = 6003
    C_CHANNELS_CANCEL = 6004
    


    def __new__(cls, database):
        xml_file = os.path.join('script-tvguide-channels.xml')
        if os.path.join(SKIN, 'extras', 'skins', 'Default', '720p', xml_file):
            XML = xml_file
        
        return super(ChannelsMenu, cls).__new__(cls, XML, PATH)

    def __init__(self, database):
        """

        @type database: source.Database
        """
        super(ChannelsMenu, self).__init__()
        self.database = database
        self.channelList = database.getChannelList(onlyVisible = False)
        self.swapInProgress = False

    @buggalo.buggalo_try_except({'method' : 'ChannelsMenu.onInit'})
    def onInit(self):
        self.updateChannelList()
        self.setFocusId(self.C_CHANNELS_LIST)

    @buggalo.buggalo_try_except({'method' : 'ChannelsMenu.onAction'})
    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_NAV_BACK, KEY_CONTEXT_MENU]:
            self.close()
            return

        if self.getFocusId() == self.C_CHANNELS_LIST and action.getId() == ACTION_LEFT:
            listControl = self.getControl(self.C_CHANNELS_LIST)
            idx = listControl.getSelectedPosition()
            buttonControl = self.getControl(self.C_CHANNELS_SELECTION)
            buttonControl.setLabel('[B]%s[/B]' % self.channelList[idx].title)

            self.getControl(self.C_CHANNELS_SELECTION_VISIBLE).setVisible(False)
            self.setFocusId(self.C_CHANNELS_SELECTION)

        elif self.getFocusId() == self.C_CHANNELS_SELECTION and action.getId() in [ACTION_RIGHT, ACTION_SELECT_ITEM]:
            self.getControl(self.C_CHANNELS_SELECTION_VISIBLE).setVisible(True)
            xbmc.sleep(350)
            self.setFocusId(self.C_CHANNELS_LIST)

        elif self.getFocusId() == self.C_CHANNELS_SELECTION and action.getId() == ACTION_UP:
            listControl = self.getControl(self.C_CHANNELS_LIST)
            idx = listControl.getSelectedPosition()
            if idx > 0:
                self.swapChannels(idx, idx - 1)

        elif self.getFocusId() == self.C_CHANNELS_SELECTION and action.getId() == ACTION_DOWN:
            listControl = self.getControl(self.C_CHANNELS_LIST)
            idx = listControl.getSelectedPosition()
            if idx < listControl.size() - 1:
                self.swapChannels(idx, idx + 1)

    @buggalo.buggalo_try_except({'method' : 'ChannelsMenu.onClick'})
    def onClick(self, controlId):
        if controlId == self.C_CHANNELS_LIST:
            listControl = self.getControl(self.C_CHANNELS_LIST)
            item = listControl.getSelectedItem()
            channel = self.channelList[int(item.getProperty('idx'))]
            channel.visible = not channel.visible

            if channel.visible:
                iconImage = 'tvguide-channel-visible.png'
            else:
                iconImage = 'tvguide-channel-hidden.png'
            item.setIconImage(iconImage)

        elif controlId == self.C_CHANNELS_SAVE:
            self.database.saveChannelList(self.close, self.channelList)

        elif controlId == self.C_CHANNELS_CANCEL:
            self.close()


    def onFocus(self, controlId):
        pass

    def updateChannelList(self):
        listControl = self.getControl(self.C_CHANNELS_LIST)
        listControl.reset()
        for idx, channel in enumerate(self.channelList):
            if channel.visible:
                iconImage = 'tvguide-channel-visible.png'
            else:
                iconImage = 'tvguide-channel-hidden.png'

            item = xbmcgui.ListItem('%3d. %s' % (idx+1, channel.title), iconImage = iconImage)
            item.setProperty('idx', str(idx))
            listControl.addItem(item)

    def updateListItem(self, idx, item):
        channel = self.channelList[idx]
        item.setLabel('%3d. %s' % (idx+1, channel.title))

        if channel.visible:
            iconImage = 'tvguide-channel-visible.png'
        else:
            iconImage = 'tvguide-channel-hidden.png'
        item.setIconImage(iconImage)
        item.setProperty('idx', str(idx))

    def swapChannels(self, fromIdx, toIdx):
        if self.swapInProgress:
            return
        self.swapInProgress = True

        c = self.channelList[fromIdx]
        self.channelList[fromIdx] = self.channelList[toIdx]
        self.channelList[toIdx] = c

        # recalculate weight
        for idx, channel in enumerate(self.channelList):
            channel.weight = idx

        listControl = self.getControl(self.C_CHANNELS_LIST)
        self.updateListItem(fromIdx, listControl.getListItem(fromIdx))
        self.updateListItem(toIdx, listControl.getListItem(toIdx))

        listControl.selectItem(toIdx)
        xbmc.sleep(50)
        self.swapInProgress = False



class StreamSetupDialog(xbmcgui.WindowXMLDialog):
    C_STREAM_STRM_TAB = 101
    C_STREAM_FAVOURITES_TAB = 102
    C_STREAM_ADDONS_TAB = 103
    C_STREAM_MASHUP_TAB = 104
    C_STREAM_STRM_BROWSE = 1001
    C_STREAM_STRM_FILE_LABEL = 1005
    C_STREAM_STRM_PREVIEW = 1002
    C_STREAM_STRM_OK = 1003
    C_STREAM_STRM_CANCEL = 1004    
    C_STREAM_FAVOURITES = 2001
    C_STREAM_FAVOURITES_PREVIEW = 2002
    C_STREAM_FAVOURITES_OK = 2003
    C_STREAM_FAVOURITES_CANCEL = 2004
    C_STREAM_ADDONS = 3001
    C_STREAM_ADDONS_STREAMS = 3002
    C_STREAM_ADDONS_NAME = 3003
    C_STREAM_ADDONS_DESCRIPTION = 3004
    C_STREAM_ADDONS_PREVIEW = 3005
    C_STREAM_ADDONS_OK = 3006
    C_STREAM_ADDONS_CANCEL = 3007

    C_STREAM_MASHUP = 4001
    C_STREAM_MASHUP_STREAMS = 4002
    C_STREAM_MASHUP_NAME = 4003
    C_STREAM_MASHUP_DESCRIPTION = 4004
    C_STREAM_MASHUP_PREVIEW = 4005
    C_STREAM_MASHUP_OK = 4006
    C_STREAM_MASHUP_CANCEL = 4007

    C_STREAM_VISIBILITY_MARKER = 100

    VISIBLE_STRM = 'strm'
    VISIBLE_FAVOURITES = 'favourites'
    VISIBLE_ADDONS = 'addons'
    VISIBLE_MASHUP= 'mashup'

    def __new__(cls, database, channel):
        xml_file = os.path.join('script-tvguide-streamsetup.xml')
        
        if os.path.join(SKIN, 'extras', 'skins', 'Default', '720p', xml_file):
            XML = xml_file
            
        return super(StreamSetupDialog, cls).__new__(cls, XML, PATH)

    def __init__(self, database, channel):
        """
        @type database: source.Database
        @type channel:source.Channel
        """
        super(StreamSetupDialog, self).__init__()
        self.database = database
        self.channel = channel
        self.player = xbmc.Player()
        self.previousAddonId = None
        self.previousProvider = None
        self.strmFile = None
        self.streamingService = streaming.StreamsService()

    def close(self):
        if self.player.isPlaying():
            self.player.stop()
        super(StreamSetupDialog, self).close()

    @buggalo.buggalo_try_except({'method' : 'StreamSetupDialog.onInit'})
    def onInit(self):
        self.getControl(self.C_STREAM_VISIBILITY_MARKER).setLabel(self.VISIBLE_STRM)
        if not os.path.exists(mashfile):
            self.getControl(self.C_STREAM_MASHUP_TAB).setVisible(False)

        favourites = self.streamingService.loadFavourites()
        items = list()
        for label, value in favourites:
            item = xbmcgui.ListItem(label)
            item.setProperty('stream', value)
            items.append(item)

        listControl = self.getControl(StreamSetupDialog.C_STREAM_FAVOURITES)
        listControl.addItems(items)

        items = list()
        for id in self.streamingService.getAddons():
            try:
                addon = xbmcaddon.Addon(id) # raises Exception if addon is not installed
                item = xbmcgui.ListItem(addon.getAddonInfo('name'), iconImage=addon.getAddonInfo('icon'))
                item.setProperty('addon_id', id)
                items.append(item)
            except Exception:
                pass
        listControl = self.getControl(StreamSetupDialog.C_STREAM_ADDONS)
        listControl.addItems(items)
        self.updateAddonInfo()

        items  = list()
        for provider in self.streamingService.getMashup():
            try:
                item = xbmcgui.ListItem(provider, iconImage=self.streamingService.getMashupIcon(provider))
                item.setProperty('provider', provider)
                items.append(item)
            except:
                pass
        listControl = self.getControl(StreamSetupDialog.C_STREAM_MASHUP)
        listControl.addItems(items)
        self.updateMashupInfo()
    

    @buggalo.buggalo_try_except({'method' : 'StreamSetupDialog.onAction'})
    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_NAV_BACK, KEY_CONTEXT_MENU]:
            self.close()
            return

        elif self.getFocusId() == self.C_STREAM_ADDONS:
            self.updateAddonInfo()

        elif self.getFocusId() == self.C_STREAM_MASHUP:
            self.updateMashupInfo()



    @buggalo.buggalo_try_except({'method' : 'StreamSetupDialog.onClick'})
    def onClick(self, controlId):
        if controlId == self.C_STREAM_STRM_BROWSE:
            stream = xbmcgui.Dialog().browse(1, ADDON.getLocalizedString(30304), 'video', '.strm')
            if stream:
                self.database.setCustomStreamUrl(self.channel, stream)
                self.getControl(self.C_STREAM_STRM_FILE_LABEL).setText(stream)
                self.strmFile = stream

        elif controlId == self.C_STREAM_ADDONS_OK:
            listControl = self.getControl(self.C_STREAM_ADDONS_STREAMS)
            item = listControl.getSelectedItem()
            if item:
                stream = item.getProperty('stream')
                self.database.setCustomStreamUrl(self.channel, stream)
            self.close()

        elif controlId == self.C_STREAM_FAVOURITES_OK:
            listControl = self.getControl(self.C_STREAM_FAVOURITES)
            item = listControl.getSelectedItem()
            if item:
                stream = item.getProperty('stream')
                self.database.setCustomStreamUrl(self.channel, stream)
            self.close()
            
        elif controlId == self.C_STREAM_MASHUP_OK:
            listControl = self.getControl(self.C_STREAM_MASHUP_STREAMS)
            item = listControl.getSelectedItem()
            if item:
                stream = item.getProperty('stream')
                self.database.setCustomStreamUrl(self.channel, stream)
            self.close()

        elif controlId == self.C_STREAM_STRM_OK:
            self.database.setCustomStreamUrl(self.channel, self.strmFile)
            self.close()

        elif controlId in [self.C_STREAM_ADDONS_CANCEL, self.C_STREAM_FAVOURITES_CANCEL, self.C_STREAM_STRM_CANCEL, self.C_STREAM_MASHUP_CANCEL]:
            self.close()

        elif controlId in [self.C_STREAM_ADDONS_PREVIEW, self.C_STREAM_FAVOURITES_PREVIEW, self.C_STREAM_STRM_PREVIEW, self.C_STREAM_MASHUP_PREVIEW]:
            if self.player.isPlaying():
                self.player.stop()
                self.getControl(self.C_STREAM_ADDONS_PREVIEW).setLabel(strings(PREVIEW_STREAM))
                self.getControl(self.C_STREAM_FAVOURITES_PREVIEW).setLabel(strings(PREVIEW_STREAM))
                self.getControl(self.C_STREAM_STRM_PREVIEW).setLabel(strings(PREVIEW_STREAM))
                self.getControl(self.C_STREAM_MASHUP_PREVIEW).setLabel(strings(PREVIEW_STREAM))
                return

            stream = None
            windowed = None
            visible = self.getControl(self.C_STREAM_VISIBILITY_MARKER).getLabel()
            if visible == self.VISIBLE_ADDONS:
                listControl = self.getControl(self.C_STREAM_ADDONS_STREAMS)
                item = listControl.getSelectedItem()
                if item:
                    stream = item.getProperty('stream')
            elif visible == self.VISIBLE_FAVOURITES:
                listControl = self.getControl(self.C_STREAM_FAVOURITES)
                item = listControl.getSelectedItem()
                if item:
                    stream = item.getProperty('stream')
            elif visible == self.VISIBLE_MASHUP:
                listControl = self.getControl(self.C_STREAM_MASHUP_STREAMS)
                item = listControl.getSelectedItem()
                if item:
                    stream = item.getProperty('stream')
            elif visible == self.VISIBLE_STRM:
                stream = self.strmFile

            if stream is not None:
                # self.player.play(item = stream, windowed = True)
                path = os.path.join(ADDON.getAddonInfo('path'), 'player.py')
                xbmc.executebuiltin('XBMC.RunScript(%s,%s,%d)' % (path, stream, 1))
                # xbmc.executebuiltin('XBMC.RunPlugin(%s)' % stream)
                retries = 10
                while retries > 0 and not self.player.isPlaying():
                   retries -= 1
                   xbmc.sleep(1000)
                if self.player.isPlaying():
                    self.getControl(self.C_STREAM_MASHUP_PREVIEW).setLabel(strings(STOP_PREVIEW))
                    self.getControl(self.C_STREAM_ADDONS_PREVIEW).setLabel(strings(STOP_PREVIEW))
                    self.getControl(self.C_STREAM_FAVOURITES_PREVIEW).setLabel(strings(STOP_PREVIEW))
                    self.getControl(self.C_STREAM_STRM_PREVIEW).setLabel(strings(STOP_PREVIEW))

    @buggalo.buggalo_try_except({'method' : 'StreamSetupDialog.onFocus'})
    def onFocus(self, controlId):
        if controlId == self.C_STREAM_STRM_TAB:
            self.getControl(self.C_STREAM_VISIBILITY_MARKER).setLabel(self.VISIBLE_STRM)
        elif controlId == self.C_STREAM_FAVOURITES_TAB:
            self.getControl(self.C_STREAM_VISIBILITY_MARKER).setLabel(self.VISIBLE_FAVOURITES)
        elif controlId == self.C_STREAM_ADDONS_TAB:
            self.getControl(self.C_STREAM_VISIBILITY_MARKER).setLabel(self.VISIBLE_ADDONS)
        elif controlId == self.C_STREAM_MASHUP_TAB:
            self.getControl(self.C_STREAM_VISIBILITY_MARKER).setLabel(self.VISIBLE_MASHUP)

    def updateAddonInfo(self):
        listControl = self.getControl(self.C_STREAM_ADDONS)
        item = listControl.getSelectedItem()
        if item is None:
            return
        
        if item.getProperty('addon_id') == self.previousAddonId:
            return

        self.previousAddonId = item.getProperty('addon_id')
        addon = xbmcaddon.Addon(id = item.getProperty('addon_id'))
        self.getControl(self.C_STREAM_ADDONS_NAME).setLabel('[B]%s[/B]' % addon.getAddonInfo('name'))
        self.getControl(self.C_STREAM_ADDONS_DESCRIPTION).setText(addon.getAddonInfo('description'))

        streams = self.streamingService.getAddonStreams(item.getProperty('addon_id'))
        items = list()
        for (label, stream) in streams:
            item = xbmcgui.ListItem(label)
            item.setProperty('stream', stream)
            items.append(item)
        listControl = self.getControl(StreamSetupDialog.C_STREAM_ADDONS_STREAMS)
        listControl.reset()
        listControl.addItems(items)

    def updateMashupInfo(self):
        pass
        listControl = self.getControl(self.C_STREAM_MASHUP)
        item = listControl.getSelectedItem()
        if item is None:
            return

        provider = item.getProperty('provider')
        if provider == self.previousProvider:
            return

        self.previousProvider = provider
        self.getControl(self.C_STREAM_MASHUP_NAME).setLabel('[B]%s[/B]' % provider)
        self.getControl(self.C_STREAM_MASHUP_DESCRIPTION).setText('')

        streams = self.streamingService.getMashupStreams(provider)
        items = list()
        for (label, stream) in streams:
            if label.upper() != 'ICON':
                item = xbmcgui.ListItem(label)
                item.setProperty('stream', stream)
                items.append(item)
        listControl = self.getControl(StreamSetupDialog.C_STREAM_MASHUP_STREAMS)
        listControl.reset()
        listControl.addItems(items)

class ChooseStreamAddonDialog(xbmcgui.WindowXMLDialog):
    C_SELECTION_LIST = 1000

    def __new__(cls, addons):
        xml_file = os.path.join('script-tvguide-streamaddon.xml')
        if os.path.join(SKIN, skinfolder, 'Default', '720p', xml_file):
            XML = xml_file
            
        return super(ChooseStreamAddonDialog, cls).__new__(cls, XML, PATH)

    def __init__(self, addons):
        super(ChooseStreamAddonDialog, self).__init__()
        self.addons = addons
        self.stream = None

    @buggalo.buggalo_try_except({'method' : 'ChooseStreamAddonDialog.onInit'})
    def onInit(self):
       items = list()
       for id, label, url in self.addons:
           try:
               addon = xbmcaddon.Addon(id)
               item = xbmcgui.ListItem(label, addon.getAddonInfo('name'), addon.getAddonInfo('icon'))
               item.setProperty('stream', url)
               items.append(item)
           except:
               item = xbmcgui.ListItem(label, '', id)
               item.setProperty('stream', url)
               items.append(item)

       listControl = self.getControl(ChooseStreamAddonDialog.C_SELECTION_LIST)
       listControl.addItems(items)

       self.setFocus(listControl)

    @buggalo.buggalo_try_except({'method' : 'ChooseStreamAddonDialog.onAction'})
    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_NAV_BACK]:
            self.close()

    @buggalo.buggalo_try_except({'method' : 'ChooseStreamAddonDialog.onClick'})
    def onClick(self, controlId):
        if controlId == ChooseStreamAddonDialog.C_SELECTION_LIST:
            listControl = self.getControl(ChooseStreamAddonDialog.C_SELECTION_LIST)
            self.stream = listControl.getSelectedItem().getProperty('stream')
            self.close()

    @buggalo.buggalo_try_except({'method' : 'ChooseStreamAddonDialog.onFocus'})
    def onFocus(self, controlId):
        pass


class CategoriesMenu(xbmcgui.WindowXMLDialog):
    C_CATEGORIES_LIST = 7000
    C_CATEGORIES_SELECTION = 7001
    C_CATEGORIES_SAVE = 7002
    C_CATEGORIES_CANCEL = 7003

    def __new__(cls, database, categoriesList):
        xml_file = os.path.join('script-tvguide-categories.xml')
        if os.path.join(SKIN, 'extras', 'skins', 'Default', '720p', xml_file):
            XML = xml_file
            
        return super(CategoriesMenu, cls).__new__(cls, XML, PATH)


    def __init__(self, database, categoriesList):
        """

        @type database: source.Database
        """
        super(CategoriesMenu, self).__init__()
        self.database = database

        self.allCategories = database.getCategoriesList()
        if categoriesList:
            self.currentCategories = list(categoriesList)
        else:
            self.currentCategories = list()

        self.workingCategories = list(self.currentCategories)

        self.swapInProgress = False


    @buggalo.buggalo_try_except({'method' : 'CategoriesMenu.onInit'})
    def onInit(self):
        self.updateCategoriesList()
        self.setFocusId(self.C_CATEGORIES_LIST)


    @buggalo.buggalo_try_except({'method' : 'CategoriesMenu.onAction'})
    def onAction(self, action):
        if action.getId() in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, KEY_NAV_BACK, KEY_CONTEXT_MENU]:
            self.close()
            return
     
    @buggalo.buggalo_try_except({'method' : 'CategoriesMenu.onClick'})
    def onClick(self, controlId):
        if controlId == self.C_CATEGORIES_LIST:            
            listControl = self.getControl(self.C_CATEGORIES_LIST)
            item        = listControl.getSelectedItem()
            category    = self.allCategories[int(item.getProperty('idx'))]           
            if category in self.workingCategories:
                self.workingCategories.remove(category)
            else:
                self.workingCategories.append(category)
 
            if category in self.workingCategories:
                iconImage = 'tvguide-categories-visible.png'
            else:
                iconImage = 'tvguide-categories-hidden.png'
            item.setIconImage(iconImage)
 
        elif controlId == self.C_CATEGORIES_SAVE:
            self.currentCategories = self.workingCategories
            self.close()
 
        elif controlId == self.C_CATEGORIES_CANCEL:
            self.close()

 
    def onFocus(self, controlId):
        pass

 
    def updateCategoriesList(self):
        listControl = self.getControl(self.C_CATEGORIES_LIST)
        listControl.reset()
        for idx, category in enumerate(self.allCategories):
            if category in self.workingCategories:
                iconImage = 'tvguide-categories-visible.png'
            else:
                iconImage = 'tvguide-categories-hidden.png'

            item = xbmcgui.ListItem('%3d. %s' % (idx+1, category), iconImage = iconImage)
            item.setProperty('idx', str(idx))
            listControl.addItem(item)


