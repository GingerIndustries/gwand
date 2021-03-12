import kano_wand.kano_wand as kano_wand
from time import sleep
import gi
import threading

#<div>Icons made by <a href="https://www.flaticon.com/authors/those-icons" title="Those Icons">Those Icons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GdkPixbuf, GLib

class SimpleThread(threading.Thread):
        def __init__(self, target, daemon = True, startOnInit = True, **args):
                super().__init__(target = target, daemon = daemon, **args)
                if startOnInit:
                        self.start()
        def start(self):
                threading.Thread.start(self)
                while super().is_alive():
                        Gtk.main_iteration()
                        #print(str(super().is_alive()) + super().name)

class ConnectionWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title = 'Connect', icon_name = "network-wireless-symbolic", default_width = 200, default_height = 300)
		self.connect('delete-event', lambda w, e: w.hide() or True)
		self.isScanning = False
		self.shop = kano_wand.Shop()
		self.wands = []
		
		self.wandList = Gtk.ListBox()
		self.wandListFrame = Gtk.ScrolledWindow(propagate_natural_height = False, hexpand = True, margin = 5, hexpand_set = True, min_content_height = 300)
		self.add(self.wandList)
		self.refreshButtonIcon = Gtk.Image.new_from_icon_name("view-refresh", Gtk.IconSize.DND)
		self.refreshButtonSpinner = Gtk.Spinner()
		self.refreshButtonSpinner.set_size_request(32, 32)
		self.refreshButtonSpinner.start()
		self.refreshButtonSpinner.show()
		self.refreshButton = Gtk.Button()
		self.refreshButton.add(self.refreshButtonIcon)
		self.refreshButton.props.halign = Gtk.Align.CENTER
		self.refreshButton.set_size_request(300, -1)
		self.refreshButton.connect("clicked", self.scanForDevices)
		self.wandList.insert(self.refreshButton, -1)
		self.refreshButton.get_parent().props.selectable = False
		
		GLib.timeout_add_seconds(2, self.rssi)
		
	def rssi(self):
		if self.refreshButton.props.sensitive:
			wands = self.shop.scan()
			#print(wands)
			for item in wands:
				print(item.name, item._dev.rssi)
				
				self.__icon = None
				def __f(row):
					if row.get_child() != self.refreshButton:
						if row.get_child().get_children()[0].get_children()[0].get_text() == item.name:
							self.__icon = row.get_child().get_children()[1]
				self.wandList.foreach(__f)
				#print(self.__icon)
				if self.__icon:
					rssi = item._dev.rssi
					if rssi >= -60:
						self.__icon.set_from_icon_name("network-cellular-signal-excellent-symbolic", Gtk.IconSize.DND)
					elif rssi >= -70:
						self.__icon.set_from_icon_name("network-cellular-signal-good-symbolic", Gtk.IconSize.DND)
					elif rssi >= -75:
						self.__icon.set_from_icon_name("network-cellular-signal-ok-symbolic", Gtk.IconSize.DND)
					elif rssi >= -80:
						self.__icon.set_from_icon_name("network-cellular-signal-weak-symbolic", Gtk.IconSize.DND)
					else:
						self.__icon.set_from_icon_name("network-cellular-signal-none-symbolic", Gtk.IconSize.DND)
		return True
	
	def _removeWandEntry(self, item):
		if item.get_child() != self.refreshButton:
			self.wandList.remove(item)
			item.destroy()
	def scanForDevices(self, button=None):
		self.refreshButton.set_sensitive(False)
		self.refreshButton.remove(self.refreshButtonIcon)
		self.refreshButton.add(self.refreshButtonSpinner)
		self.wandList.foreach(self._removeWandEntry)
		SimpleThread(self._scan)
		for item in self.wands:
			_box = Gtk.Box()
			_textBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
			_icon = Gtk.Image.new_from_icon_name("network-cellular-acquiring-symbolic", Gtk.IconSize.DIALOG)
			_nameLabel = Gtk.Label(label = item.name)
			_addrLabel = Gtk.Label(label = "<span foreground = \"#999999\" size = \"small\"> " + str(item._dev.addr) + "</span>" , use_markup = True)
			_textBox.add(_nameLabel)
			_textBox.add(_addrLabel)
			_textBox.props.halign = Gtk.Align.START
			_box.pack_start(_textBox, True, False, 25)
			_box.pack_end(_icon, False, False, 0)
			self.wandList.insert(_box, 0)
			
		self.wandList.show_all()
		self.refreshButton.remove(self.refreshButtonSpinner)
		self.refreshButton.add(self.refreshButtonIcon)
		self.refreshButton.set_sensitive(True)
	def _scan(self):
		self.wands = self.shop.scan(timeout=3)
	
	def show(self):
		self.set_position(Gtk.WindowPosition.CENTER)
		self.show_all()
	
class Window(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title = 'gwand', icon = GdkPixbuf.Pixbuf.new_from_file("magic-wand.png"), default_width = 1250, default_height = 750)
		self.wand = None
		self.wands = []
		self.connectWindow = ConnectionWindow()
		self.connect("destroy", Gtk.main_quit)
		
		self.mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
		self.add(self.mainBox)
		
		self.connectMenu = Gtk.Menu()
		self.dialogOption = Gtk.MenuItem(label = "Open Connect Dialog")
		self.recentOption = Gtk.MenuItem(label = "Recent...")
		self.directOption = Gtk.MenuItem(label = "Direct Connect")
		self.recentMenu = Gtk.Menu()
		self.dummyOption = Gtk.MenuItem(label = "Coming Soon")
		self.recentOption.set_submenu(self.recentMenu)
		self.recentMenu.append(self.dummyOption)
		self.recentMenu.show_all()
		self.connectMenu.append(self.dialogOption)
		self.connectMenu.append(self.recentOption)
		self.connectMenu.append(self.directOption)
		self.connectMenu.show_all()
		
		self.toolbar = Gtk.Toolbar(icon_size = Gtk.IconSize.DND, show_arrow = True, toolbar_style = Gtk.ToolbarStyle.BOTH)
		self.connectButton = Gtk.MenuToolButton(icon_name = "network-wired", label = "Connect...")
		self.connectButton.set_menu(self.connectMenu)
		self.connectButton.connect("clicked", self.openConnectionWindow)
		self.infoButton = Gtk.ToolButton(icon_name = "dialog-information", label = "Wand Info")
		self.infoButton.set_sensitive(False)
		self.wandSettingsButton = Gtk.ToolButton(icon_name = "preferences-system", label = "Wand Settings")
		self.wandSettingsButton.set_sensitive(False)
		self.settingsButton = Gtk.ToolButton(icon_name = "applications-system", label = "App Settings")
		self.aboutButton = Gtk.ToolButton(icon_name = "help-about", label = "About")
		self.toolbar.add(self.connectButton)
		self.toolbar.add(self.infoButton)
		self.toolbar.add(Gtk.SeparatorToolItem.new())
		self.toolbar.add(self.wandSettingsButton)
		self.toolbar.add(self.settingsButton)
		self.toolbar.add(Gtk.SeparatorToolItem.new())
		self.toolbar.add(self.aboutButton)
		
		self.mainBox.add(self.toolbar)
		self.mainBox.add(Gtk.Separator.new(orientation = Gtk.Orientation.VERTICAL))
		
		self.statusBar = Gtk.Statusbar()
		self.statusBar.push(1, "gwand 0.1.0 | Disconnected")
		self.statusIcon = Gtk.Image.new_from_icon_name("network-offline-symbolic", Gtk.IconSize.DND)
		self.statusIcon.props.margin_end = 5
		self.statusBox = Gtk.Box()
		self.statusBox.pack_start(self.statusBar, True, True, 0)
		self.statusBox.pack_start(self.statusIcon, False, False, 0)
		self.mainBox.pack_end(self.statusBox, False, False, 0)
	def show(self):
		self.set_position(Gtk.WindowPosition.CENTER)
		self.show_all()
	
	def openConnectionWindow(self, button):
		self.connectWindow.show()
		self.connectWindow.scanForDevices()
		

# ~ wands = []
# ~ wand = None
# ~ shop = kano_wand.Shop()
# ~ while len(wands) == 0:
	# ~ # Scan for wands and automatically connect
	# ~ print("Scanning...")
	# ~ wands = shop.scan(connect=True)
	# ~ if len(wands):
		# ~ wand = wands[0]
		# ~ break
# ~ print("Connected to {}".format(wand.name))

win = Window()
win.show()
Gtk.main()
