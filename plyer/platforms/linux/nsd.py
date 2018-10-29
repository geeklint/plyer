'''Implementation NSD for Linux.'''

import warnings
from plyer.facades import NSD


class DBusNSD(NSD):
    '''Linux NSD class.
    '''

    def __init__(self):
        import dbus
        self.dbus = dbus

    def _register_service(self, service_info, listener):
        bus = self.dbus.SystemBus()
        server = self.dbus.Interface(
            bus.get_object("org.freedesktop.Avahi", "/"),
            "org.freedesktop.Avahi.Server")
        group = dbus.Interface(
            bus.get_object("org.freedesktop.Avahi", server.EntryGroupNew()),
            "org.freedesktop.Avahi.EntryGroup")
        group.AddService(
            -1,  # interface (IF_UNSPEC)
            -1,  # protocol (PROTO_UNSPEC)
            dbus.UInt32(0),  # flags (none)
            service_info.service_name,
            service_info.service_type,
            "",  # domain (none)
            service_info.host,
            dbus.UInt16(service_info.port),
            ""  # text (none)
        )

        group.Commit()
        self.group = group

    def _unregister_service(self, listener):
        raise NotImplemented()

    def _discover_services(self, service, listener):
        loop = DBusGMainLoop()
        bus = dbus.SystemBus(mainloop=loop)
        server = dbus.Interface(
            bus.get_object("org.freedesktop.Avahi", "/"),
            'org.freedesktop.Avahi.Server')
        server.ServiceBrowserNew(
            avahi.IF_UNSPEC,
            avahi.PROTO_UNSPEC,
            TYPE,
            'local',
            dbus.UInt32(0)
        )
        browser = dbus.Interface(
            bus.get_object(avahi.DBUS_NAME,),
            avahi.DBUS_INTERFACE_SERVICE_BROWSER,
        )
        sbrowser.connect_to_signal("ItemNew", myhandler)
        gobject.MainLoop().run()

    def _resolve_service(self, service_info, listener):
        raise NotImplemented()


def instance():
    '''Returns NSD with android features.

    :return: instance of class LinuxNSD
    '''
    try:
        import dbus
    except ImportError:
        msg = ("The Python dbus package is not installed.\n"
               "Try installing it with your distribution's package manager, "
               "it is usually called python-dbus or python3-dbus, but you "
               "might have to try dbus-python instead, e.g. when using pip.")
    else:
        return ()
