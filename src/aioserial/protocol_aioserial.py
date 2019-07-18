
import aioserial

try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse


def serial_class_for_url(url):
    """extract host and port from an URL string"""
    parts = urlparse.urlsplit(url)
    if parts.scheme != 'aioserial':
        raise aioserial.SerialException(
            'expected a string in the form "aioserial://port": '
            'not starting with aioserial:// ({!r})'.format(parts.scheme))

    return ''.join([parts.netloc, parts.path]), aioserial.AioSerial
