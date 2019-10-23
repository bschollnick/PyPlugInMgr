# Py Plugin Manager

A slightly different take on a Python Plugin Manager for python 3.



## Introduction

- ###### What is a plugin?

  - Well, strictly, it's a component that adds a specific feature to a program.  But for Py Plugin Manager, this concept is a bit less strict.  
  - PPM allows any python file be loaded and reloaded dynamically.

- ###### How does PPM differ from other Plugin Managers?

  - Currently, no changes need to be made to the module or code you wish to import.
  - Unlike some other Plugin Managers, no configuration (aka .plugin) files need to be created.

- ###### Best Practices (so far)

  - Separate your plugins into a separate directly, so that they are not mixed in with your application code.
  - If your plugins require access to other modules that are not within the plugin directory, make sure that the sys.path is pointing to those directories so that your plugin's can successfully import those modules.



## What is Py Plugin Manager? 

PPM allows you to quickly load in a Python module, and be able to (reasonably) easily access variables, functions, constants, etc from those modules.

For example:

`>>>import PyPluginMgr`
`>>>test = PyPluginMgr.PlugInMgr(plugin_dir=r".\plugins",
                   			  allow_creation=True, plug_ext=".py")`
`>>>test.findcandidate_files()`

At this point all the .py files in .\plugins will be loaded and placed in the plugin catalog.  At this point there are several ways to access the plugin contents:

1. Indirectly accessing the plugin name space (via get)
   `>>>test.get("pyfile1", "__email__")`
   `'Benjamin@Schollnick.net'`
   `>>>test.get("pyfile1", "test")("this is an example of calling a function via get")`
   `test,  this is an example of calling a function via get`

2. Directly access the plugin name space (via get_plugin)

   `>>>activeplugin = test.get_plugin("pyfile1")`
   `>>>activeplugin`
   `<module 'pyfile1.py' from '....\\PluginMgr\\plugins\\pyfile1.py'>`
   `>>>activeplugin.__name__`
   `'pyfile1.py'`
   `>>>activeplugin.test("hello from Test!")`
   `test,  hello from Test!`

