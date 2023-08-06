#!/usr/bin/env python
# Copyright 2010-2017, Damian Johnson and The Tor Project
# See LICENSE for licensing information

import gzip
import os
import stat
import sys
import sysconfig

import nyx

from distutils import log
from distutils.core import setup
from distutils.command.install import install


if '--dryrun' in sys.argv:
  DRY_RUN = True
  sys.argv.remove('--dryrun')
else:
  DRY_RUN = False

SUMMARY = 'Terminal status monitor for Tor (https://www.torproject.org/).'
DRY_RUN_SUMMARY = 'Ignore this package. This is dry-run release creation to work around PyPI limitations (https://github.com/pypa/packaging-problems/issues/74#issuecomment-260716129).'

DESCRIPTION = """
Nyx is a command-line monitor for Tor. With this you can get detailed real-time information about your relay such as bandwidth usage, connections, logs, and much more. For more information see `Nyx's homepage <https://nyx.torproject.org/>`_.

Quick Start
-----------

To install you can either use...

::

  pip install nyx

... or install from the source tarball. Nyx supports both the python 2.x and 3.x series.
"""

MANIFEST = """
include LICENSE
include MANIFEST.in
include nyx.1
include run_tests.py
graft test
graft web
global-exclude __pycache__
global-exclude *.orig
global-exclude *.pyc
global-exclude *.swp
global-exclude *.swo
global-exclude *~
""".strip()


class NyxInstaller(install):
  """
  Nyx installer. This adds the following additional options...

    --man-page [path]
    --sample-path [path]

  If the man page path ends in '.gz' it will be compressed. Empty paths such
  as...

    % python setup.py install --man-page ''

  ... will cause that resource to be omitted.
  """

  user_options = install.user_options + [
    ('man-page=', None, 'man page location'),
    ('sample-path=', None, 'example nyxrc location'),
  ]

  def initialize_options(self):
    install.initialize_options(self)
    self.man_page = None
    self.sample_path = None

  def run(self):
    install.run(self)

    self.install_bin_script('run_nyx', os.path.join(self.install_scripts, 'nyx'))
    self.install_file('man page', 'nyx.1', self.man_page)
    self.install_file('nyxrc sample', os.path.join('web', 'nyxrc.sample'), self.sample_path)

  def install_bin_script(self, source, dest):
    # Install our bin script. We do this ourselves rather than with the setup()
    # method's scripts argument because we want to call the script 'nyx' rather
    # than 'run_nyx'.
    #
    # If using setuptools this would be better replaced with its entry_points.

    self.mkpath(os.path.dirname(dest))

    with open(source, 'rb') as source_file:
      with open(dest, 'wb') as dest_file:
        orig_shebang = source_file.readline()

        python_cmd = 'python%s%s' % (sysconfig.get_config_var('VERSION'), sysconfig.get_config_var('EXE'))
        new_shebang = '#!%s\n' % os.path.join(sysconfig.get_config_var('BINDIR'), python_cmd)

        log.info("adjusting bin script's shebang line '%s' -> '%s'" % (orig_shebang.strip(), new_shebang.strip()))
        dest_file.write(str.encode(new_shebang))
        dest_file.write(source_file.read())

    mode = ((os.stat(dest)[stat.ST_MODE]) | 0o555) & 0o7777
    os.chmod(dest, mode)
    log.info("installed bin script to '%s'" % dest)

  def install_file(self, resource, source, dest):
    if not dest:
      log.info('skipping installation of the %s' % resource)
      return
    elif not os.path.exists(source):
      raise OSError(None, "%s doesn't exist at '%s'" % (resource, source))

    self.mkpath(os.path.dirname(dest))
    open_func = gzip.open if dest.endswith('.gz') else open

    with open(source, 'rb') as source_file:
      with open_func(dest, 'wb') as dest_file:
        dest_file.write(source_file.read())
        log.info("installed %s to '%s'" % (resource, dest))


# installation requires us to be in our setup.py's directory

setup_dir = os.path.dirname(os.path.join(os.getcwd(), __file__))
os.chdir(setup_dir)

with open('MANIFEST.in', 'w') as manifest_file:
  manifest_file.write(MANIFEST)

try:
  setup(
    name = 'nyx-dry-run' if DRY_RUN else 'nyx',
    version = nyx.__version__,
    description = DRY_RUN_SUMMARY if DRY_RUN else SUMMARY,
    long_description = DESCRIPTION,
    license = nyx.__license__,
    author = nyx.__author__,
    author_email = nyx.__contact__,
    url = nyx.__url__,
    packages = ['nyx', 'nyx.panel'],
    keywords = 'tor onion controller',
    install_requires = ['stem>=1.6.0'],
    package_data = {'nyx': ['settings/*']},
    cmdclass = {'install': NyxInstaller},
    classifiers = [
      'Development Status :: 5 - Production/Stable',
      'Environment :: Console :: Curses',
      'Intended Audience :: System Administrators',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Topic :: Security',
    ],
  )
finally:
  if os.path.exists('MANIFEST.in'):
    os.remove('MANIFEST.in')

  if os.path.exists('MANIFEST'):
    os.remove('MANIFEST')
