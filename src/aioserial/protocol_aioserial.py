
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
            'expected a string in the form "aioserial://port[?handler=value[&option=[value]]]": '
            'not starting with aioserial:// ({!r})'.format(parts.scheme))

    handler_cls_name = None
    try:
        for option, values in urlparse.parse_qs(parts.query, True).items():
            if option == 'handler':
                handler_cls_name = values[0]
    except ValueError as e:
        raise aioserial.SerialException(
            'expected a string in the form '
            '"aioserial://port[?handler=value[&option=[value]]]": {!r}'.format(e))

    if handler_cls_name:
        import importlib

        #
        # Copied (and modified) from serial.serial_for_url
        #
        # Unfortunately there is no API for getting the class,
        # only an instance of a serial.Serial.
        #
        protocol = handler_cls_name
        module_name = '.protocol_{}'.format(protocol)
        for package_name in aioserial.protocol_handler_packages:
            try:
                importlib.import_module(package_name)
                handler_module = importlib.import_module(module_name,
                                                         package_name)
            except ImportError:
                continue
            else:
                url = url.replace("aioserial://", protocol + "://"). \
                    replace("handler=" + protocol, "")

                if hasattr(handler_module, 'serial_class_for_url'):
                    url, cls = handler_module.serial_class_for_url(url)
                else:
                    cls = handler_module.Serial
                break
        else:
            raise ValueError(
                'invalid URL, protocol {!r} not known'.format(protocol))

        cls = type(
            "AioSerial{}".format(handler_cls_name.capitalize()),
            (aioserial.aioserial._AioSerialMixin, cls),
            {}
        )
    else:
        cls = aioserial.AioSerial
        url = ''.join([parts.netloc, parts.path])

    return url, cls
