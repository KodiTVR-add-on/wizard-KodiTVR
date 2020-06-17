############################################################################
#                             /T /I                                        #
#                              / |/ | .-~/                                 #
#                          T\ Y  I  |/  /  _                               #
#         /T               | \I  |  I  Y.-~/                               #
#        I l   /I       T\ |  |  l  |  T  /                                #
#     T\ |  \ Y l  /T   | \I  l   \ `  l Y       If your going to copy     #
# __  | \l   \l  \I l __l  l   \   `  _. |       this addon just           #
# \ ~-l  `\   `\  \  \ ~\  \   `. .-~   |        give credit!              #
#  \   ~-. "-.  `  \  ^._ ^. "-.  /  \   |                                 #
#.--~-._  ~-  `  _  ~-_.-"-." ._ /._ ." ./        Stop Deleting the        #
# >--.  ~-.   ._  ~>-"    "\   7   7   ]          credits file!            #
#^.___~"--._    ~-{  .-~ .  `\ Y . /    |                                  #
# <__ ~"-.  ~       /_/   \   \I  Y   : |                                  #
#   ^-.__           ~(_/   \   >._:   | l______                            #
#       ^--.,___.-~"  /_/   !  `-.~"--l_ /     ~"-.                        #
#              (_/ .  ~(   /'     "~"--,Y   -=b-. _)                       #
#               (_/ .  \  :           / l      c"~o \                      #
#                \ /    `.    .     .^   \_.-~"~--.  )                     #
#                 (_/ .   `  /     /       !       )/                      #
#                  / / _.   '.   .':      /        '                       #
#                  ~(_/ .   /    _  `  .-<_                                #
#                    /_/ . ' .-~" `.  / \  \          ,z=.  Surfacingx     #
#                    ~( /   '  :   | K   "-.~-.______//   Original Author  #
#                      "-,.    l   I/ \_    __{--->._(==.                  #
#                       //(     \  <    ~"~"     //                        #
#                      /' /\     \  \     ,v=.  ((     Fire TV Guru        #
#                    .^. / /\     "  }__ //===-  `    PyXBMCt LaYOUt       #
#                   / / ' '  "-.,__ {---(==-                               #
#                 .^ '       :  T  ~"   ll                                 #
#                / .  .  . : | :!        \                                 #
#               (_/  /   | | j-"          ~^                               #
#                 ~-<_(_.^-~"                                              #
#                                                                          #
#                  Copyright (C) One of those Years....                    #
#                                                                          #
#  This program is free software: you can redistribute it and/or modify    #
#  it under the terms of the GNU General Public License as published by    #
#  the Free Software Foundation, either version 3 of the License, or       #
#  (at your option) any later version.                                     #
#                                                                          #
#  This program is distributed in the hope that it will be useful,         #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#  GNU General Public License for more details.                            #
#                                                                          #
############################################################################
import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob
import shutil
import urllib2,urllib
import re
import zipfile
import uservar
import fnmatch
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database
from datetime import date, datetime, timedelta
from urlparse import urljoin
from resources.libs import extract, downloader, notify, debridit, traktit, allucit, loginit, net, skinSwitch, uploadLog, yt, speedtest, wizard as wiz, addonwindow as pyxbmct


ADDON_ID         = uservar.ADDON_ID
ADDONTITLE       = uservar.ADDONTITLE
ADDON            = wiz.addonId(ADDON_ID)
VERSION          = wiz.addonInfo(ADDON_ID,'version')
ADDONPATH        = wiz.addonInfo(ADDON_ID, 'path')
DIALOG           = xbmcgui.Dialog()
DP               = xbmcgui.DialogProgress()
HOME             = xbmc.translatePath('special://home/')
LOG              = xbmc.translatePath('special://logpath/')
PROFILE          = xbmc.translatePath('special://profile/')
TEMPDIR          = xbmc.translatePath('special://temp')
ADDONS           = os.path.join(HOME,      'addons')
USERDATA         = os.path.join(HOME,      'userdata')
PLUGIN           = os.path.join(ADDONS,    ADDON_ID)
PACKAGES         = os.path.join(ADDONS,    'packages')
ADDOND           = os.path.join(USERDATA,  'addon_data')
ADDONDATA        = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADVANCED         = os.path.join(USERDATA,  'advancedsettings.xml')
SOURCES          = os.path.join(USERDATA,  'sources.xml')
FAVOURITES       = os.path.join(USERDATA,  'favourites.xml')
PROFILES         = os.path.join(USERDATA,  'profiles.xml')
GUISETTINGS      = os.path.join(USERDATA,  'guisettings.xml')
THUMBS           = os.path.join(USERDATA,  'Thumbnails')
DATABASE         = os.path.join(USERDATA,  'Database')
FANART           = os.path.join(PLUGIN,    'fanart.jpg')
ICON             = os.path.join(PLUGIN,    'icon.png')
ART              = os.path.join(PLUGIN,    'resources', 'art')
WIZLOG           = os.path.join(ADDONDATA, 'wizard.log')
SPEEDTESTFOLD    = os.path.join(ADDONDATA, 'SpeedTest')
ARCHIVE_CACHE    = os.path.join(TEMPDIR,   'archive_cache')
SKIN             = xbmc.getSkinDir()
BUILDNAME        = wiz.getS('buildname')
DEFAULTSKIN      = wiz.getS('defaultskin')
DEFAULTNAME      = wiz.getS('defaultskinname')
DEFAULTIGNORE    = wiz.getS('defaultskinignore')
BUILDVERSION     = wiz.getS('buildversion')
BUILDTHEME       = wiz.getS('buildtheme')
BUILDLATEST      = wiz.getS('latestversion')
SHOW15           = wiz.getS('show15')
SHOW16           = wiz.getS('show16')
SHOW17           = wiz.getS('show17')
SHOW18           = wiz.getS('show18')
SHOWADULT        = wiz.getS('adult')
SHOWMAINT        = wiz.getS('showmaint')
AUTOCLEANUP      = wiz.getS('autoclean')
AUTOCACHE        = wiz.getS('clearcache')
AUTOPACKAGES     = wiz.getS('clearpackages')
AUTOTHUMBS       = wiz.getS('clearthumbs')
AUTOFEQ          = wiz.getS('autocleanfeq')
AUTONEXTRUN      = wiz.getS('nextautocleanup')
INCLUDEVIDEO     = wiz.getS('includevideo')
INCLUDEALL       = wiz.getS('includeall')
INCLUDEBOB       = wiz.getS('includebob')
INCLUDEPHOENIX   = wiz.getS('includephoenix')
INCLUDESPECTO    = wiz.getS('includespecto')
INCLUDEGENESIS   = wiz.getS('includegenesis')
INCLUDEEXODUS    = wiz.getS('includeexodus')
INCLUDEONECHAN   = wiz.getS('includeonechan')
INCLUDESALTS     = wiz.getS('includesalts')
INCLUDESALTSHD   = wiz.getS('includesaltslite')
SEPERATE         = wiz.getS('seperate')
NOTIFY           = wiz.getS('notify')
NOTEID           = wiz.getS('noteid')
NOTEDISMISS      = wiz.getS('notedismiss')
TRAKTSAVE        = wiz.getS('traktlastsave')
REALSAVE         = wiz.getS('debridlastsave')
ALLUCSAVE        = wiz.getS('alluclastsave')
LOGINSAVE        = wiz.getS('loginlastsave')
KEEPFAVS         = wiz.getS('keepfavourites')
FAVSsave         = wiz.getS('favouriteslastsave')
KEEPSOURCES      = wiz.getS('keepsources')
KEEPPROFILES     = wiz.getS('keepprofiles')
KEEPADVANCED     = wiz.getS('keepadvanced')
KEEPREPOS        = wiz.getS('keeprepos')
KEEPSUPER        = wiz.getS('keepsuper')
KEEPWHITELIST    = wiz.getS('keepwhitelist')
KEEPTRAKT        = wiz.getS('keeptrakt')
KEEPREAL         = wiz.getS('keepdebrid')
KEEPALLUC        = wiz.getS('keepalluc')
KEEPLOGIN        = wiz.getS('keeplogin')
DEVELOPER        = wiz.getS('developer')
THIRDPARTY       = wiz.getS('enable3rd')
THIRD1NAME       = wiz.getS('wizard1name')
THIRD1URL        = wiz.getS('wizard1url')
THIRD2NAME       = wiz.getS('wizard2name')
THIRD2URL        = wiz.getS('wizard2url')
THIRD3NAME       = wiz.getS('wizard3name')
THIRD3URL        = wiz.getS('wizard3url')
BACKUPLOCATION   = ADDON.getSetting('path') if not ADDON.getSetting('path') == '' else 'special://home/'
BACKUPROMS       = wiz.getS('rompath')
MYBUILDS         = os.path.join(BACKUPLOCATION, 'My_Builds', '')
AUTOFEQ          = int(float(AUTOFEQ)) if AUTOFEQ.isdigit() else 0
TODAY            = date.today()
TOMORROW         = TODAY + timedelta(days=1)
THREEDAYS        = TODAY + timedelta(days=3)
KODIV          = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
if KODIV > 17:
	from resources.libs import zfile as zipfile #FTG mod for Kodi 18
else:
	import zipfile
MCNAME           = wiz.mediaCenter()
EXCLUDES         = uservar.EXCLUDES
CACHETEXT        = uservar.CACHETEXT
CACHEAGE         = uservar.CACHEAGE if str(uservar.CACHEAGE).isdigit() else 30
BUILDFILE        = uservar.BUILDFILE
ADDONPACK        = uservar.ADDONPACK
APKFILE          = uservar.APKFILE
YOUTUBETITLE     = uservar.YOUTUBETITLE
YOUTUBEFILE      = uservar.YOUTUBEFILE
ADDONFILE        = uservar.ADDONFILE
ADVANCEDFILE     = uservar.ADVANCEDFILE
UPDATECHECK      = uservar.UPDATECHECK if str(uservar.UPDATECHECK).isdigit() else 1
NEXTCHECK        = TODAY + timedelta(days=UPDATECHECK)
NOTIFICATION     = uservar.NOTIFICATION
ENABLE           = uservar.ENABLE
HEADERMESSAGE    = uservar.HEADERMESSAGE
AUTOUPDATE       = uservar.AUTOUPDATE  
BUILDERNAME      = uservar.BUILDERNAME  
WIZARDFILE       = uservar.WIZARDFILE
HIDECONTACT      = uservar.HIDECONTACT
CONTACT          = uservar.CONTACT
CONTACTICON      = uservar.CONTACTICON if not uservar.CONTACTICON == 'http://' else ICON 
CONTACTFANART    = uservar.CONTACTFANART if not uservar.CONTACTFANART == 'http://' else FANART
HIDESPACERS      = uservar.HIDESPACERS
COLOR1           = uservar.COLOR1
COLOR2           = uservar.COLOR2
THEME1           = uservar.THEME1
THEME2           = uservar.THEME2
THEME3           = uservar.THEME3
THEME4           = uservar.THEME4
THEME5           = uservar.THEME5
THEME6           = uservar.THEME6
ICONBUILDS       = uservar.ICONBUILDS if not uservar.ICONBUILDS == 'http://' else ICON
ICONMAINT        = uservar.ICONMAINT if not uservar.ICONMAINT == 'http://' else ICON
ICONAPK          = uservar.ICONAPK if not uservar.ICONAPK == 'http://' else ICON
ICONADDONS       = uservar.ICONADDONS if not uservar.ICONADDONS == 'http://' else ICON
ICONYOUTUBE      = uservar.ICONYOUTUBE if not uservar.ICONYOUTUBE == 'http://' else ICON
ICONSAVE         = uservar.ICONSAVE if not uservar.ICONSAVE == 'http://' else ICON
ICONTRAKT        = uservar.ICONTRAKT if not uservar.ICONTRAKT == 'http://' else ICON
ICONREAL         = uservar.ICONREAL if not uservar.ICONREAL == 'http://' else ICON
ICONLOGIN        = uservar.ICONLOGIN if not uservar.ICONLOGIN == 'http://' else ICON
ICONCONTACT      = uservar.ICONCONTACT if not uservar.ICONCONTACT == 'http://' else ICON
ICONSETTINGS     = uservar.ICONSETTINGS if not uservar.ICONSETTINGS == 'http://' else ICON
Images           = xbmc.translatePath(os.path.join('special://home','addons',ADDON_ID,'resources','images/'));
LOGFILES         = wiz.LOGFILES
TRAKTID          = traktit.TRAKTID
DEBRIDID         = debridit.DEBRIDID
LOGINID          = loginit.LOGINID
ALLUCID          = allucit.ALLUCID
MODURL           = 'http://tribeca.tvaddons.ag/tools/maintenance/modules/'
MODURL2          = 'http://mirrors.kodi.tv/addons/jarvis/'
INSTALLMETHODS   = ['Always Ask', 'Reload Profile', 'Force Close']
DEFAULTPLUGINS   = ['metadata.album.universal', 'metadata.artists.universal', 'metadata.common.fanart.tv', 'metadata.common.imdb.com', 'metadata.common.musicbrainz.org', 'metadata.themoviedb.org', 'metadata.tvdb.com', 'service.xbmc.versioncheck']
#FTG MOD##
ROMPACK          = uservar.ROMPACK
EMUAPKS          = uservar.EMUAPKS
ROMPATH          = ADDON.getSetting('rompath') if not ADDON.getSetting('rompath') == '' else 'special://home/'
ROMLOC           = os.path.join(ROMPATH, 'Roms', '')
try:
	INSTALLMETHOD    = int(float(wiz.getS('installmethod')))
except:
	INSTALLMETHOD    = 0



	

###########################
###### Menu Items   #######
###########################
#addDir (display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None)
#addFile(display,mode,name=None,url=None,menu=None,overwrite=True,fanart=FANART,icon=ICON, themeit=None)
def index():
	errors = int(errorChecking(count=True))
	err = str(errors)
	errorsfound = '[COLOR red]%s[/COLOR] Error(s) Found'  % (err) if errors > 0 else 'None Found'
	if AUTOUPDATE == 'Yes':
		wizfile = wiz.textCache(WIZARDFILE)
		if not wizfile == False:
			ver = wiz.checkWizard('version')
			if ver > VERSION: addFile('%s [v%s] [COLOR red][B][UPDATE v%s][/B][/COLOR]' % (ADDONTITLE, VERSION, ver), 'wizardupdate', themeit=THEME2)
			else: addFile('%s [v%s]' % (ADDONTITLE, VERSION), '', themeit=THEME2)
		else: addFile('%s [v%s]' % (ADDONTITLE, VERSION), '', themeit=THEME2)
	else: addFile('%s [v%s]' % (ADDONTITLE, VERSION), '', themeit=THEME2)
	if len(BUILDNAME) > 0:
		version = wiz.checkBuild(BUILDNAME, 'version')
		build = '%s (v%s)' % (BUILDNAME, BUILDVERSION)
		if version > BUILDVERSION: build = '%s [COLOR red][B][UPDATE v%s][/B][/COLOR]' % (build, version)
		addDir(build,'viewbuild',BUILDNAME, themeit=THEME4)
		themefile = wiz.themeCount(BUILDNAME)
		if not themefile == False:
			addFile('None' if BUILDTHEME == "" else BUILDTHEME, 'theme', BUILDNAME, themeit=THEME5)
	else: addDir('None', 'builds', themeit=THEME4)
	if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	addDir ('Builds', 'builds',   icon=ICONBUILDS,   themeit=THEME1)
	addDir ('Maintenance', 'maint',    icon=ICONMAINT,    themeit=THEME1)
	addDir ('Internet Tools' ,'net', icon=ICONCONTACT, themeit=THEME1)
	if wiz.platform() == 'android' or DEVELOPER == 'true': addDir ('Apk Installer' ,'apk', icon=ICONAPK, themeit=THEME1)
	if wiz.platform() == 'android' or wiz.platform() == 'windows' or DEVELOPER == 'true': addDir ('Retro Gaming Zone'       ,'retromenu', icon=ICONSAVE,     themeit=THEME1)
	if not ADDONFILE == 'http://': addDir ('Addon Installer' ,'addons', icon=ICONADDONS, themeit=THEME1)
	if not YOUTUBEFILE == 'http://' and not YOUTUBETITLE == '': addDir (YOUTUBETITLE ,'youtube', icon=ICONYOUTUBE, themeit=THEME1)
	addDir ('Save Login Data / Favs Options', 'savedata', icon=ICONSAVE,     themeit=THEME1)
	addDir ('Backup/Restore Data Options'     ,'backup', icon=ICONSAVE,     themeit=THEME1)
	if HIDECONTACT == 'No': addFile('Contact' ,'contact', icon=ICONCONTACT,  themeit=THEME1)
	if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	addFile('Upload Log File', 'uploadlog',       icon=ICONMAINT, themeit=THEME1)
	addFile('View Errors in Log: %s' % (errorsfound), 'viewerrorlog', icon=ICONMAINT, themeit=THEME1)
	if errors > 0: addFile('View Last Error In Log', 'viewerrorlast', icon=ICONMAINT, themeit=THEME1)
	if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	addFile('Settings', 'settings', icon=ICONSETTINGS, themeit=THEME1)
	addFile('Force Update Text Files', 'forcetext', icon=ICONMAINT, themeit=THEME1)
	if DEVELOPER == 'true': addDir('Developer Menu', 'developer', icon=ICON, themeit=THEME1)
	setView('files', 'viewType')
def KodiVer():
	if KODIV >= 16.0 and KODIV <= 16.9:vername = 'Jarvis'
	elif KODIV >= 17.0 and KODIV <= 17.9:vername = 'Krypton'
	elif KODIV >= 18.0 and KODIV <= 18.9:vername = 'Leia'
	else: vername = "Unknown"
	return vername
def buildMenu():
	kodi_ver = KodiVer()
	bf = wiz.textCache(BUILDFILE)
	if bf == False:
		WORKINGURL = wiz.workingURL(BUILDFILE)
		addFile('%s Version: %s' % (MCNAME, KODIV), '', icon=ICONBUILDS, themeit=THEME3)
		addDir ('Save Data Menu'       ,'savedata', icon=ICONSAVE,     themeit=THEME3)
		if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
		addFile('Url for txt file not valid', '', icon=ICONBUILDS, themeit=THEME3)
		addFile('%s' % WORKINGURL, '', icon=ICONBUILDS, themeit=THEME3)
		return
	total, count15, count16, count17, count18, adultcount, hidden = wiz.buildCount()
	third = False; addin = []
	if THIRDPARTY == 'true':
		if not THIRD1NAME == '' and not THIRD1URL == '': third = True; addin.append('1')
		if not THIRD2NAME == '' and not THIRD2URL == '': third = True; addin.append('2')
		if not THIRD3NAME == '' and not THIRD3URL == '': third = True; addin.append('3')
	link  = bf.replace('\n','').replace('\r','').replace('\t','').replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"').replace('adult=""', 'adult="no"').replace('url2=""', 'url2="http://"').replace('url3=""', 'url3="http://"').replace('preview=""', 'preview="http://"')
	match = re.compile('name="(.+?)".+?ersion="(.+?)".+?rl="(.+?)".+?rl2="(.+?)".+?rl3="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)".+?review="(.+?)"').findall(link)
	if total == 1 and third == False:
		for name, version, url, url2, url3, gui, kodi, theme, icon, fanart, adult, description, preview in match:
			if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
			if not DEVELOPER == 'true' and wiz.strTest(name): continue
			viewBuild(match[0][0])
			return
	addFile('%s Version: %s' % (MCNAME, KODIV), '', icon=ICONBUILDS, themeit=THEME3)
	addDir ('Save Data Menu'       ,'savedata', icon=ICONSAVE,     themeit=THEME3)
	addDir ('[COLOR yellow]---[B][COLOR lime]Addon Packs [COLOR blue]/ [COLOR red]Fixes[/COLOR][/B][COLOR yellow]---[/COLOR]'        ,'viewpack',   icon=ICONMAINT,   themeit=THEME1)
	if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	if third == True:
		for item in addin:
			name = eval('THIRD%sNAME' % item)
			addDir ("[B]%s[/B]" % name, 'viewthirdparty', item, icon=ICONBUILDS, themeit=THEME3)
	if len(match) >= 1:
		if SEPERATE == 'true':
			for name, version, url, url2, url3, gui, kodi, theme, icon, fanart, adult, description, preview in match:
				if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
				if not DEVELOPER == 'true' and wiz.strTest(name): continue
				menu = createMenu('install', '', name)
				addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
		elif DEVELOPER == 'true':
			if count15 > 0:
				addFile('[B]Test builds[/B]', 'togglesetting',  'show15', themeit=THEME3)
				for name, version, url, url2, url3, gui, kodi, theme, icon, fanart, adult, description, preview in match:
					if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
					if not DEVELOPER == 'true' and wiz.strTest(name): continue
					kodiv = int(float(kodi))
					if kodiv <= 15:
						menu = createMenu('install', '', name)
						addDir(' %s (v%s)' % (name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
			if count18 > 0:
				state = '+' if SHOW18 == 'false' else '-'
				addFile('[B]%s Leia Builds(%s)[/B]' % (state, count18), 'togglesetting',  'show18', themeit=THEME3)
				if SHOW18 == 'true':
					for name, version, url, url2, url3, gui, kodi, theme, icon, fanart, adult, description, preview in match:
						if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
						if not DEVELOPER == 'true' and wiz.strTest(name): continue
						kodiv = int(float(kodi))
						if kodiv == 18:
							menu = createMenu('install', '', name)
							addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
			if count17 > 0:
				state = '+' if SHOW17 == 'false' else '-'
				addFile('[B]%s Krypton Builds(%s)[/B]' % (state, count17), 'togglesetting',  'show17', themeit=THEME3)
				if SHOW17 == 'true':
					for name, version, url, url2, url3, gui, kodi, theme, icon, fanart, adult, description, preview in match:
						if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
						if not DEVELOPER == 'true' and wiz.strTest(name): continue
						kodiv = int(float(kodi))
						if kodiv == 17:
							menu = createMenu('install', '', name)
							addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
			if count16 > 0:
				state = '+' if SHOW16 == 'false' else '-'
				addFile('[B]%s Jarvis Builds(%s)[/B]' % (state, count16), 'togglesetting',  'show16', themeit=THEME3)
				if SHOW16 == 'true':
					for name, version, url, url2, url3, gui, kodi, theme, icon, fanart, adult, description, preview in match:
						if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
						if not DEVELOPER == 'true' and wiz.strTest(name): continue
						kodiv = int(float(kodi))
						if kodiv == 16:
							menu = createMenu('install', '', name)
							addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
		else:
			if kodi_ver == "Leia":
				state = '+' if SHOW18 == 'false' else '-'
				addFile('[B]%s Leia Builds(%s)[/B]' % (state, count18), 'togglesetting',  'show18', themeit=THEME3)
				if SHOW18 == 'true':
					for name, version, url, url2, url3, gui, kodi, theme, icon, fanart, adult, description, preview in match:
						if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
						if not DEVELOPER == 'true' and wiz.strTest(name): continue
						kodiv = int(float(kodi))
						if kodiv == 18:
							menu = createMenu('install', '', name)
							addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
			elif kodi_ver == "Krypton":
				state = '+' if SHOW17 == 'false' else '-'
				addFile('[B]%s Krypton Builds(%s)[/B]' % (state, count17), 'togglesetting',  'show17', themeit=THEME3)
				if SHOW17 == 'true':
					for name, version, url, url2, url3, gui, kodi, theme, icon, fanart, adult, description, preview in match:
						if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
						if not DEVELOPER == 'true' and wiz.strTest(name): continue
						kodiv = int(float(kodi))
						if kodiv == 17:
							menu = createMenu('install', '', name)
							addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
			elif kodi_ver == "Jarvis":
				state = '+' if SHOW16 == 'false' else '-'
				addFile('[B]%s Jarvis Builds(%s)[/B]' % (state, count16), 'togglesetting',  'show16', themeit=THEME3)
				if SHOW16 == 'true':
					for name, version, url, url2, url3, gui, kodi, theme, icon, fanart, adult, description, preview in match:
						if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
						if not DEVELOPER == 'true' and wiz.strTest(name): continue
						kodiv = int(float(kodi))
						if kodiv == 16:
							menu = createMenu('install', '', name)
							addDir('[%s] %s (v%s)' % (float(kodi), name, version), 'viewbuild', name, description=description, fanart=fanart,icon=icon, menu=menu, themeit=THEME2)
	elif hidden > 0: 
		if adultcount > 0:
			addFile('There is currently only Adult builds', '', icon=ICONBUILDS, themeit=THEME3)
			addFile('Enable Show Adults in Addon Settings > Misc', '', icon=ICONBUILDS, themeit=THEME3)
		else:
			addFile('Currently No Builds Offered from %s' % ADDONTITLE, '', icon=ICONBUILDS, themeit=THEME3)
	else: addFile('Text file for builds not formated correctly.', '', icon=ICONBUILDS, themeit=THEME3)
	setView('files', 'viewType')
def viewBuild(name):
	bf = wiz.textCache(BUILDFILE)
	if bf == False:
		WORKINGURL = wiz.workingURL(BUILDFILE)
		addFile('Url for txt file not valid', '', themeit=THEME3)
		addFile('%s' % WORKINGURL, '', themeit=THEME3)
		return
	if wiz.checkBuild(name, 'version') == False: 
		addFile('Error reading the txt file.', '', themeit=THEME3)
		addFile('%s was not found in the builds list.' % name, '', themeit=THEME3)
		return
	link  = bf.replace('\n','').replace('\r','').replace('\t','').replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"').replace('url2=""', 'url2="http://"').replace('url3=""', 'url3="http://"').replace('preview=""', 'preview="http://"').replace('"https://"', 'preview="http://"')
	match = re.compile('name="%s".+?ersion="(.+?)".+?rl="(.+?)".+?rl2="(.+?)".+?rl3="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)".+?review="(.+?)"' % name).findall(link)
	for version, url, url2, url3, gui, kodi, themefile, icon, fanart, adult, description, preview in match:
		icon        = icon
		fanart      = fanart
		build       = '%s (v%s)' % (name, version)
		if BUILDNAME == name and version > BUILDVERSION:
			build = '%s [COLOR red][CURRENT v%s][/COLOR]' % (build, BUILDVERSION)
		addFile(build, '', description=description, fanart=fanart, icon=icon, themeit=THEME4)
		if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
		addDir ('Save Data Menu',       'savedata', icon=ICONSAVE,     themeit=THEME3)
		addFile('Build Information',    'buildinfo', name, description=description, fanart=fanart, icon=icon, themeit=THEME3)
		if not preview == "http://": addFile('View Video Preview', 'buildpreview', name, description=description, fanart=fanart, icon=icon, themeit=THEME3)
		temp1 = int(float(KODIV)); temp2 = int(float(kodi))
		if not temp1 == temp2: 
			if temp1 == 16 and temp2 <= 15: warning = False
			else: warning = True
		else: warning = False
		if warning == True:
			addFile('BUILD DESIGNED FOR KODI VERSION %s [COLOR yellow](INSTALLED: %s)[/COLOR]' % (str(kodi), str(KODIV)), '', fanart=fanart, icon=icon, themeit=THEME6)
		addFile(wiz.sep('INSTALL'), '', fanart=fanart, icon=icon, themeit=THEME3)
		addFile('Fresh Start then Install'   , 'install', name, 'fresh'  , description=description, fanart=fanart, icon=icon, themeit=THEME1)
		addFile('Standard Install', 'install', name, 'normal' , description=description, fanart=fanart, icon=icon, themeit=THEME1)
		if not gui == 'http://': addFile('Apply guiFix'    , 'install', name, 'gui'     , description=description, fanart=fanart, icon=icon, themeit=THEME1)
		if not themefile == 'http://':
			themecheck = wiz.textCache(themefile)
			if not themecheck == False:
				addFile(wiz.sep('THEMES'), '', fanart=fanart, icon=icon, themeit=THEME3)
				link  = themecheck.replace('\n','').replace('\r','').replace('\t','')
				match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
				for themename, themeurl, themeicon, themefanart, description in match:
					themeicon   = themeicon   if themeicon   == 'http://' else icon
					themefanart = themefanart if themefanart == 'http://' else fanart
					addFile(themename if not themename == BUILDTHEME else "[B]%s (Installed)[/B]" % themename, 'theme', name, themename, description=description, fanart=themefanart, icon=themeicon, themeit=THEME3)
	setView('files', 'viewType')
def viewThirdList(number):
	name = eval('THIRD%sNAME' % number)
	url  = eval('THIRD%sURL' % number)
	work = wiz.workingURL(url)
	if not work == True:
		addFile('Url for txt file not valid', '', icon=ICONBUILDS, themeit=THEME3)
		addFile('%s' % WORKINGURL, '', icon=ICONBUILDS, themeit=THEME3)
	else:
		type, buildslist = wiz.thirdParty(url)
		addFile("[B]%s[/B]" % name, '', themeit=THEME3)
		if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
		if type:
			for name, version, url, kodi, icon, fanart, adult, description in buildslist:
				if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
				addFile("[%s] %s v%s" % (kodi, name, version), 'installthird', name, url, icon=icon, fanart=fanart, description=description, themeit=THEME2)
		else:
			for name, url, icon, fanart, description in buildslist:
				addFile(name, 'installthird', name, url, icon=icon, fanart=fanart, description=description, themeit=THEME2)
def editThirdParty(number):
	name  = eval('THIRD%sNAME' % number)
	url   = eval('THIRD%sURL' % number)
	name2 = wiz.getKeyboard(name, 'Enter the Name of the Wizard')
	url2  = wiz.getKeyboard(url, 'Enter the URL of the Wizard Text')
	wiz.setS('wizard%sname' % number, name2)
	wiz.setS('wizard%surl' % number, url2)
def apkScraper(name=""):
	if name == 'kodi':
		kodiurl1 = 'http://mirrors.kodi.tv/releases/android/arm/'
		kodiurl2 = 'http://mirrors.kodi.tv/releases/android/arm/old/'
		url1 = wiz.openURL(kodiurl1).replace('\n', '').replace('\r', '').replace('\t', '')
		url2 = wiz.openURL(kodiurl2).replace('\n', '').replace('\r', '').replace('\t', '')
		x = 0
		match1 = re.compile('<tr><td><a href="(.+?)".+?>(.+?)</a></td><td>(.+?)</td><td>(.+?)</td></tr>').findall(url1)
		match2 = re.compile('<tr><td><a href="(.+?)".+?>(.+?)</a></td><td>(.+?)</td><td>(.+?)</td></tr>').findall(url2)
		addFile("Official Kodi Apk\'s", themeit=THEME1)
		rc = False
		for url, name, size, date in match1:
			if url in ['../', 'old/']: continue
			if not url.endswith('.apk'): continue
			if not url.find('_') == -1 and rc == True: continue
			try:
				tempname = name.split('-')
				if not url.find('_') == -1:
					rc = True
					name2, v2 = tempname[2].split('_')
				else: 
					name2 = tempname[2]
					v2 = ''
				title = "[COLOR %s]%s v%s%s %s[/COLOR] [COLOR %s]%s[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR1, tempname[0].title(), tempname[1], v2.upper(), name2, COLOR2, size.replace(' ', ''), COLOR1, date)
				download = urljoin(kodiurl1, url)
				addFile(title, 'apkinstall', "%s v%s%s %s" % (tempname[0].title(), tempname[1], v2.upper(), name2), download)
				x += 1
			except:
				wiz.log("Error on: %s" % name)
		for url, name, size, date in match2:
			if url in ['../', 'old/']: continue
			if not url.endswith('.apk'): continue
			if not url.find('_') == -1: continue
			try:
				tempname = name.split('-')
				title = "[COLOR %s]%s v%s %s[/COLOR] [COLOR %s]%s[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR1, tempname[0].title(), tempname[1], tempname[2], COLOR2, size.replace(' ', ''), COLOR1, date)
				download = urljoin(kodiurl2, url)
				addFile(title, 'apkinstall', "%s v%s %s" % (tempname[0].title(), tempname[1], tempname[2]), download)
				x += 1
			except:
				wiz.log("Error on: %s" % name)
		if x == 0: addFile("Error Kodi Scraper Is Currently Down.")
	elif name == 'spmc':
		spmcurl1 = 'https://github.com/koying/SPMC/releases'
		url1 = wiz.openURL(spmcurl1).replace('\n', '').replace('\r', '').replace('\t', '')
		x = 0
		match1 = re.compile('<div.+?lass="release-body.+?div class="release-header".+?a href=.+?>(.+?)</a>.+?ul class="release-downloads">(.+?)</ul>.+?/div>').findall(url1)
		addFile("Official SPMC Apk\'s", themeit=THEME1)
		for name, urls in match1:
			tempurl = ''
			match2 = re.compile('<li>.+?<a href="(.+?)" rel="nofollow">.+?<small class="text-gray float-right">(.+?)</small>.+?strong>(.+?)</strong>.+?</a>.+?</li>').findall(urls)
			for apkurl, apksize, apkname in match2:
				if apkname.find('armeabi') == -1: continue
				if apkname.find('launcher') > -1: continue
				tempurl = urljoin('https://github.com', apkurl)
				break
			if tempurl == '': continue
			try:
				name = "SPMC %s" % name
				title = "[COLOR %s]%s[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR1, name, COLOR2, apksize.replace(' ', ''))
				download = tempurl
				addFile(title, 'apkinstall', name, download)
				x += 1
			except Exception, e:
				wiz.log("Error on: %s / %s" % (name, str(e)))
		if x == 0: addFile("Error SPMC Scraper Is Currently Down.")
def apkMenu(name=None, url=None):
	if HIDESPACERS == 'No': addFile(wiz.sep('Apps from apkfiles.com'), '', themeit=THEME3)
	addDir ('App Lists'       ,'apkfiles', icon=ICONSAVE,     themeit=THEME1)
	if HIDESPACERS == 'No': addFile(wiz.sep('FTG Modded Apps'), '', themeit=THEME3)
	addDir ('App Lists'       ,'ftgmod', icon=ICONSAVE,     themeit=THEME1)
	setView('files', 'viewType')
	if url == None:
		if HIDESPACERS == 'No': addFile(wiz.sep('Official Kodi/SPMC'), '', themeit=THEME3)
		addDir ('Kodi Apk\'s', 'apkscrape', 'kodi', icon=ICONAPK, themeit=THEME1)
		addDir ('SPMC Apk\'s', 'apkscrape', 'spmc', icon=ICONAPK, themeit=THEME1)
		if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	if not APKFILE == 'http://':
		if url == None:
			TEMPAPKFILE = wiz.textCache(uservar.APKFILE)
			if TEMPAPKFILE == False: APKWORKING  = wiz.workingURL(uservar.APKFILE)
		else:
			TEMPAPKFILE = wiz.textCache(url)
			if TEMPAPKFILE == False: APKWORKING  = wiz.workingURL(url)
		if not TEMPAPKFILE == False:
			link = TEMPAPKFILE.replace('\n','').replace('\r','').replace('\t','')
			match = re.compile('name="(.+?)".+?ection="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
			if len(match) > 0:
				x = 0
				for aname, section, url, icon, fanart, adult, description in match:
					if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
					if section.lower() == 'yes':
						x += 1
						addDir ("[B]%s[/B]" % aname, 'apk', aname, url, description=description, icon=icon, fanart=fanart, themeit=THEME3)
					elif section.lower() == 'yes':
						x += 1
						addFile(aname, 'rominstall', aname, url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
					else:
						x += 1
						addFile(aname, 'apkinstall', aname, url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
					if x == 0:
						addFile("No addons added to this menu yet!", '', themeit=THEME2)
			else: wiz.log("[APK Menu] ERROR: Invalid Format.", xbmc.LOGERROR)
		else:
			wiz.log("[APK Menu] ERROR: URL for apk list not working.", xbmc.LOGERROR)
			addFile('Url for txt file not valid', '', themeit=THEME3)
			addFile('%s' % APKWORKING, '', themeit=THEME3)
		return
	else: wiz.log("[APK Menu] No APK list added.")
	setView('files', 'viewType')
def ftgmod():
	if not APKFILE == 'http://':
		APKWORKING = wiz.workingURL(APKFILE)
		if APKWORKING == True:
			link = wiz.openURL(APKFILE).replace('\n','').replace('\r','').replace('\t','')
			match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)"').findall(link)
			if len(match) > 0:
				for name, url, icon, fanart in match:
					#if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
					addDir(name, 'GetList', name, url, icon=icon, fanart=fanart, themeit=THEME1)
			else: wiz.log("[APK Menu] ERROR: Invalid Format.")
		else: 
			wiz.log("[APK Menu] ERROR: URL for apk list not working.", xbmc.LOGERROR)
			addFile('Url for txt file not valid', '', themeit=THEME3)
			addFile('%s' % APKWORKING, '', themeit=THEME3)
		return
	else: wiz.log("[APK Menu] No APK list added.")
def GetList(url):
	if not wiz.workingURL(url) == True: return False
	link = wiz.openURL(url).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)"').findall(link)
	if len(match) > 0:
		for name, url, icon, fanart in match:
			addFile(name, 'apkinstall', name, url, icon=icon, fanart=fanart, themeit=THEME1)
		else: wiz.log("[APK Menu] ERROR: Invalid Format.")
	else: wiz.log("[APK Menu] ERROR: URL for emu list not working.")
def apkfiles():
	if HIDESPACERS == 'No': addFile(wiz.sep('Apps from apkfiles.com'), '', themeit=THEME3)
	html= wiz.openURL('https://www.apkfiles.com/')
	match = re.compile('href="([^"]*)">Applications(.+?)</a>').findall(html)
	match2 = re.compile('href="([^"]*)">Games(.+?)</a>').findall(html)
	for url,count in match:
		addDir2('[COLOR blue]Android Apps[/COLOR]','https://www.apkfiles.com' +url,'apkgame',ICONAPK,FANART)
	for url,count in match2:
		addDir2('[COLOR blue]Android Games[/COLOR]','https://www.apkfiles.com' +url,'apkgame',ICONAPK,FANART)
	setView('movies', 'MAIN')
def apkshowMenu(url):
	if not wiz.workingURL(url) == True: return False
	link = wiz.openURL(url).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)"').findall(link)
	if len(match) > 0:
		for name, url, icon, fanart in match:
			addFile(name, 'apkinstall', name, url, icon=icon, fanart=fanart, themeit=THEME1)
		else: wiz.log("[APK Menu] ERROR: Invalid Format.")
	else: wiz.log("[APK Menu] ERROR: URL for emu list not working.")
def APKGAME(url):
	html=wiz.openURL(url)
	match = re.compile('<a href="([^"]*)" >(.+?)</a>').findall(html)
	for url,name in match:
		if '/cat' in url:
			addDir2((name).replace('&amp;',' - '),'https://www.apkfiles.com'+url,'select',ART+'APK.png',FANART)
def APKSELECT2(url):
	html=wiz.openURL(url)
	url1 = url
	if "page=" in str(url):
		url1 = url.split('?')[0]
	match = re.compile('<a href="([^"]*)".+?<img src="([^"]*)" class="file_list_icon".+?alt="([^"]*)"',re.DOTALL).findall(html)
	match2 = re.compile('class="[^"]*".+?ref="([^"]*)".+?yle=.+?</a>').findall(html)
	for url,img,name in match:
		if 'apk' in url:
			addDir2((name).replace('&#39;','').replace('&amp;',' - ').replace('&#174;:',': ').replace('&#174;',' '),'https://www.apkfiles.com'+url,'grab','http:'+img, FANART)
	if len(match2) > 1:
		match2 = str(match2[len(match2) - 1])
	addDir2('Next Page',url1+str(match2),'select',ART+'Next.png',FANART)
def APKGRAB(name,url):
	html=wiz.openURL(url)
	name=name
	match = re.compile('href="([^"]*)".+?lass="yellow_button".+?itle=').findall(html)
	for url in match:
		url = 'https://www.apkfiles.com'+url
		apkInstaller1(name,url)
###########################################################################
#################################RETRO PACKS###############################
def retromenu():
	MKDIRS()#if not os.path.exists(ROMLOC): os.makedirs(ROMLOC)
	if HIDESPACERS == 'No': addFile(wiz.sep('Emulators'), '', themeit=THEME3)
	if wiz.platform() == 'android' or DEVELOPER == 'true': addDir ('Emulator APKs'       ,'emumenu', icon=ICONSAVE,     themeit=THEME1)
	if wiz.platform() == 'windows' or DEVELOPER == 'true': addDir ('Emulator APPs'       ,'emumenu', icon=ICONSAVE,     themeit=THEME1)
	if HIDESPACERS == 'No': addFile(wiz.sep('Rom Packs'), '', themeit=THEME3)
	addDir ('Rom Pack Zips'       ,'rompackmenu', icon=ICONSAVE,     themeit=THEME1)
def emumenu():
	link = wiz.openURL(EMUAPKS).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)"').findall(link)
	if len(match) > 0:
		if wiz.platform() == 'android':
			for name, url, icon, fanart in match:
				addFile(name, 'apkinstall', name, url, icon=icon, fanart=fanart, themeit=THEME1)
		elif wiz.platform() == 'windows':
			DIALOG.ok(ADDONTITLE, "[COLOR yellow]Please go download RetroArch for PC[/COLOR]", " Goto http://tinyurl.com/RetroFTG for a full tutorial")
		elif wiz.platform() == 'linux':
			DIALOG.ok(ADDONTITLE, "[COLOR yellow]Please go download RetroArch for PC[/COLOR]", " Goto http://tinyurl.com/RetroFTG for a full tutorial")
def rompackmenu():
	link = wiz.openURL(ROMPACK).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)"').findall(link)
	if len(match) > 0:
		for name, url, icon, fanart in match:
			addFile(name, 'UNZIPROM', name, url, icon=icon, fanart=fanart, themeit=THEME1)
def UNZIPROM():
	myroms = xbmc.translatePath(BACKUPROMS)
	if myroms == '':
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Parece que voce nao tem um local de armazenamento das ROOMS" % COLOR2, "Voce gostaria de definir um agora?[/COLOR]", yeslabel="[COLOR green][B]Definir Local[/B][/COLOR]", nolabel="[COLOR red][B]Cancelar Download[/B][/COLOR]"):
			wiz.openS('rompath')
			myroms = wiz.getS('rompath')
			if myroms == '': return
	yes = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Tem certeza que voce gostaria de baixar e extrair? [COLOR %s]%s[/COLOR] para:" % (COLOR2, COLOR1, name), "[COLOR %s]%s[/COLOR]" % (COLOR1, myroms), yeslabel="[B][COLOR green]Download[/COLOR][/B]", nolabel="[B][COLOR red]Cancelar[/COLOR][/B]")
	if not yes: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]ERROR: Install Cancelled[/COLOR]' % COLOR2); return
	display = name
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Rom Installer: Invalid Rom Url![/COLOR]' % COLOR2); return
	DP.create(ADDONTITLE,'[COLOR %s][B]Baixando:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, display),'', 'Por favor aguarde')
	lib=os.path.join(PACKAGES, "%s.zip" % name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', ''))
	try: os.remove(lib)
	except: pass
	downloader.download(url, lib, DP)
	xbmc.sleep(100)
	percent, errors, error = extract.all(lib,myroms,DP, title=display)
	try: os.remove(lib)
	except: pass
	wiz.LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Rom Pack Installed[/COLOR]' % COLOR2)
	DP.close()
def MKDIRS():
	if not os.path.exists(ROMLOC): os.makedirs(ROMLOC)
		
####################################################################################
def buildVideo(name):
	if wiz.workingURL(BUILDFILE) == True:
		videofile = wiz.checkBuild(name, 'preview')
		wiz.FTGlog('Name %s'%name)
		wiz.FTGlog('URL %s'%videofile)
		if videofile and not videofile == 'http://': playVideoB(videofile)
		else: wiz.log("[%s]Unable to find url for video preview" % name)
	else: wiz.log("Build text file not working: %s" % WORKINGURL)


def playVideo(url):
	if 'watch?v=' in url:
		a, b = url.split('?')
		find = b.split('&')
		for item in find:
			if item.startswith('v='):
				url = item[2:]
				break
			else: continue
	elif 'embed' in url or 'youtu.be' in url:
		a = url.split('/')
		if len(a[-1]) > 5:
			url = a[-1]
		elif len(a[-2]) > 5:
			url = a[-2]
	wiz.log("YouTube URL: %s" % url)
	if wiz.getCond('System.HasAddon(plugin.video.youtube)') == 1:
		url = 'plugin://plugin.video.youtube/play/?video_id=%s' % url
		xbmc.Player().play(url)
	xbmc.sleep(2000)
	if xbmc.Player().isPlayingVideo() == 0:
		 yt.PlayVideo(url)
####################################################################################
def addonMenu(name=None, url=None):
	if not ADDONFILE == 'http://':
		if url == None:
			TEMPADDONFILE = wiz.textCache(uservar.ADDONFILE)
			if TEMPADDONFILE == False: ADDONWORKING  = wiz.workingURL(uservar.ADDONFILE)
		else:
			TEMPADDONFILE = wiz.textCache(url)
			if TEMPADDONFILE == False: ADDONWORKING  = wiz.workingURL(url)
		if not TEMPADDONFILE == False:
			link = TEMPADDONFILE.replace('\n','').replace('\r','').replace('\t','').replace('repository=""', 'repository="none"').replace('repositoryurl=""', 'repositoryurl="http://"').replace('repositoryxml=""', 'repositoryxml="http://"')
			match = re.compile('name="(.+?)".+?lugin="(.+?)".+?rl="(.+?)".+?epository="(.+?)".+?epositoryxml="(.+?)".+?epositoryurl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
			if len(match) > 0:
				x = 0
				for aname, plugin, aurl, repository, repositoryxml, repositoryurl, icon, fanart, adult, description in match:
					if plugin.lower() == 'section':
						addonMenu(name, url)
					elif plugin.lower() == 'skin':
						skinInstaller(name, url)
					elif plugin.lower() == 'pack':
						packInstaller(name, url)
					else:
						if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
						try:
							add    = xbmcaddon.Addon(id=plugin).getAddonInfo('path')
							if os.path.exists(add):
								aname   = "[COLOR green][Installed][/COLOR] %s" % aname
						except:
							pass
						addonInstaller(plugin, url)
					if x < 1:
						wiz.LogNotify("[COLOR %s]No Addons[/COLOR]" % COLOR1)
			else: 
				addFile('Text File not formated correctly!', '', themeit=THEME3)
				wiz.log("[Addon Menu] ERROR: Invalid Format.")
		else: 
			wiz.log("[Addon Menu] ERROR: URL for Addon list not working.")
			addFile('Url for txt file not valid', '', themeit=THEME3)
			addFile('%s' % ADDONWORKING, '', themeit=THEME3)
	else: wiz.log("[Addon Menu] No Addon list added.")
	#else: 
	#	wiz.LogNotify("[COLOR %s]error[/COLOR]" % COLOR1)

def packInstaller(name, url):
	if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s:[/COLOR] [COLOR %s]URL do arquivo ZIP invalido![/COLOR]' % (COLOR1, name, COLOR2)); return
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	DP.create(ADDONTITLE,'[COLOR %s][B]Baixando:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '', '[COLOR %s]Por favor, agaurde...[/COLOR]' % COLOR2)
	urlsplits = url.split('/')
	lib = xbmc.makeLegalFilename(os.path.join(PACKAGES, urlsplits[-1]))
	try: os.remove(lib)
	except: pass
	downloader.download(url, lib, DP)
	title = '[COLOR %s][B]Instalando:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
	DP.update(0, title,'', '[COLOR %s]Por favor, aguarde...[/COLOR]' % COLOR2)
	percent, errors, error = extract.all(lib,ADDONS,DP, title=title)
	installed = grabAddons(lib)
	if KODIV >= 17: wiz.addonDatabase(installed, 1, True)
	DP.close()
	wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s: Installed![/COLOR]' % (COLOR2, name))
	wiz.ebi('UpdateAddonRepos()')
	wiz.ebi('UpdateLocalAddons()')
	wiz.refresh()
def skinInstaller(name, url):
	if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s:[/COLOR] [COLOR %s]Invalid Zip Url![/COLOR]' % (COLOR1, name, COLOR2)); return
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	DP.create(ADDONTITLE,'[COLOR %s][B]Baixando:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '', '[COLOR %s]Por favor, aguarde..[/COLOR]' % COLOR2)
	urlsplits = url.split('/')
	lib = xbmc.makeLegalFilename(os.path.join(PACKAGES, urlsplits[-1]))
	try: os.remove(lib)
	except: pass
	downloader.download(url, lib, DP)
	title = '[COLOR %s][B]Instalando:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
	DP.update(0, title,'', '[COLOR %s]Por favor, aguarde...[/COLOR]' % COLOR2)
	percent, errors, error = extract.all(lib,HOME,DP, title=title)
	installed = grabAddons(lib)
	if KODIV >= 17: wiz.addonDatabase(installed, 1, True)
	DP.close()
	wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s: Installed![/COLOR]' % (COLOR2, name))
	wiz.ebi('UpdateAddonRepos()')
	wiz.ebi('UpdateLocalAddons()')
	for item in installed:
		if item.startswith('skin.') == True and not item == 'skin.shortcuts':
			if not BUILDNAME == '' and DEFAULTIGNORE == 'true': wiz.setS('defaultskinignore', 'true')
			wiz.swapSkins(item, 'Skin Installer')
	wiz.refresh()
def addonInstaller(plugin, url):
	if not ADDONFILE == 'http://' or '':
		url = ADDONFILE
		ADDONWORKING = wiz.workingURL(url)
		if ADDONWORKING == True:
			link = wiz.textCache(url).replace('\n','').replace('\r','').replace('\t','').replace('repository=""', 'repository="none"').replace('repositoryurl=""', 'repositoryurl="http://"').replace('repositoryxml=""', 'repositoryxml="http://"')
			match = re.compile('name="(.+?)".+?lugin="%s".+?rl="(.+?)".+?epository="(.+?)".+?epositoryxml="(.+?)".+?epositoryurl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"' % plugin).findall(link)
			if len(match) > 0:
				for name, url, repository, repositoryxml, repositoryurl, icon, fanart, adult, description in match:
					if os.path.exists(os.path.join(ADDONS, plugin)):
						do        = ['Iiniciar ADDON', 'Remover ADDON']
						selected = DIALOG.select("[COLOR %s]Addons ja esta instalado, o que voce gostaria de fazer?[/COLOR]" % COLOR2, do)
						if selected == 0:
							wiz.ebi('RunAddon(%s)' % plugin)
							xbmc.sleep(500)
							return True
						elif selected == 1:
							wiz.cleanHouse(os.path.join(ADDONS, plugin))
							try: wiz.removeFolder(os.path.join(ADDONS, plugin))
							except: pass
							if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to remove the addon_data for:" % COLOR2, "[COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR1, plugin), yeslabel="[B][COLOR green]Yes Remove[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"):
								removeAddonData(plugin)
							wiz.refresh()
							return True
						else:
							return False
					repo = os.path.join(ADDONS, repository)
					if not repository.lower() == 'none' and not os.path.exists(repo):
						wiz.log("Repository not installed, installing it")
						if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Would you like to install the repository for [COLOR %s]%s[/COLOR]:" % (COLOR2, COLOR1, plugin), "[COLOR %s]%s[/COLOR]?[/COLOR]" % (COLOR1, repository), yeslabel="[B][COLOR green]Yes Install[/COLOR][/B]", nolabel="[B][COLOR red]No Skip[/COLOR][/B]"): 
							ver = wiz.parseDOM(wiz.openURL(repositoryxml), 'addon', ret='version', attrs = {'id': repository})
							if len(ver) > 0:
								repozip = '%s%s-%s.zip' % (repositoryurl, repository, ver[0])
								wiz.log(repozip)
								if KODIV >= 17: wiz.addonDatabase(repository, 1)
								installAddon(repository, repozip)
								wiz.ebi('UpdateAddonRepos()')
								#wiz.ebi('UpdateLocalAddons()')
								wiz.log("Installing Addon from Kodi")
								install = installFromKodi(plugin)
								wiz.log("Install from Kodi: %s" % install)
								if install:
									wiz.refresh()
									return True
							else:
								wiz.log("[Addon Installer] Repository not installed: Unable to grab url! (%s)" % repository)
						else: wiz.log("[Addon Installer] Repository for %s not installed: %s" % (plugin, repository))
					elif repository.lower() == 'none':
						wiz.log("No repository, installing addon")
						pluginid = plugin
						zipurl = url
						installAddon(plugin, url)
						wiz.refresh()
						return True
					else:
						wiz.log("Repository installed, installing addon")
						install = installFromKodi(plugin, False)
						if install:
							wiz.refresh()
							return True
					if os.path.exists(os.path.join(ADDONS, plugin)): return True
					ver2 = wiz.parseDOM(wiz.openURL(repositoryxml), 'addon', ret='version', attrs = {'id': plugin})
					if len(ver2) > 0:
						url = "%s%s-%s.zip" % (url, plugin, ver2[0])
						wiz.log(str(url))
						if KODIV >= 17: wiz.addonDatabase(plugin, 1)
						installAddon(plugin, url)
						wiz.refresh()
					else: 
						wiz.log("no match"); return False
			else: wiz.log("[Addon Installer] Invalid Format")
		else: wiz.log("[Addon Installer] Text File: %s" % ADDONWORKING)
	else: wiz.log("[Addon Installer] Not Enabled.")
def installFromKodi(plugin, over=True):
	if over == True:
		xbmc.sleep(2000)
	#wiz.ebi('InstallAddon(%s)' % plugin)
	wiz.ebi('RunPlugin(plugin://%s)' % plugin)
	if not wiz.whileWindow('yesnodialog'):
		return False
	xbmc.sleep(500)
	if wiz.whileWindow('okdialog'):
		return False
	wiz.whileWindow('progressdialog')
	if os.path.exists(os.path.join(ADDONS, plugin)): return True
	else: return False
def installAddon(name, url):
	if not wiz.workingURL(url) == True: wiz.LogNotify("[COLOR %s]Addon Installer[/COLOR]" % COLOR1, '[COLOR %s]%s:[/COLOR] [COLOR %s]Invalid Zip Url![/COLOR]' % (COLOR1, name, COLOR2)); return
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	DP.create(ADDONTITLE,'[COLOR %s][B]Baixando:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name), '', '[COLOR %s]Por favor, aguarde..[/COLOR]' % COLOR2)
	urlsplits = url.split('/')
	lib=os.path.join(PACKAGES, urlsplits[-1])
	try: os.remove(lib)
	except: pass
	downloader.download(url, lib, DP)
	title = '[COLOR %s][B]Instalando:[/B][/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, name)
	DP.update(0, title,'', '[COLOR %s]Por favor, aguarde...[/COLOR]' % COLOR2)
	percent, errors, error = extract.all(lib,ADDONS,DP, title=title)
	DP.update(0, title,'', '[COLOR %s]Instalando dependencias[/COLOR]' % COLOR2)
	installed(name)
	installlist = grabAddons(lib)
	wiz.log(str(installlist))
	if KODIV >= 17: wiz.addonDatabase(installlist, 1, True)
	installDep(name, DP)
	DP.close()
	wiz.ebi('UpdateAddonRepos()')
	wiz.ebi('UpdateLocalAddons()')
	wiz.refresh()
	for item in installlist:
		if item.startswith('skin.') == True and not item == 'skin.shortcuts':
			if not BUILDNAME == '' and DEFAULTIGNORE == 'true': wiz.setS('defaultskinignore', 'true')
			wiz.swapSkins(item, 'Skin Installer')
def installDep(name, DP=None):
	dep=os.path.join(ADDONS,name,'addon.xml')
	if os.path.exists(dep):
		source = open(dep,mode='r'); link = source.read(); source.close(); 
		match  = wiz.parseDOM(link, 'import', ret='addon')
		for depends in match:
			if not 'xbmc.python' in depends:
				if not DP == None:
					DP.update(0, '', '[COLOR %s]%s[/COLOR]' % (COLOR1, depends))
				try:
					add   = xbmcaddon.Addon(id=depends)
					name2 = add.getAddonInfo('name')
				except:
					wiz.createTemp(depends)
					if KODIV >= 17: wiz.addonDatabase(depends, 1)
def installed(addon):
	url = os.path.join(ADDONS,addon,'addon.xml')
	if os.path.exists(url):
		try:
			list  = open(url,mode='r'); g = list.read(); list.close()
			name = wiz.parseDOM(g, 'addon', ret='name', attrs = {'id': addon})
			icon  = os.path.join(ADDONS,addon,'icon.png')
			wiz.LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, name[0]), '[COLOR %s]Addon Enabled[/COLOR]' % COLOR2, '2000', icon)
		except: pass
def youtubeMenu(name=None, url=None):
	if not YOUTUBEFILE == 'http://':
		if url == None:
			TEMPYOUTUBEFILE = wiz.textCache(uservar.YOUTUBEFILE)
			if TEMPYOUTUBEFILE == False: YOUTUBEWORKING  = wiz.workingURL(uservar.YOUTUBEFILE)
		else:
			TEMPYOUTUBEFILE = wiz.textCache(url)
			if TEMPYOUTUBEFILE == False: YOUTUBEWORKING  = wiz.workingURL(url)
		if not TEMPYOUTUBEFILE == False:
			link = TEMPYOUTUBEFILE.replace('\n','').replace('\r','').replace('\t','')
			match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
			if len(match) > 0:
				for name, url, icon, fanart, description in match:
					addFile(name, 'viewVideo', url=url, description=description, icon=icon, fanart=fanart, themeit=THEME2)
			else: wiz.log("[YouTube Menu] ERROR: Invalid Format.")
		else: 
			wiz.log("[YouTube Menu] ERROR: URL for YouTube list not working.")
			addFile('Url for txt file not valid', '', themeit=THEME3)
			addFile('%s' % YOUTUBEWORKING, '', themeit=THEME3)
	else: wiz.log("[YouTube Menu] No YouTube list added.")
	setView('files', 'viewType')
def maintMenu(view=None):
	on = '[B][COLOR green]ON[/COLOR][/B]'; off = '[B][COLOR red]OFF[/COLOR][/B]'
	if wiz.Grab_Log(True) == False: kodilog = 0
	else: kodilog = errorChecking(wiz.Grab_Log(True), True)
	if wiz.Grab_Log(True, True) == False: kodioldlog = 0
	else: kodioldlog = errorChecking(wiz.Grab_Log(True,True), True)
	errorsinlog = int(kodilog) + int(kodioldlog)
	wizlogsize = ': [COLOR red]Not Found[/COLOR]' if not os.path.exists(WIZLOG) else ": [COLOR green]%s[/COLOR]" % wiz.convertSize(os.path.getsize(WIZLOG))
	sizepack   = wiz.getSize(PACKAGES)
	sizethumb  = wiz.getSize(THUMBS)
	sizecache  = wiz.getCacheSize()
	totalsize  = sizepack+sizethumb+sizecache
	addFile('Total Clean Up: [COLOR green][B]%s[/B][/COLOR]' % wiz.convertSize(totalsize)  ,'fullclean',       icon=ICONMAINT, themeit=THEME3)
	addFile('Clear Cache: [COLOR green][B]%s[/B][/COLOR]' % wiz.convertSize(sizecache)     ,'clearcache',      icon=ICONMAINT, themeit=THEME3)
	addFile('Limpando Temporarios: [COLOR green][B]%s[/B][/COLOR]' % wiz.convertSize(sizepack)   ,'clearpackages',   icon=ICONMAINT, themeit=THEME3)
	addFile('Clear Thumbnails: [COLOR green][B]%s[/B][/COLOR]' % wiz.convertSize(sizethumb),'clearthumb',      icon=ICONMAINT, themeit=THEME3)
	addFile('Clear Old Thumbnails', 'oldThumbs',      icon=ICONMAINT, themeit=THEME3)
	addFile('Clear Crash Logs',     'clearcrash',      icon=ICONMAINT, themeit=THEME3)
	addFile('Purge Databases',      'purgedb',         icon=ICONMAINT, themeit=THEME3)
	addDir ('[B]Back up/Restore[/B]'     , 'backup',   icon=ICONMAINT, themeit=THEME1)
	addDir ('[B]Advanced Settings Tool[/B]'     , 'autoconfig',   icon=ICONMAINT, themeit=THEME1)
	addDir ('[B]Addon Tools[/B]', 'addon',  icon=ICONMAINT, themeit=THEME1)
	addDir ('[B]Misc Maintenance[/B]'     , 'misc',   icon=ICONMAINT, themeit=THEME1)
	addDir ('[B]System Tweaks/Fixes[/B]', 'tweaks', icon=ICONMAINT, themeit=THEME1)
	if HIDESPACERS == 'No': addFile(wiz.sep(), '', themeit=THEME3)
	addFile('!!!>>Fresh Start<<!!!',          'freshstart',      icon=ICONMAINT, themeit=THEME6)
def backup():
		addFile('Back Up Location: [COLOR %s]%s[/COLOR]' % (COLOR2, MYBUILDS),'settings', 'Maintenance', icon=ICONMAINT, themeit=THEME3)
		if HIDESPACERS == 'No': addFile(wiz.sep('Backup'), '', themeit=THEME1)
		addFile('[Back Up]: Build',               'backupbuild',     icon=ICONMAINT,   themeit=THEME3)
		addFile('[Back Up]: GuiFix',              'backupgui',       icon=ICONMAINT,   themeit=THEME3)
		addFile('[Back Up]: Theme',               'backuptheme',     icon=ICONMAINT,   themeit=THEME3)
		addFile('[Back Up]: Addon Pack',          'backupaddonpack', icon=ICONMAINT,   themeit=THEME3)
		addFile('[Back Up]: Addon_data',          'backupaddon',     icon=ICONMAINT,   themeit=THEME3)
		if HIDESPACERS == 'No': addFile(wiz.sep('Restore'), '', themeit=THEME1)
		addFile('[Restore]: Local Build',         'restorezip',      icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restore]: Local GuiFix',        'restoregui',      icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restore]: Local Addon_data',    'restoreaddon',    icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restore]: External Build',      'restoreextzip',   icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restore]: External GuiFix',     'restoreextgui',   icon=ICONMAINT,   themeit=THEME3)
		addFile('[Restore]: External Addon_data', 'restoreextaddon', icon=ICONMAINT,   themeit=THEME3)
		if HIDESPACERS == 'No': addFile(wiz.sep('Delete All Backups'), '', themeit=THEME1)
		addFile('Clean Up Back Up Folder',        'clearbackup',     icon=ICONMAINT,   themeit=THEME3)
def addon():
		addFile('Remove Addons',                  'removeaddons',    icon=ICONMAINT, themeit=THEME3)
		addDir ('Remove Addon Data',              'removeaddondata', icon=ICONMAINT, themeit=THEME3)
		addDir ('Enable/Disable Addons',          'enableaddons',    icon=ICONMAINT, themeit=THEME3)
		ad