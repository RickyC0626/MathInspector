"""
this class adds extra functionality to the builtin help function,
and is used to override the the builtin help function by calling

>>> __builtins__["help"] = Help(app)

in console/interpreter.py

"""
"""
Copyright (C) 2021 Matt Calhoun

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import builtins, os
from ..util import name_ext, INSTALLED_PKGS, BUILTIN_PKGS, BUILTIN_CLASS
from ..console.builtin_print import builtin_print
from .browser import Browser
from . import manual

class Help:
	def __init__(self, app=None):
		self.app = app
		self.geometry = None
		self.browser = None

	def __call__(self, key=None, title=None):
		if key is None:
			self.browser = Browser(self.app, manual, "mathinspector", geometry=self.geometry)
			return
		obj = self.getobj(key)
		if obj is None: return
		browser = self.browser = Browser(self.app, obj, title=title, geometry=self.geometry)
		if not self.app:
			browser.mainloop()

	def __repr__(self):
		return "Type help() for interactive help, help(object) for help about object, or help.browse() to view all available documentation."

	def browse(self, callback=None):
		self.browser = Browser(self.app, browse=True, on_import=callback)

	def import_module(self, callback):
		self.browser = Browser(self.app, on_import=callback)

	def getobj(self, key):
		if key is None: return manual

		if isinstance(key, str):
			if self.app:
				if key in INSTALLED_PKGS + BUILTIN_PKGS:
					try:
						obj = __import__(key)
						return obj
					except:
						pass
				if key in self.app.objects:
					if isinstance(self.app.objects[key], tuple([getattr(builtins,i) for i in BUILTIN_CLASS])):
						return self.app.objects[key].__class__
					return self.app.objects[key]
				elif key in self.app.modules:
					return self.app.modules[key]
				elif os.path.isfile(key):
					name, ext = name_ext(key)
					if name in self.app.modules:
						return self.app.modules[name]

					if name in ("LICENSE") or ext in (".md", ".rst"):
						return key
				try:
					module, attr = key.rsplit('.', 1)
					return getattr(self.app.modules[module], attr)
				except:
					try:
						obj, attr = key.split('.', 1)
						return getattr(self.app.objects[obj], attr)
					except:
						pass
			else:
				try:
					return eval(key)
				except:
					pass
			return str
		else:
			if hasattr(key, "__class__"):
				return key.__class__
			return key
