'''
Network Service Discovery
====

The :class:`NSD` provides a way to discover services on a network.

Simple Examples
---------------


Supported Platforms
-------------------


'''
from collections import namedtuple

ServiceInfoBase = namedtuple(
    'ServiceInfoBase',
    'host, port, service_name, service_type, attributes, data')


class NSD(object):
    '''
    Network service discovery facade.
    '''

    class ServiceInfo(ServiceInfoBase):
        '''
        Use this class to descibe the service.
        '''
        def __new__(cls, name, **kwargs):
            kwargs['service_name'] = name
            kwargs.setdefault('service_type', ''.join((name.lower(), '._tcp')))
            kwargs.setdefault('host', None)
            kwargs.setdefault('port', None)
            kwargs.setdefault('attributes', dict())
            kwargs.setdefault('data', None)
        def __init__(self, ):
            if attributes is None:
                attributes = dict()
            super(NSD.ServiceInfo, self).__init__(
                None, port, name, type_, attributes)

    def register_service(self, service_info, listener):
        '''
        Register local services to be advertised

        :param service_info: The service to register
        :param listener: methods to be called on events

        :type service_info: :class:`NSD.ServiceInfo`
        :type listener: TODO
        '''
        self._register_service(service_info, listener)

    def unregister_service(self, listener):
        '''
        Unregister a previously-registered service
        '''
        self._unregister_service(listener)

    def discover_services(self, service, listener):
        '''
        Initiate service discovery to browse for instances of a service type.

        :param service: The service to look for
        :param listener: Listener to handle results

        :type service_info: string
        :type listener: TODO
        '''
        self._discover_services(service, listener)

    def resolve_service(self, service_info, listener):
        '''
        Resolve a discovered service.

        :param service_info: The discovered info object
        :param listener: Listener to handle results

        :type service_info: TODO
        :type listener: TODO
        '''
        self._resolve_service(service_info, listener)

    # private

    def _register_service(self, service_info, listener):
        raise NotImplementedError()

    def _unregister_service(self, listener):
        raise NotImplementedError()

    def _discover_services(self, service, listener):
        raise NotImplementedError()

    def _resolve_service(self, service_info, listener):
        raise NotImplementedError()
