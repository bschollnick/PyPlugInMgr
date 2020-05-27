"""
General Plugin Manager for Python v3

The basic concept is a simplified (but not less featured) version of YAPSY.

Some core ideas were based off of
https://lkubuntu.wordpress.com/2012/10/02/writing-a-python-plugin-api/.  Others
were not...

YAPSY, and I have had a distinct love/hate relationship, the main issue is that
in the application I am using YAPSY with plugins sometimes stop functioning for
no obvious reason.

While YAPSY, and PPM are both designed around "Python's standard library'".
The main difference is simply in execution.  PPM does not require configuration
files, and allows the implementor to design the code of the plug-in to work
without needing an dedicated "plug-in" class.

Example:

.. code-block:
    import PyPluginMgr
    test = PyPluginMgr.PlugInMgr(plugin_dir=r"plugins",
                                 allow_creation=True, plug_ext=".py")
    test.findcandidate_files()

at this point, PPM will check the plugin_dir for files, if the directory does
not exist (allow_creation=True) it would be created.

Please note plug_ext must be .py.  The comments in the stackoverflow thread
(see findcandidate_files) indicate this import mechanism does not allow
non-standard (.py) file extensions.  Testing does bare this out.
I have left plug_ext currently in the API, in the off chance that it can
be enabled in the future.

Once the candidate plugin files are detected, there are several ways to access
the plugin contents:

1) Indirectly accessing the plugin name space (via get):

.. code-block:

>>>test.get("pyfile1", "__email__")
'Benjamin@Schollnick.net'
>>>test.get("pyfile1", "test")("this is an example of calling a function via get")
test,  this is an example of calling a function via get```


2) Or via directly access the plugin name space (via get_plugin).  Please note:
    the name is based off the file system filename of the module.

.. code-block:
>>>activeplugin = test.get_plugin("pyfile1")
>>>activeplugin
<module 'pyfile1.py' from '....\\PluginMgr\\plugins\\pyfile1.py'>
>>>activeplugin.__name__
'pyfile1.py'
>>>activeplugin.test("hello from Test!")    # running the function test
test,  hello from Test!


.. moduleauthor:: Benjamin Schollnick <Benjamin@Schollnick.net>


"""
__version__ = "1.0.0"
__author__ = "Benjamin Schollnick"
__status__ = "Release"
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
    """
    Plug-In Manager core class

    """
    def __init__(self,
                 plugin_dir=r".{}Plugins".format(os.sep),
                 allow_creation=False,
                 plug_ext=".py"):
        """
            Plug-in Manager.  Locate, Manage, and hand-off Plug-Ins.

        Args:

            plugin_dir (str): The path to the plug-in files

            allow_creation (boolean): Default - False.  Controls the behavior
                If the plugin_dir does not exist.  If set True, the directory
                will be created.  If False (Default), then it will silently
                fail.

            plug_ext (str): The file extension (eg. .py) of the plug-in files.
                **CURRENTLY UNUSED**  For future use.

        Returns:

            Boolean: True if the file exists, or false if it doesn't.
            Integer: If rtn_size is true, an existing file will return
                an integer


        Examples
        --------

        import PyPluginMgr
        test = PyPluginMgr.PlugInMgr(plugin_dir=r"plugins",
                                     allow_creation=True)
        test.findcandidate_files()

        """
        self.plugin_dir = pathlib.Path.cwd() / plugin_dir
        self.candidate_files = []
        self.plug_ext = plug_ext
        self.catalog = {}
        self.formattedCatalog = {}

        if not self.plugin_dir.exists() and allow_creation == True:
            self.plugin_dir.mkdir(exist_ok=True)


    def findcandidate_files(self):
        """
        Find the candidate files for the Plug-in Manager.

	    Raises:

            ImportError : If unable to import a plug-in, ImportError will be
                raised.

        Examples
        --------

        import PyPluginMgr
        test = PyPluginMgr.PlugInMgr(plugin_dir=r"plugins",
                                     allow_creation=True)
        test.findcandidate_files()


        """
        #cfiles = list(self.plugin_dir.glob("*{}".format(self.plug_ext)))
        sys.path.append(str(self.plugin_dir))
        cfiles = self.plugin_dir.glob("*{}".format(self.plug_ext))
        self.candidate_files = []
        for x in cfiles:
            self.candidate_files.append(str(x))
            base_filename = os.path.split(x)[1]

            try:
                module = self.get_installed_config(base_filename)
                self.catalog[os.path.splitext(base_filename)[0]] = [module,\
                    dict(inspect.getmembers(module))]
                self.formattedCatalog[os.path.splitext(base_filename)[0].title()] = [module,\
                    dict(inspect.getmembers(module))]
            except AttributeError:

                # An Error occurred during import of plugin
                raise ImportError("Unable to import Plugin Module - %s" % base_filename)
            #self.PluginCatlaog


    def get_installed_config(self, config_file):
        """
        import a python file from file system

        :param config_file: name of the configuration file
        :raises: FileNotFoundError
        :return: the configuration as a python object

        https://stackoverflow.com/questions/19009932/
            import-arbitrary-python-source-file-python-3-3
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
        Return module to access the plug-in (or in otherwords return a
        "Pointer" to the name space of the module)

        Args:

            plugin_name (str): The File System filename (w/o extension)
                of the plug-in.


        Examples
        --------

        import PyPluginMgr
        test = PyPluginMgr.PlugInMgr(plugin_dir=r"plugins",
                                     allow_creation=True)
        test.findcandidate_files()
        plugin1 = test.get_plugin("myPlugin1")
        plugin1.run()

        """
        if plugin_name in self.catalog:
            return self.catalog[plugin_name][0]
        if plugin_name.title() in self.formattedCatalog:
            return self.formattedCatalog[plugin_name.title()][0]
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
        pname = None
        if plugin_name in self.catalog:
            pname = plugin_name
        elif plugin_name.title() in self.formattedCatalog:
            pname = plugin_name.title()
        print(pname)
        if pname is None:
            if object_name in self.catalog[pname][1]:
                return self.catalog[pname][1][object_name]
        return default_value


#     def has(self, plugin_name, object_name):
#         """
#         If the object_name is in the plugin_name's name space,
#         then return True.
#
#         Otherwise, return False in the following conditions
#
#             1) plugin was not found (eg not in catalog)
#             2) object was not found in plugin's name space
#
#         """
#         if plugin_name in self.catalog:
#             return object_name in self.catalog[plugin_name][1]
#         return None
