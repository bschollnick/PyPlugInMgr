"""
General Plugin Manager for Python


.. moduleauthor:: Benjamin Schollnick <Benjamin@Schollnick.net>

import PluginMgr
test = PluginMgr.PluginMgr()
test.findcandidate_files()
"""
__version__ = "0.501"
__author__ = "Benjamin Schollnick"
__status__ = "Beta"
__credits__ = ["Benjamin Schollnick"]
__maintainer__ = "Benjamin Schollnick"
__email__ = "Benjamin@Schollnick.net"
__AppName__ = 'Py Plugin Manager (PPM)'


import importlib
import inspect
import pathlib
import os
import os.path
import sys
from importlib.util import spec_from_file_location, module_from_spec

class PlugInMgr:
    def __init__(self,
                 plugin_dir=r".{}Plugins".format(os.sep),
                 allow_creation=False,
                 plug_ext=".py"):

        self.plugin_dir = pathlib.Path.cwd() / plugin_dir
        self.candidate_files = []
        self.plug_ext = plug_ext
        self.catalog = {}

        if not self.plugin_dir.exists() and allow_creation == True:
            self.plugin_dir.mkdir(exist_ok=True)


    def findcandidate_files(self):
        """
            Locate what files are available as plugins and load them.

        """
        #cfiles = list(self.plugin_dir.glob("*{}".format(self.plug_ext)))
        sys.path.append(str(self.plugin_dir))
        cfiles = self.plugin_dir.glob("*{}".format(self.plug_ext))
        self.candidate_files = []
        for x in cfiles:
            self.candidate_files.append(str(x))
            #base_filename = os.path.splitext(os.path.split(x)[1])[0]
            base_filename = os.path.split(x)[1]

            module = self.get_installed_config(base_filename)
            self.catalog[os.path.splitext(base_filename)[0]] = [module,\
                dict(inspect.getmembers(module))]
            #self.PluginCatlaog


    def get_installed_config(self, config_file):#installDir, config_file):
        """
        Reads config from the installation directory of Plenum.

        #:param installDir: installation directory of Plenum
        :param config_file: name of the configuration file
        :raises: FileNotFoundError
        :return: the configuration as a python object
        """
        #config_path = os.path.join(installDir, config_file)
        config_path = self.plugin_dir / config_file
        if not config_path.exists():
            raise FileNotFoundError("No file found at location {}".
                                    format(config_path))
        spec = spec_from_file_location(config_file, config_path)
        config = module_from_spec(spec)
        spec.loader.exec_module(config)
        return config

    def get_plugin(self, plugin_name):
        """
        Return the pointer to the name space of the plugin
        """
        if plugin_name in self.catalog:
            return self.catalog[plugin_name][0]
        return None


    def get(self, plugin_name, object_name, default_value=None):
        """
        This allows you to be able to pull any variable, function, etc
        from the module's name space.

        It's not necessary, since you just use get_plugin to gain direct access
        the module, but this allows you to use indirection to get access to
        the constants, variables, functions, and classes.

        Examples:


        Alternative:
        getattr(themodule, "attribute_name", None)

            The third argument is the default value if the attribute does not exist.
        """
        #if object_name in self.catalog[plugin_name][1]:
        if self.has(plugin_name, object_name):
            return self.catalog[plugin_name][1][object_name]

        return default_value

    def has(self, plugin_name, object_name):
        """
        If the object_name is in the plugin_name's name space,
        then return True.

        Otherwise, return False in the following conditions

            1) plugin was not found (eg not in catalog)
            2) object was not found in plugin's name space

        """
        if plugin_name in self.catalog:
            return object_name in self.catalog[plugin_name][1]
        return None