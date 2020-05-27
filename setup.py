import os
import re
import setuptools

PIPNAME          = "PyPluginMgr"
NAME             = "PluginMgr"
AUTHOR           = "Benjamin Schollnick"
AUTHOR_EMAIL     = "Benjamin@Schollnick.net"
DESCRIPTION      = "Python Plugin Manager."
LICENSE          = "MIT"
KEYWORDS         = "Plugin"
URL              = "https://github.com/bschollnick/" + PIPNAME
README           = ".github/README.md"
CLASSIFIERS      = [
  "Environment :: Console",
  "Development Status :: 5 - Production/Stable",
  "Intended Audience :: Developers",
  "Topic :: Software Development",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3.7",
  "Programming Language :: Python :: 3.8",
]
INSTALL_REQUIRES = []
ENTRY_POINTS     = {}

HERE = os.path.dirname(__file__)

def read(file):
  with open(os.path.join(HERE, file), "r") as fh:
    return fh.read()

VERSION = re.search(
  r'__version__ = [\'"]([^\'"]*)[\'"]',
  read(NAME.replace("-", "_") + "/__init__.py")
).group(1)

LONG_DESCRIPTION = read(README)

if __name__ == "__main__":
  setuptools.setup(name=PIPNAME,
        version=VERSION,
        packages=setuptools.find_packages(),
        author=AUTHOR,
        author_email=AUTHOR_EMAIL,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        license=LICENSE,
        keywords=KEYWORDS,
        url=URL,
        classifiers=CLASSIFIERS,
        install_requires=INSTALL_REQUIRES,
        entry_points=ENTRY_POINTS)
