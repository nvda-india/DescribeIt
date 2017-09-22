# DescribeIt: An Add-on for nvda that provides description of web images using Microsoft cognitive API 
#Copyright (C) 2016-2017 Assistech Lab IIT Delhi, Manshul Belani, Dinesh Kaushal
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import globalPluginHandler
import wx
import gui
import globalVars
import configobj
import addonHandler
from imageDescription import imageDescription

addonHandler.initTranslation()

class addProxyDetailsDialog(wx.Dialog):
    def __init__(self, document):
		self.filename="userDetails.ini"
		self.config = configobj.ConfigObj(os.path.join(globalVars.appArgs.configPath, "addons\DescribeIt\globalPlugins\DescribeIt\%s" % self.filename))
		self.document = document
		# Translators: The title of the Image Description dialog.
		super(addProxyDetailsDialog, self).__init__(gui.mainFrame, wx.ID_ANY, _("Proxy Details"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		contentsSizer = wx.BoxSizer(wx.VERTICAL)
		bHelper = gui.guiHelper.ButtonHelper(wx.HORIZONTAL)
		
		labelText = _("Proxy IP")
		labeledCtrl = gui.guiHelper.LabeledControlHelper(self, labelText, wx.TextCtrl)
		self.labelIPEdit = labeledCtrl.control
		contentsSizer.Add(labeledCtrl.sizer)
		contentsSizer.AddSpacer(gui.guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
 		
		labelText = _("Proxy Port")
		labeledCtrl = gui.guiHelper.LabeledControlHelper(self, labelText, wx.TextCtrl)
		self.labelPortEdit = labeledCtrl.control
		contentsSizer.Add(labeledCtrl.sizer)
		contentsSizer.AddSpacer(gui.guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		if self.config:
	 		try:
				self.labelIPEdit.SetValue(self.config["Proxy IP"])
 				self.labelPortEdit.SetValue(self.config["Proxy Port"])
	 		except:
	 			pass
		
		bHelper.addButton(self, id=wx.ID_OK)
		bHelper.addButton(self, id=wx.ID_CANCEL)
		
		contentsSizer.Add(bHelper.sizer, flag=wx.ALIGN_RIGHT)
		mainSizer.Add(contentsSizer, border=gui.guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
        
class addAPIKeyDialog(wx.Dialog):
    def __init__(self, document):
		self.filename="userDetails.ini"
		self.config = configobj.ConfigObj(os.path.join(globalVars.appArgs.configPath, "addons\DescribeIt\globalPlugins\DescribeIt\%s" % self.filename))
		self.document = document
		# Translators: The title of the Image Description dialog.
		super(addAPIKeyDialog, self).__init__(gui.mainFrame, wx.ID_ANY, _("API key details"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		contentsSizer = wx.BoxSizer(wx.VERTICAL)
		bHelper = gui.guiHelper.ButtonHelper(wx.HORIZONTAL)
		
		labelText = _("API Subscription Key")
		labeledCtrl = gui.guiHelper.LabeledControlHelper(self, labelText, wx.TextCtrl)
		self.labelKeyEdit = labeledCtrl.control
		contentsSizer.Add(labeledCtrl.sizer)
		contentsSizer.AddSpacer(gui.guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		if self.config:
	 		try:
	 			self.labelKeyEdit.SetValue(self.config["Key"])
	 		except:
	 			pass

		bHelper.addButton(self, id=wx.ID_OK)
		bHelper.addButton(self, id=wx.ID_CANCEL)
		
		contentsSizer.Add(bHelper.sizer, flag=wx.ALIGN_RIGHT)
		mainSizer.Add(contentsSizer, border=gui.guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
        
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    
    def prefAddProxy(self,arg):
        d=addProxyDetailsDialog(None)
        def callback(result):
            if result == wx.ID_OK:
                self.config["Proxy IP"] = unicode(d.labelIPEdit.GetValue())
                self.config["Proxy Port"]=unicode(d.labelPortEdit.GetValue())
                self.config.write()
        gui.runScriptModalDialog(d, callback)
        
    def prefAddAPIKey(self,arg):
        d=addAPIKeyDialog(None)
        def callback(result):
            if result == wx.ID_OK:
                self.config["Key"]=unicode(d.labelKeyEdit.GetValue())
                self.config.write()
        gui.runScriptModalDialog(d, callback)
        
    def __init__(self):
        super(GlobalPlugin,self).__init__()
        self.filename="userDetails.ini"
        self.config = configobj.ConfigObj(os.path.join(globalVars.appArgs.configPath, "addons\DescribeIt\globalPlugins\DescribeIt\%s" % self.filename))
        systray = gui.mainFrame.sysTrayIcon
        self.menu = wx.Menu()
        systray.Bind(wx.EVT_MENU,
                     self.prefAddAPIKey,
                     self.menu.Append(wx.ID_ANY,
                                      ##Translators: context menu entry for API Subscription key
                                      _("Add API &Key"),
                                      ##Translators: help for context menu entry for API Subscription key
                                      _("Add API Subscription Key")))
        ## Translators: The menu item in the NVDA Context Menu
        systray.Bind(wx.EVT_MENU,
                     self.prefAddProxy,
                     self.menu.Append(wx.ID_ANY,
                                      ##Translators: context menu entry for Proxy details
                                      _("Add &Proxy Details"),
                                      ## Translators: help for context menu entry for proxy details
                                      _("Add Proxy IP and port")))
        systray.menu.InsertMenu(2,wx.ID_ANY,  _("A&ssistech IIT Delhi"), self.menu)
        
    def chooseNVDAObjectOverlayClasses(self,obj,clsList):
        if obj.windowClassName in (u"Internet Explorer_Server",u"MozillaWindowClass",u"Chrome_RenderWidgetHostHWND"):
            clsList.insert(0, imageDescription)