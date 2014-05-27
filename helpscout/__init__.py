"""Python Helpscout API Wrapper"""

__version__ = '0.0.1'
__all__ = ['Client']

USER_AGENT = 'Helpscout Python API Wrapper %s' % __version__

from helpscout.client import Client