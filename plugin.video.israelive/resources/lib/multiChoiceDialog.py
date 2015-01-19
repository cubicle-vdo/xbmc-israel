import os
import xbmcgui
import xbmcaddon
import pyxbmct.addonwindow as pyxbmct

AddonID = "plugin.video.israelive"
_addon = xbmcaddon.Addon(AddonID)
_path = _addon.getAddonInfo("path")
_check_icon = os.path.join(_path, "check.png") # Don't decode _path to utf-8!!!


class MultiChoiceDialog(pyxbmct.AddonDialogWindow):
	def __init__(self, title="", items=[]):
		super(MultiChoiceDialog, self).__init__(title)
		self.setGeometry(450, 600, 10, 4)
		self.selected = []
		self.set_controls()
		self.connect_controls()
		self.listing.addItems(items)
		self.set_navigation()

	def set_controls(self):
		self.listing = pyxbmct.List(_imageWidth=15)
		self.placeControl(self.listing, 0, 0, rowspan=9, columnspan=4)
		self.ok_button = pyxbmct.Button("OK")
		self.placeControl(self.ok_button, 9, 1)
		self.cancel_button = pyxbmct.Button("Cancel")
		self.placeControl(self.cancel_button, 9, 2)

	def connect_controls(self):
		self.connect(self.listing, self.check_uncheck)
		self.connect(self.ok_button, self.ok)
		self.connect(self.cancel_button, self.close)

	def set_navigation(self):
		self.listing.controlUp(self.ok_button)
		self.listing.controlDown(self.ok_button)
		self.ok_button.setNavigation(self.listing, self.listing, self.cancel_button, self.cancel_button)
		self.cancel_button.setNavigation(self.listing, self.listing, self.ok_button, self.ok_button)
		self.setFocus(self.listing)

	def check_uncheck(self):
		list_item = self.listing.getSelectedItem()
		if list_item.getLabel2() == "checked":
			list_item.setIconImage("")
			list_item.setLabel2("unchecked")
		else:
			list_item.setIconImage(_check_icon)
			list_item.setLabel2("checked")

	def ok(self):
		for index in range(self.listing.size()):
			if self.listing.getListItem(index).getLabel2() == "checked":
				self.selected.append(index)
		super(MultiChoiceDialog, self).close()

	def close(self):
		self.selected = []
		super(MultiChoiceDialog, self).close()
