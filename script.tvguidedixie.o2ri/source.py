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
import StringIO
import os
import threading
import datetime
import time
import urllib2
import urllib
from xml.etree import ElementTree
import buggalo
import xbmcaddon
import xbmcplugin
from strings import *
import xbmc
import xbmcgui
import xbmcvfs
import sqlite3

SOURCE     = ADDON.getSetting('source')
DIXIEURL   = ADDON.getSetting('dixie.url')
DIXIELOGOS = ADDON.getSetting('dixie.logo.folder')
XMLTVLOGOS = ADDON.getSetting('xmltv.logo.folder')
datapath   = xbmc.translatePath(ADDON.getAddonInfo('profile'))
extras     = os.path.join(datapath, 'extras')
logopath   = os.path.join(extras, 'logos')
logos      = None

if SOURCE == 'DIXIE':
    logos = os.path.join(logopath, DIXIELOGOS)
else:
    logos = XMLTVLOGOS

################### MIGRATE SETTINGS ###################
if SOURCE == 'XMLTV':
    ADDON.setSetting('categories', '')

if DIXIEURL == 'North America':
    ADDON.setSetting('dixie.url', 'Dixie')

if DIXIEURL == 'SmoothStreams':
    ADDON.setSetting('dixie.url', 'XPat Planet')

if DIXIEURL == 'Datho Digital - DC Listings':
    ADDON.setSetting('dixie.url', 'XPat Planet')

if DIXIEURL == 'OffSide':
    ADDON.setSetting('dixie.url', 'Basic Channels')

if DIXIEURL == 'NTV':
    ADDON.setSetting('dixie.url', 'Basic Channels')

dixiecats = ADDON.getSetting('categories')
oldcats   = dixiecats
fixcats   = ''
# newcats   = ADDON.setSetting('categories', fixcats)
ntv       = 'NTV'
oss       = 'OffSide Streams'
stvb      = 'StreamTVBox'
ntvs      = 'NTV Scandinavian'

if oldcats == oss:
    cats_fix = dixiecats.replace(oldcats, fixcats)
    # newcats
elif oldcats == ntv:
    cats_fix = dixiecats.replace(oldcats, fixcats)
    # newcats
elif oldcats == stvb:
    cats_fix = dixiecats.replace(oldcats, fixcats)
    # newcats
elif oldcats == ntvs:
    cats_fix = dixiecats.replace(oldcats, fixcats)
else: pass

print '****** TV GUIDE DIXIE INFORMATION ******'
print '*************** LOGO PACK **************'
print logos


SETTINGS_TO_CHECK = ['source', 'xmltv.file', 'xmltv.logo.folder', 'dixie.url', 'dixie.logo.folder', 'gmtfrom']

class Channel(object):
    #SJP1 categories parameter moved to end
    def __init__(self, id, title, logo = None, streamUrl = None, visible = True, weight = -1, categories = ''):
        self.id = id
        self.title = title
        self.categories = categories
        self.logo = logo
        self.streamUrl = streamUrl
        self.visible = visible
        self.weight = weight

    def isPlayable(self):
        return hasattr(self, 'streamUrl') and self.streamUrl

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return 'Channel(id=%s, title=%s, categories=%s, logo=%s, streamUrl=%s)' \
               % (self.id, self.title, self.categories, self.logo, self.streamUrl)



class Program(object):
    def __init__(self, channel, title, startDate, endDate, description, subTitle, imageLarge = None, imageSmall = None, notificationScheduled = None):
        """

        @param channel:
        @type channel: source.Channel
        @param title:
        @param startDate:
        @param endDate:
        @param description:
        @param subTitle:
        @param imageLarge:
        @param imageSmall:
        """
        self.channel = channel
        self.title = title
        self.startDate = startDate
        self.endDate = endDate
        self.description = description
        self.subTitle = subTitle
        self.imageLarge = imageLarge
        self.imageSmall = imageSmall
        self.notificationScheduled = notificationScheduled
        


    def __repr__(self):
        return 'Program(channel=%s, title=%s, startDate=%s, endDate=%s, description=%s, subTitle=%s, imageLarge=%s, imageSmall=%s)' % \
            (self.channel, self.title, self.startDate, self.endDate, self.description, self.subTitle, self.imageLarge, self.imageSmall)

class SourceException(Exception):
    pass


class SourceUpdateCanceledException(SourceException):
    pass


class SourceNotConfiguredException(SourceException):
    pass


class DatabaseSchemaException(sqlite3.DatabaseError):
    pass


class Database(object):
    SOURCE_DB = 'source.db'

    def __init__(self, nChannel):
        self.conn = None
        self.eventQueue = list()
        self.event = threading.Event()
        self.eventResults = dict()

        self.categoriesList = None

        self.source = instantiateSource()

        self.updateInProgress = False
        self.updateFailed = False
        self.settingsChanged = None

        buggalo.addExtraData('source', self.source.KEY)
        for key in SETTINGS_TO_CHECK:
           buggalo.addExtraData('setting: %s' % key, ADDON.getSetting(key))

        self.channelList = list()

        profilePath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
        if not os.path.exists(profilePath):
            os.makedirs(profilePath)
        self.databasePath = os.path.join(profilePath, Database.SOURCE_DB)

        threading.Thread(name='Database Event Loop', target=self.eventLoop).start()

    def eventLoop(self):
        print 'Database.eventLoop() >>>>>>>>>> starting...'
        while True:
            self.event.wait()
            self.event.clear()

            event = self.eventQueue.pop(0)

            command = event[0]
            callback = event[1]

            print 'Database.eventLoop() >>>>>>>>>> processing command: ' + command.__name__

            try:
                result = command(*event[2:])
                self.eventResults[command.__name__] = result

                if callback:
                    if self._initialize == command:
                        threading.Thread(name='Database callback', target=callback, args=[result]).start()
                    else:
                        threading.Thread(name='Database callback', target=callback).start()

                if self._close == command:
                    del self.eventQueue[:]
                    break


            except Exception:
                print 'Database.eventLoop() >>>>>>>>>> exception!'
                buggalo.onExceptionRaised()

        print 'Database.eventLoop() >>>>>>>>>> exiting...'

    def _invokeAndBlockForResult(self, method, *args):
        event = [method, None]
        event.extend(args)
        self.eventQueue.append(event)
        self.event.set()

        while not self.eventResults.has_key(method.__name__):
            time.sleep(0.1)

        result = self.eventResults.get(method.__name__)
        del self.eventResults[method.__name__]
        return result

    def initialize(self, callback, cancel_requested_callback=None):
        self.eventQueue.append([self._initialize, callback, cancel_requested_callback])
        self.event.set()

    def _initialize(self, cancel_requested_callback):
        sqlite3.register_adapter(datetime.datetime, self.adapt_datetime)
        sqlite3.register_converter('timestamp', self.convert_datetime)

        self.alreadyTriedUnlinking = False
        while True:
            if cancel_requested_callback is not None and cancel_requested_callback():
                break

            try:
                self.conn = sqlite3.connect(self.databasePath, detect_types=sqlite3.PARSE_DECLTYPES)
                self.conn.execute('PRAGMA foreign_keys = ON')
                self.conn.row_factory = sqlite3.Row

                # create and drop dummy table to check if database is locked
                c = self.conn.cursor()
                c.execute('CREATE TABLE IF NOT EXISTS database_lock_check(id TEXT PRIMARY KEY)')
                c.execute('DROP TABLE database_lock_check')
                c.close()

                self._createTables()
                self.settingsChanged = self._wasSettingsChanged(ADDON)
                break

            except sqlite3.OperationalError:
                if cancel_requested_callback is None:
                    xbmc.log('[script.tvguidetest] Database is locked, bailing out...', xbmc.LOGDEBUG)
                    break
                else:  # ignore 'database is locked'
                    xbmc.log('[script.tvguidedixie] Database is locked, retrying...', xbmc.LOGDEBUG)

            except sqlite3.DatabaseError:
                self.conn = None
                if self.alreadyTriedUnlinking:
                    xbmc.log('[script.tvguidedixie] Database is broken and unlink() failed', xbmc.LOGDEBUG)
                    break
                else:
                    try:
                        os.unlink(self.databasePath)
                    except OSError:
                        pass
                    self.alreadyTriedUnlinking = True
                    xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), strings(DATABASE_SCHEMA_ERROR_1),
                                        strings(DATABASE_SCHEMA_ERROR_2), strings(DATABASE_SCHEMA_ERROR_3))

        return self.conn is not None

    def close(self, callback=None):
        self.eventQueue.append([self._close, callback])
        self.event.set()

    def _close(self):
        try:
            # rollback any non-commit'ed changes to avoid database lock
            if self.conn:
                self.conn.rollback()
        except sqlite3.OperationalError:
            pass  # no transaction is active
        if self.conn:
            self.conn.close()

    def _wasSettingsChanged(self, addon):
        settingsChanged = False
        noRows = True
        count = 0

        c = self.conn.cursor()
        c.execute('SELECT * FROM settings')
        for row in c:
            noRows = False
            key = row['key']
            if SETTINGS_TO_CHECK.count(key):
                count += 1
                if row['value'] != addon.getSetting(key):
                    settingsChanged = True

        if count != len(SETTINGS_TO_CHECK):
            settingsChanged = True

        if settingsChanged or noRows:
            for key in SETTINGS_TO_CHECK:
                value = addon.getSetting(key).decode('utf-8', 'ignore')
                c.execute('INSERT OR IGNORE INTO settings(key, value) VALUES (?, ?)', [key, value])
                if not c.rowcount:
                    c.execute('UPDATE settings SET value=? WHERE key=?', [value, key])
            self.conn.commit()

        c.close()
        print 'Settings changed: ' + str(settingsChanged)
        return settingsChanged

    def _isCacheExpired(self, date):
        if self.settingsChanged:
            return True
        
        channelsLastUpdated = datetime.datetime.fromtimestamp(0)
        programsLastUpdated = datetime.datetime.fromtimestamp(0)

        # check if channel data is up-to-date in database
        try:
            c = self.conn.cursor()
            c.execute('SELECT channels_updated FROM sources WHERE id=?', [self.source.KEY])
            row = c.fetchone()
            if not row:
                return True
            channelsLastUpdated = row['channels_updated']
            c.close()
        except TypeError:
            return True

        # check if program data is up-to-date in database
        dateStr = date.strftime('%Y-%m-%d')
        c = self.conn.cursor()
        c.execute('SELECT programs_updated FROM updates WHERE source=? AND date=?', [self.source.KEY, dateStr])
        row = c.fetchone()
        if row:
            programsLastUpdated = row['programs_updated']
        c.close()

        return self.source.isUpdated(channelsLastUpdated, programsLastUpdated)

    def updateChannelAndProgramListCaches(self, callback, date = datetime.datetime.now(), progress_callback = None, clearExistingProgramList = True):
        self.eventQueue.append([self._updateChannelAndProgramListCaches, callback, date, progress_callback, clearExistingProgramList])
        self.event.set()

    def _updateChannelAndProgramListCaches(self, date, progress_callback, clearExistingProgramList):
        # todo workaround service.py 'forgets' the adapter and convert set in _initialize.. wtf?!
        sqlite3.register_adapter(datetime.datetime, self.adapt_datetime)
        sqlite3.register_converter('timestamp', self.convert_datetime)

        if not self._isCacheExpired(date):
            return

        self.updateInProgress = True
        self.updateFailed = False
        dateStr = date.strftime('%Y-%m-%d')
        c = self.conn.cursor()
        try:
            xbmc.log('[script.tvguidedixie] Updating caches...', xbmc.LOGDEBUG)
            if progress_callback:
                progress_callback(0)

            if self.settingsChanged:
                self.source.doSettingsChanged(c)
            self.settingsChanged = False # only want to update once due to changed settings

            clearExistingProgramList = True
            if clearExistingProgramList:
                c.execute("DELETE FROM updates WHERE source=?", [self.source.KEY])  # cascades and deletes associated programs records
            else:
                c.execute("DELETE FROM updates WHERE source=? AND date=?", [self.source.KEY, dateStr])  # cascades and deletes associated programs records

            # programs updated
            #c.execute("INSERT INTO updates(source, date, programs_updated) VALUES(?, ?, ?)", [self.source.KEY, dateStr, datetime.datetime.now()])
            updatesId = c.lastrowid
            c.execute("DELETE FROM programs WHERE source=?", [self.source.KEY])
            
            startDates = []

            imported = imported_channels = imported_programs = 0
            for item in self.source.getDataFromExternal(date, progress_callback):
                imported += 1

                if imported % 10000 == 0:
                    self.conn.commit()

                if isinstance(item, Channel):
                    imported_channels += 1
                    channel = item
                    c.execute('INSERT OR IGNORE INTO channels(id, title, categories, logo, stream_url, visible, weight, source) VALUES(?, ?, ?, ?, ?, ?, (CASE ? WHEN -1 THEN (SELECT COALESCE(MAX(weight)+1, 0) FROM channels WHERE source=?) ELSE ? END), ?)', [channel.id, channel.title, channel.categories, channel.logo, channel.streamUrl, channel.visible, channel.weight, self.source.KEY, channel.weight, self.source.KEY])
                    if not c.rowcount:
                        c.execute('UPDATE channels SET title=?, categories=?, logo=?, stream_url=?, visible=(CASE ? WHEN -1 THEN visible ELSE ? END), weight=(CASE ? WHEN -1 THEN weight ELSE ? END) WHERE id=? AND source=?',
                            [channel.title, channel.categories, channel.logo, channel.streamUrl, channel.weight, channel.visible, channel.weight, channel.weight, channel.id, self.source.KEY])

                elif isinstance(item, Program):
                    imported_programs += 1
                    program = item
                    if isinstance(program.channel, Channel):
                        channel = program.channel.id
                    else:
                        channel = program.channel
                        
                    if program.startDate.date() not in startDates:
                        startDates.append(program.startDate.date())
                        
                    c.execute('INSERT INTO programs(channel, title, start_date, end_date, description, subTitle, image_large, image_small, source, updates_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                        [channel, program.title, program.startDate, program.endDate, program.description, program.subTitle, program.imageLarge, program.imageSmall, self.source.KEY, updatesId])
                        
            # programs updated
            
            #startDates = startDates[:-1] #remove last date, will cause new data to be fetched when just 1 day of data left
            if len(startDates) > 0:
                startDates.sort()
                #startDates = startDates[:-1] #remove last date, will cause new data to be fetched when just 1 day of data left
                for date in startDates:        
                    dateStr = date.strftime('%Y-%m-%d')
                    c.execute("INSERT INTO updates(source, date, programs_updated) VALUES(?, ?, ?)", [self.source.KEY, dateStr, datetime.datetime.now()])
            c.execute("UPDATE sources SET channels_updated=? WHERE id=?", [datetime.datetime.now(), self.source.KEY])
            self.conn.commit()

            if imported_channels == 0 or imported_programs == 0:
                self.updateFailed = True

        except SourceUpdateCanceledException:
            # force source update on next load
            c.execute('UPDATE sources SET channels_updated=? WHERE id=?', [0, self.source.KEY])
            c.execute("DELETE FROM updates WHERE source=?", [self.source.KEY]) # cascades and deletes associated programs records
            self.conn.commit()

        except Exception:
            import traceback as tb
            import sys
            (etype, value, traceback) = sys.exc_info()
            tb.print_exception(etype, value, traceback)

            try:
                self.conn.rollback()
            except sqlite3.OperationalError:
                pass # no transaction is active

            try:
                # invalidate cached data
                c.execute('UPDATE sources SET channels_updated=? WHERE id=?', [0, self.source.KEY])
                self.conn.commit()
            except sqlite3.OperationalError:
                pass # database is locked

            self.updateFailed = True
        finally:
            self.updateInProgress = False
            c.close()

    def getEPGView(self, channelStart, date = datetime.datetime.now(), progress_callback = None, clearExistingProgramList = True, categories = None, nmrChannels=9):
        result = self._invokeAndBlockForResult(self._getEPGView, channelStart, date, progress_callback, clearExistingProgramList, categories, nmrChannels)

        if self.updateFailed:
            raise SourceException('No channels or programs imported')

        return result


    def _getEPGView(self, channelStart, date, progress_callback, clearExistingProgramList, categories, nmrChannels):
        self._updateChannelAndProgramListCaches(date, progress_callback, clearExistingProgramList)
        
        channels = self._getChannelList(onlyVisible = True, categories = categories)

        if channelStart < 0:
            channelStart = len(channels) - 1
        elif channelStart > len(channels) - 1:
            channelStart = 0
        channelEnd = channelStart + nmrChannels
        channelsOnPage = channels[channelStart : channelEnd]

        programs = self._getProgramList(channelsOnPage, date)

        return [channelStart, channelsOnPage, programs]


    def getNextChannel(self, currentChannel):
        channels = self.getChannelList()
        idx = channels.index(currentChannel)
        idx += 1
        if idx > len(channels) - 1:
            idx = 0
        return channels[idx]

    def getPreviousChannel(self, currentChannel):
        channels = self.getChannelList()
        idx = channels.index(currentChannel)
        idx -= 1
        if idx < 0:
            idx = len(channels) - 1
        return channels[idx]

    def saveChannelList(self, callback, channelList):
        self.eventQueue.append([self._saveChannelList, callback, channelList])
        self.event.set()

    def _saveChannelList(self, channelList):
        c = self.conn.cursor()
        for idx, channel in enumerate(channelList):
            c.execute('INSERT OR IGNORE INTO channels(id, title, categories, logo, stream_url, visible, weight, source) VALUES(?, ?, ?, ?, ?, ?, (CASE ? WHEN -1 THEN (SELECT COALESCE(MAX(weight)+1, 0) FROM channels WHERE source=?) ELSE ? END), ?)', [channel.id, channel.title, channel.categories, channel.logo, channel.streamUrl, channel.visible, channel.weight, self.source.KEY, channel.weight, self.source.KEY])
            if not c.rowcount:
                c.execute('UPDATE channels SET title=?, categories=?, logo=?, stream_url=?, visible=?, weight=(CASE ? WHEN -1 THEN weight ELSE ? END) WHERE id=? AND source=?', [channel.title, channel.categories, channel.logo, channel.streamUrl, channel.visible, channel.weight, channel.weight, channel.id, self.source.KEY])

        c.execute("UPDATE sources SET channels_updated=? WHERE id=?", [datetime.datetime.now(), self.source.KEY])
        self.channelList = None
        self.conn.commit()

    def getChannelList(self, onlyVisible = True):
        if not self.channelList or not onlyVisible:
            result = self._invokeAndBlockForResult(self._getChannelList, onlyVisible)

            if not onlyVisible:
                return result

            self.channelList = result
        return self.channelList


    def _getChannelList(self, onlyVisible, categories = None):
        if categories and len(categories) > 0:
            return self._getChannelListFilteredByCategory(onlyVisible, categories)
        c = self.conn.cursor()
        channelList = list()
        if onlyVisible:
            c.execute('SELECT * FROM channels WHERE source=? AND visible=? ORDER BY weight', [self.source.KEY, True])
        else:
            c.execute('SELECT * FROM channels WHERE source=? ORDER BY weight', [self.source.KEY])
        for row in c:
            channel = Channel(row['id'], row['title'], row['logo'], row['stream_url'], row['visible'], row['weight'], row['categories'])
            channelList.append(channel)
        c.close()
        return channelList


    def _getChannelListFilteredByCategory(self, onlyVisible, categories):
        channelList = list()

        c = self.conn.cursor()
        if onlyVisible:
            c.execute('SELECT * FROM channels WHERE source=? AND visible=? ORDER BY weight', [self.source.KEY, True])
        else:
            c.execute('SELECT * FROM channels WHERE source=? ORDER BY weight', [self.source.KEY])

        for row in c:
            channelCats = row['categories']
            channelCats = channelCats.split('|')
            for category in channelCats:
                if category in categories:
                    channel = Channel(row['id'], row['title'], row['logo'], row['stream_url'], row['visible'], row['weight'], row['categories'])      
                    channelList.append(channel)
                    break
        c.close()
        return channelList


    def getCategoriesList(self):
        if not self.categoriesList:
           self.categoriesList = self._invokeAndBlockForResult(self._getCategoriesList)
        return self.categoriesList

    def _getCategoriesList(self):
        c = self.conn.cursor()
        categoriesList = list()
        c.execute('SELECT * FROM channels WHERE source=? ORDER BY categories', [self.source.KEY])

        for row in c:
            categories = row['categories']
            categories = categories.split('|')
            for category in categories:
                if category not in categoriesList:
                    categoriesList.append(category)

        c.close()
        return categoriesList


    def getCurrentProgram(self, channel):
        return self._invokeAndBlockForResult(self._getCurrentProgram, channel)

    def _getCurrentProgram(self, channel):
        """

        @param channel:
        @type channel: source.Channel
        @return:
        """
        program = None
        now = datetime.datetime.now()
        c = self.conn.cursor()
        c.execute('SELECT * FROM programs WHERE channel=? AND source=? AND start_date <= ? AND end_date >= ?', [channel.id, self.source.KEY, now, now])
        row = c.fetchone()
        if row:
            program = Program(channel, row['title'], row['start_date'], row['end_date'], row['description'], row['subTitle'], row['image_large'], row['image_small'])
        c.close()

        return program

    def getNextProgram(self, channel):
        return self._invokeAndBlockForResult(self._getNextProgram, channel)

    def _getNextProgram(self, program):
        nextProgram = None
        c = self.conn.cursor()
        c.execute('SELECT * FROM programs WHERE channel=? AND source=? AND start_date >= ? ORDER BY start_date ASC LIMIT 1', [program.channel.id, self.source.KEY, program.endDate])
        row = c.fetchone()
        if row:
            nextProgram = Program(program.channel, row['title'], row['start_date'], row['end_date'], row['description'], row['subTitle'], row['image_large'], row['image_small'])
        c.close()

        return nextProgram

    def getPreviousProgram(self, channel):
        return self._invokeAndBlockForResult(self._getPreviousProgram, channel)

    def _getPreviousProgram(self, program):
        previousProgram = None
        c = self.conn.cursor()
        c.execute('SELECT * FROM programs WHERE channel=? AND source=? AND end_date <= ? ORDER BY start_date DESC LIMIT 1', [program.channel.id, self.source.KEY, program.startDate])
        row = c.fetchone()
        if row:
            previousProgram = Program(program.channel, row['title'], row['start_date'], row['end_date'], row['description'], row['subTitle'], row['image_large'], row['image_small'])
        c.close()

        return previousProgram

    def _getProgramList(self, channels, startTime):
        """

        @param channels:
        @type channels: list of source.Channel
        @param startTime:
        @type startTime: datetime.datetime
        @return:
        """
        endTime = startTime + datetime.timedelta(hours = 2)
        programList = list()

        channelMap = dict()
        for c in channels:
            if c.id:
                channelMap[c.id] = c

        if not channels:
            return []

        c = self.conn.cursor()
        c.execute('SELECT p.*, (SELECT 1 FROM notifications n WHERE n.channel=p.channel AND n.program_title=p.title AND n.source=p.source) AS notification_scheduled FROM programs p WHERE p.channel IN (\'' + ('\',\''.join(channelMap.keys())) + '\') AND p.source=? AND p.end_date > ? AND p.start_date < ?', [self.source.KEY, startTime, endTime])
        for row in c:
            program = Program(channelMap[row['channel']], row['title'], row['start_date'], row['end_date'], row['description'], row['subTitle'], row['image_large'], row['image_small'], row['notification_scheduled'])
            programList.append(program)

        return programList

    def _isProgramListCacheExpired(self, date = datetime.datetime.now()):
        # check if data is up-to-date in database
        dateStr = date.strftime('%Y-%m-%d')
        c = self.conn.cursor()
        c.execute('SELECT programs_updated FROM updates WHERE source=? AND date=?', [self.source.KEY, dateStr])
        row = c.fetchone()
        today = datetime.datetime.now()
        expired = row is None or row['programs_updated'].day != today.day
        c.close()
        return expired

    def setCustomStreamUrl(self, channel, stream_url):
        if stream_url is not None:
            self._invokeAndBlockForResult(self._setCustomStreamUrl, channel, stream_url)
        # no result, but block until operation is done

    def _setCustomStreamUrl(self, channel, stream_url):
        if stream_url is not None:
            c = self.conn.cursor()
            c.execute("DELETE FROM custom_stream_url WHERE channel=?", [channel.id])
            c.execute("INSERT INTO custom_stream_url(channel, stream_url) VALUES(?, ?)", [channel.id, stream_url.decode('utf-8', 'ignore')])
            self.conn.commit()
            c.close()

    def getCustomStreamUrl(self, channel):
        return self._invokeAndBlockForResult(self._getCustomStreamUrl, channel)

    def _getCustomStreamUrl(self, channel):
        c = self.conn.cursor()
        c.execute("SELECT stream_url FROM custom_stream_url WHERE channel=?", [channel.id])
        stream_url = c.fetchone()
        c.close()

        if stream_url:
            return stream_url[0]
        else:
            return None

    def deleteCustomStreamUrl(self, channel):
        self.eventQueue.append([self._deleteCustomStreamUrl, None, channel])
        self.event.set()

    def _deleteCustomStreamUrl(self, channel):
        c = self.conn.cursor()
        c.execute("DELETE FROM custom_stream_url WHERE channel=?", [channel.id])
        self.conn.commit()
        c.close()

    def getStreamUrl(self, channel):
        customStreamUrl = self.getCustomStreamUrl(channel)
        if customStreamUrl:
            customStreamUrl = customStreamUrl.encode('utf-8', 'ignore')
            return customStreamUrl

        elif channel.isPlayable():
            streamUrl = channel.streamUrl.encode('utf-8', 'ignore')
            return streamUrl

        return None

    def adapt_datetime(self, ts):
        # http://docs.python.org/2/library/sqlite3.html#registering-an-adapter-callable
        return time.mktime(ts.timetuple())

    def convert_datetime(self, ts):
        try:
            return datetime.datetime.fromtimestamp(float(ts))
        except ValueError:
            return None

    def _createTables(self):
        c = self.conn.cursor()

        try:
            c.execute('SELECT major, minor, patch FROM version')
            (major, minor, patch) = c.fetchone()
            version = [major, minor, patch]
        except sqlite3.OperationalError:
            version = [0, 0, 0]

        try:
            c.execute("ALTER TABLE channels add column 'categories' 'TEXT'")
            c.execute("ALTER TABLE programs add column 'subTitle' 'TEXT'")
        except:
            pass            

        try:
            if version < [1, 3, 0]:
                c.execute('CREATE TABLE IF NOT EXISTS custom_stream_url(channel TEXT, stream_url TEXT)')
                c.execute('CREATE TABLE version (major INTEGER, minor INTEGER, patch INTEGER)')
                c.execute('INSERT INTO version(major, minor, patch) VALUES(1, 3, 0)')

                # For caching data
                c.execute('CREATE TABLE sources(id TEXT PRIMARY KEY, channels_updated TIMESTAMP)')
                c.execute('CREATE TABLE updates(id INTEGER PRIMARY KEY, source TEXT, date TEXT, programs_updated TIMESTAMP)')
                c.execute('CREATE TABLE channels(id TEXT, title TEXT, categories TEXT, logo TEXT, stream_url TEXT, source TEXT, visible BOOLEAN, weight INTEGER, PRIMARY KEY (id, source), FOREIGN KEY(source) REFERENCES sources(id) ON DELETE CASCADE)')
                c.execute('CREATE TABLE programs(channel TEXT, title TEXT, start_date TIMESTAMP, end_date TIMESTAMP, description TEXT, subTitle TEXT, image_large TEXT, image_small TEXT, source TEXT, updates_id INTEGER, FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE, FOREIGN KEY(updates_id) REFERENCES updates(id) ON DELETE CASCADE)')
                c.execute('CREATE INDEX program_list_idx ON programs(source, channel, start_date, end_date)')
                c.execute('CREATE INDEX start_date_idx ON programs(start_date)')
                c.execute('CREATE INDEX end_date_idx ON programs(end_date)')
                # For active setting
                c.execute('CREATE TABLE settings(key TEXT PRIMARY KEY, value TEXT)')

                # For notifications
                c.execute("CREATE TABLE notifications(channel TEXT, program_title TEXT, source TEXT, FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE)")

            if version < [1, 3, 1]:
                # Recreate tables with FOREIGN KEYS as DEFERRABLE INITIALLY DEFERRED
                c.execute('UPDATE version SET major=1, minor=3, patch=1')
                c.execute('DROP TABLE channels')
                c.execute('DROP TABLE programs')
                c.execute('CREATE TABLE channels(id TEXT, title TEXT, categories TEXT, logo TEXT, stream_url TEXT, source TEXT, visible BOOLEAN, weight INTEGER, PRIMARY KEY (id, source), FOREIGN KEY(source) REFERENCES sources(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED)')
                c.execute('CREATE TABLE programs(channel TEXT, title TEXT, start_date TIMESTAMP, end_date TIMESTAMP, description TEXT, subTitle TEXT, image_large TEXT, image_small TEXT, source TEXT, updates_id INTEGER, FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED, FOREIGN KEY(updates_id) REFERENCES updates(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED)')
                c.execute('CREATE INDEX program_list_idx ON programs(source, channel, start_date, end_date)')
                c.execute('CREATE INDEX start_date_idx ON programs(start_date)')
                c.execute('CREATE INDEX end_date_idx ON programs(end_date)')
            # make sure we have a record in sources for this Source
            c.execute("INSERT OR IGNORE INTO sources(id, channels_updated) VALUES(?, ?)", [self.source.KEY, 0])
            self.conn.commit()
            c.close()

        except sqlite3.OperationalError, ex:
            raise DatabaseSchemaException(ex)

    def addNotification(self, program):
        self._invokeAndBlockForResult(self._addNotification, program)
        # no result, but block until operation is done

    def _addNotification(self, program):
        """
        @type program: source.program
        """
        c = self.conn.cursor()
        c.execute("INSERT INTO notifications(channel, program_title, source) VALUES(?, ?, ?)", [program.channel.id, program.title, self.source.KEY])
        self.conn.commit()
        c.close()

    def removeNotification(self, program):
        self._invokeAndBlockForResult(self._removeNotification, program)
        # no result, but block until operation is done

    def _removeNotification(self, program):
        """
        @type program: source.program
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM notifications WHERE channel=? AND program_title=? AND source=?", [program.channel.id, program.title, self.source.KEY])
        self.conn.commit()
        c.close()


    def getNotifications(self, daysLimit = 2):
        return self._invokeAndBlockForResult(self._getNotifications, daysLimit)

    def _getNotifications(self, daysLimit):
        start = datetime.datetime.now()
        end = start + datetime.timedelta(days = daysLimit)
        c = self.conn.cursor()
        c.execute("SELECT DISTINCT c.title, p.title, p.start_date FROM notifications n, channels c, programs p WHERE n.channel = c.id AND p.channel = c.id AND n.program_title = p.title AND n.source=? AND p.start_date >= ? AND p.end_date <= ?", [self.source.KEY, start, end])
        programs = c.fetchall()
        c.close()

        return programs

    def isNotificationRequiredForProgram(self, program):
        return self._invokeAndBlockForResult(self._isNotificationRequiredForProgram, program)

    def _isNotificationRequiredForProgram(self, program):
        """
        @type program: source.program
        """
        c = self.conn.cursor()
        c.execute("SELECT 1 FROM notifications WHERE channel=? AND program_title=? AND source=?", [program.channel.id, program.title, self.source.KEY])
        result = c.fetchone()
        c.close()

        return result

    def clearAllNotifications(self):
        self._invokeAndBlockForResult(self._clearAllNotifications)
        # no result, but block until operation is done

    def _clearAllNotifications(self):
        c = self.conn.cursor()
        c.execute('DELETE FROM notifications')
        self.conn.commit()
        c.close()



class Source(object):
    def getDataFromExternal(self, date, progress_callback = None):
        """
        Retrieve data from external as a list or iterable. Data may contain both Channel and Program objects.
        The source may choose to ignore the date parameter and return all data available.

        @param date: the date to retrieve the data for
        @param progress_callback:
        @return:
        """
        return None

    def doSettingsChanged(self, c):
        c.execute('DELETE FROM channels WHERE source=?', [self.KEY])
        c.execute('DELETE FROM programs WHERE source=?', [self.KEY])
        c.execute("DELETE FROM updates WHERE source=?", [self.KEY])

    def isUpdated(self, channelsLastUpdated, programsLastUpdated):
        today = datetime.datetime.now()
        if channelsLastUpdated is None or channelsLastUpdated.day != today.day:
            return True

        if programsLastUpdated is None or programsLastUpdated.day != today.day:
            return True
        return False

    def _downloadUrl(self, url):
        u = urllib2.urlopen(url, timeout=30)
        content = u.read()
        u.close()

        return content


class YouSeeTvSource(Source):
    KEY = 'youseetv'

    def __init__(self, addon):
        self.date = datetime.datetime.today()
        self.channelCategory = addon.getSetting('youseetv.category')
        self.ysApi = ysapi.YouSeeTVGuideApi()

    def getDataFromExternal(self, date, progress_callback = None):
        channels = self.ysApi.channelsInCategory(self.channelCategory)
        for idx, channel in enumerate(channels):
            c = Channel(id = channel['id'], title = channel['name'], logo = channel['logo'])
            yield c

            for program in self.ysApi.programs(c.id, tvdate = date):
                description = program['description']
                if description is None:
                    description = strings(NO_DESCRIPTION)

                imagePrefix = program['imageprefix']

                p = Program(
                    c,
                    program['title'],
                    self._parseDate(program['begin']),
                    self._parseDate(program['end']),
                    description,
                    imagePrefix + program['images_sixteenbynine']['large'],
                    imagePrefix + program['images_sixteenbynine']['small'],
                )
                yield p


            if progress_callback:
                if not progress_callback(100.0 / len(channels) * idx):
                    raise SourceUpdateCanceledException()

    def _parseDate(self, dateString):
        return datetime.datetime.fromtimestamp(dateString)


class XMLTVSource(Source):
    KEY = 'xmltv'

    def __init__(self, addon):
        self.logoFolder = addon.getSetting('xmltv.logo.folder')
        self.xmltvFile = addon.getSetting('xmltv.file')

        if not self.xmltvFile or not xbmcvfs.exists(self.xmltvFile):
            raise SourceNotConfiguredException()

    def getDataFromExternal(self, date, progress_callback = None):
        f = FileWrapper(self.xmltvFile)
        context = ElementTree.iterparse(f, events=("start", "end"))
        return parseXMLTV(context, f, f.size, self.logoFolder, progress_callback)

    def isUpdated(self, channelsLastUpdated, programLastUpdate):
        if channelsLastUpdated is None or not xbmcvfs.exists(self.xmltvFile):
            return True

        stat = xbmcvfs.Stat(self.xmltvFile)
        fileUpdated = datetime.datetime.fromtimestamp(stat.st_mtime())
        return fileUpdated > channelsLastUpdated
        
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
        

class DIXIESource(Source):
    KEY = 'dixie'

    def isUpdated(self, channelsLastUpdated, programsLastUpdated):
        zero = datetime.datetime.fromtimestamp(0)
        
        if channelsLastUpdated is None or channelsLastUpdated == zero:
            return True
        
        if programsLastUpdated is None or programsLastUpdated == zero:
            return True
            
        return False

    def GetDixieUrl(self):
        dixieUrl = self.dixieUrl.upper()

        if dixieUrl == 'O2RI':
            dixieUrl = 'https://dl.dropboxusercontent.com/u/5461675/guide.xml'
            return dixieUrl
        if dixieUrl=='SELECTED':
                dixieUrl='https://dl.dropboxusercontent.com/u/5461675/selected.xml'
                return dixieUrl
            

    def __init__(self, addon):
        self.logoFolder = None
        if os.path.exists(logos):
            self.logoFolder = logos
            
        self.dixieUrl = addon.getSetting('dixie.url')
        self.KEY += '.' + self.dixieUrl.upper()
        self.xml = None
        #SJP store GMT offset from settings
        gmt = addon.getSetting('gmtfrom').replace('GMT', '')
        if gmt == '':
            self.offset = 0
        else:
            self.offset = int(gmt)


    def getDataFromExternal(self, date, progress_callback = None): 
        #SJP1
        categories = self.getCategories()
   
        if not self.xml:
            self.xml = self._downloadUrl(self.GetDixieUrl())
            self.xml = self.xml.replace("&amp;apos;", "'")

        io = StringIO.StringIO(self.xml)
        
        context = ElementTree.iterparse(io, events=("start", "end"))
        #SJP pass GMT offset in
        return parseXMLTV(context, io, len(self.xml), self.logoFolder, progress_callback, self.offset, categories)

    def doSettingsChanged(self, c):   
        c.execute('DELETE FROM programs WHERE source=?', [self.KEY])
        c.execute("DELETE FROM updates WHERE source=?", [self.KEY])


    #SJP1 this method returns a dictionary mapping channels to categories
    def getCategories(self):
        cat  = dict()
        path = os.path.join(datapath, 'cats.xml')
        url = 'https://dl.dropboxusercontent.com/u/5461675/cats2.xml'
        f = urllib2.urlopen(url, timeout=30)
        xml = f.read()
        f.close()

        xml = xml.replace('&', '&amp;')
        xml = StringIO.StringIO(xml)
        xml = ElementTree.iterparse(xml, events=("start", "end"))

        for event, elem in xml:
            try:
                if event == 'end':
                   if elem.tag == 'cats':
                       channel  = elem.findtext('channel')
                       category = elem.findtext('category')
                       if channel != '' and category != '':
                           cat[channel] = category
            except:
                pass

        return cat
        
#SJP add offset parameter
def parseXMLTVDate(dateString, offset):
    if dateString is not None:
        if dateString.find(' ') != -1:
            # remove timezone information
            dateString = dateString[:dateString.find(' ')]
        t = time.strptime(dateString, '%Y%m%d%H%M%S')
        d = datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
        d += datetime.timedelta(hours = offset)
        return d
    else:
        return None

#SJP add offset parameter                
def parseXMLTV(context, f, size, logoFolder, progress_callback, offset=0, categories=None):
    event, root = context.next()
    elements_parsed = 0

    for event, elem in context:
        if event == "end":
            result = None
            if elem.tag == "programme":
                channel = elem.get("channel")
                title = elem.findtext("title")
                subTitle = elem.findtext("sub-title")
                category = elem.findtext("category")
                description = elem.findtext("desc")
                mergeTitle = elem.findtext("sub-title")
                if not description:
                    description = subTitle
                if subTitle:
                    title += " " + "- " + mergeTitle
                    
                result = Program(channel, title, parseXMLTVDate(elem.get('start'), offset), parseXMLTVDate(elem.get('stop'), offset), description, elem.findtext("sub-title"))

            elif elem.tag == "channel":
                id = elem.get("id")
                title = elem.findtext("display-name")
                logo = None
                if logoFolder:
                    logoFile = os.path.join(logos, title + '.png')
                    if xbmcvfs.exists(logoFile):
                        logo = logoFile

                result = Channel(id, title, logo)
                #SJP1 now see if we have the category for this channel
                if categories:
                    try:
                        category = categories[title]
                        result.categories = category
                        #print 'The category for %s is %s' % (title, category)
                    except:
                        pass
                        #print 'Couldn't find %s in the categories' % title

            if result:
                elements_parsed += 1
                if progress_callback and elements_parsed % 500 == 0:
                    if not progress_callback(100.0 / size * f.tell()):
                        raise SourceUpdateCanceledException()
                yield result

        root.clear()
    f.close()
    
def parseCATEGORIES(self, f, context):
    import os
    path = os.path.join(datapath, 'cats.xml')
    if os.path.exists(path):
        f = open(path)
        xml = f.read()
        f.close()

    for event, elem in context:
        if event == "end":
            result = None
            if elem.get == "channel":
                categories = elem.findtext("category")
                result = Channel(categories)
            return self.categories
        else:
            return None



class FileWrapper(object):
    def __init__(self, filename):
        self.vfsfile = xbmcvfs.File(filename)
        self.size = self.vfsfile.size()
        self.bytesRead = 0

    def close(self):
        self.vfsfile.close()

    def read(self, bytes):
        self.bytesRead += bytes
        return self.vfsfile.read(bytes)

    def tell(self):
        return self.bytesRead


def instantiateSource():
    SOURCES = {
        'YouSee.tv' : YouSeeTvSource,
        'XMLTV' : XMLTVSource,
        'DIXIE' : DIXIESource
    }

    try:
        activeSource = SOURCES[ADDON.getSetting('source')]
    except KeyError:
        activeSource = SOURCES['YouSee.tv']

    return activeSource(ADDON)


