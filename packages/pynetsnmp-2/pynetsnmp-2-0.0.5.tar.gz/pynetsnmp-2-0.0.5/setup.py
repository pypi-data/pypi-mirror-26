from distutils.command.build import build as _build
from distutils.command.clean import clean as _clean

from setuptools import setup, find_packages
import os
from pynetsnmp import genconstants
from pynetsnmp.version import VERSION


class clean(_clean):
    def run(self):
        if os.path.exists('/usr/include/net-snmp/library/snmp_api.h'):
            for filename in "CONSTANTS.py", "CONSTANTS.pyc":
                if os.path.exists(filename):
                    os.remove(filename)
                _clean.run(self)


class build(_build):
    def run(self):
        if os.path.exists('/usr/include/net-snmp/library/snmp_api.h'):
            genconstants.make_imports()
            _build.run(self)

if __name__ == '__main__':
    setup(name='pynetsnmp-2',
          version=VERSION,
          url="https://github.com/kalombos/pynetsnmp",
          download_url="https://github.com/kalombos/pynetsnmp",
          description='Ctypes Wrapper for net-snmp using twisted',
          long_description="This repo is a fork of https://github.com/zenoss/pynetsnmp "
                           "with opportunity to use set method.",
          author='Eric C. Newton',
          author_email='ecn@zenoss.com',
          maintainer='kalombo',
          maintainer_email='nogamemorebrain@gmail.com',
          cmdclass={'build': build, 'clean': clean},
          packages=find_packages(),
          install_requires=[
              'ipaddr',
              'Twisted'
          ],
          keywords=['snmp', 'twisted', 'pynetsnmp', 'netsnmp'],
          )
