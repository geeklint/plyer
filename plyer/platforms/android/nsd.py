'''Implementation NSD for Android.'''

from collections import Iterator, MutableMapping

from jnius import autoclass, PythonJavaClass, java_method
from plyer.facades import NSD


NsdServiceInfo = autoclass('android.net.nsd.NsdServiceInfo')
NsdManager = autoclass('android.net.nsd.NsdManager')
PROTOCOL = NsdManager.PROTOCOL_DNS_SD


class MapWrapper(MutableMapping):
    class IterWrapper(Iterator):
        def __init__(self, javaiter):
            self.javaiter = javaiter

        def next(self):
            if not self.javaiter.hasNext():
                raise StopIteration
            else:
                return self.javaiter.next()

    def __init__(self, javamap):
        self.javamap = javamap

    def __getitem__(self, key):
        if self.javamap.containsKey(key):
            return self.javamap.get(key)
        else:
            raise KeyError

    def __setitem__(self, key, value):
        self.javamap.put(key, value)

    def __delitem__(self, key):
        self.javamap.remove(key)

    def __iter__(self):
        return self.IterWrapper(self.javamap.keySet().iterator())

    def __len__(self):
        return self.javamap.size()


def service_info_topy(javains):
    '''
    Convert java NsdServiceInfo to NSD.ServiceInfo
    '''
    pyins = NSD.ServiceInfo(None)
    pyins._internal = javains
    pyins.host = javains.getHost().getHostAddress()
    pyins.port = javains.getPort()
    pyins.service_name = javains.getServiceName()
    pyins.service_type = javains.getServiceType()
    pyins.attributes = MapWrapper(javains.getAttributes())
    return pyins


def service_info_tojava(pyins):
    if pyins._internal is not None:
        return pyins._internal
    javains = pyins._internal = NsdServiceInfo()
    javains.setServiceName(pyins.service_name)
    javains.setServiceType(pyins.service_type)
    javains.setPort(pyins.port)
    for key, value in pyins.attributes.iteritems():
        javains.setAttribute(key, value)
    return javains


class PythonRegistrationListener(PythonJavaClass):
    __javainterfaces__ = ['android.net.nsd.NsdManager.RegistrationListener']

    def __init__(self, listener):
        super(PythonRegistrationListener, self).__init__()
        self.listener = listener

    @java_method('(Landroid/net/nsd/NsdServiceInfo;)V')
    def onServiceRegistered(serviceInfo):
        try:
            cb = self.listener.on_service_registered
        except AttributeError:
            pass
        else:
            cb(service_info_topy(serviceInfo))

    @java_method('(Landroid/net/nsd/NsdServiceInfo;I)V')
    def onRegistrationFailed(serviceInfo, errorCode):
        try:
            cb = self.listener.on_registration_failed
        except AttributeError:
            pass
        else:
            cb(service_info_topy(serviceInfo), errorCode)

    @java_method('(Landroid/net/nsd/NsdServiceInfo;)V')
    def onServiceUnregistered(serviceInfo):
        try:
            cb = self.listener.on_service_unregistered
        except AttributeError:
            pass
        else:
            cb(service_info_topy(serviceInfo))

    @java_method('(Landroid/net/nsd/NsdServiceInfo;I)V')
    def onUnregistrationFailed(serviceInfo, errorCode):
        try:
            cb = self.listener.on_unregistration_failed
        except AttributeError:
            pass
        else:
            cb(service_info_topy(serviceInfo), errorCode)


class PythonDiscoveryListener(PythonJavaClass):
    __javainterfaces__ = ['android.net.nsd.NsdManager.DiscoveryListener']

    def __init__(self, listener):
        super(PythonDiscoveryListener, self).__init__()
        self.listener = listener

    @java_method('(Ljava/util/String;)V')
    def onDiscoveryStarted(regType):
        try:
            cb = self.listener.on_discovery_started
        except AttributeError:
            pass
        else:
            cb(regType)

    @java_method('(Landroid/net/nsd/NsdServiceInfo;)V')
    def onServiceFound(service):
        try:
            cb = self.listener.on_service_found
        except AttributeError:
            pass
        else:
            cb(service_info_topy(service))

    @java_method('(Landroid/net/nsd/NsdServiceInfo;)V')
    def onServiceLost(service):
        try:
            cb = self.listener.on_service_lost
        except AttributeError:
            pass
        else:
            cb(service_info_topy(service))

    @java_method('(Ljava/util/String;)V')
    def onDiscoveryStopped(serviceType):
        try:
            cb = self.listener.on_discovery_stopped
        except AttributeError:
            pass
        else:
            cb(serviceType)

    @java_method('(Ljava/util/String;I)V')
    def onStartDiscoveryFailed(serviceType, int errorCode):
        try:
            cb = self.listener.on_start_discovery_failed
        except AttributeError:
            pass
        else:
            cb(serviceType, errorCode)

    @java_method('(Ljava/util/String;I)V')
    def onStopDiscoveryFailed(String serviceType, int errorCode):
        try:
            cb = self.listener.on_stop_discovery_failed
        except AttributeError:
            pass
        else:
            cb(serviceType, errorCode)


class PythonResolveListener(PythonJavaClass):
    __javainterfaces__ = ['android.net.nsd.NsdManager.ResolveListener']

    def __init__(self, listener):
        super(PythonResolveListener, self).__init__()
        self.listener = listener

    @java_method('(Landroid/net/nsd/NsdServiceInfo;I)V')
    def onResolveFailed(serviceInfo, errorCode):
        try:
            cb = self.listener.on_resolve_failed
        except AttributeError:
            pass
        else:
            cb(service_info_topy(serviceInfo), errorCode)

    @java_method('(Landroid/net/nsd/NsdServiceInfo;)V')
    def onServiceResolved(serviceInfo):
        try:
            cb = self.listener.on_service_resolved
        except AttributeError:
            pass
        else:
            cb(service_info_topy(serviceInfo))


class AndroidNSD(NSD):
    '''Android NSD class.
    '''

    def __init__(self):
        self.manager = NsdManager()

    def _register_service(self, service_info, listener):
        # wrap listener
        try:
            android_listener = listener._AndroidNSD__registration_listener
        except AttributeError:
            android_listener = PythonRegistrationListener(listener)
            listener._AndroidNSD__registration_listener = android_listener
        # register
        self.manager.registerService(
            service_info_tojava(service_info), PROTOCOL, android_listener)

    def _unregister_service(self, listener):
        try:
            android_listener = listener._AndroidNSD__registration_listener
        except AttributeError:
            android_listener = PythonRegistrationListener(listener)
            listener._AndroidNSD__registration_listener = android_listener
        self.manager.unregisterService(android_listener)

    def _discover_services(self, service, listener):
        try:
            android_listener = listener._AndroidNSD__discovery_listener
        except AttributeError:
            android_listener = PythonRegistrationListener(listener)
            listener._AndroidNSD__discovery_listener = android_listener
        self.manager.discoverServices(service, android_listener)

    def _resolve_service(self, service_info, listener):
        try:
            android_listener = listener._AndroidNSD__resolve_listener
        except AttributeError:
            android_listener = PythonResolveListener(listener)
            listener._AndroidNSD__resolve_listener = android_listener
        self.manager.discoverServices(service, android_listener)


def instance():
    '''Returns NSD with android features.

    :return: instance of class AndroidNSD
    '''
    return AndroidNSD()
