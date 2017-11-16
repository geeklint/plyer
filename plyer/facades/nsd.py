'''
Network Service Discovery
====

The :class:`NSD` provides a way to discover services on a network.

Simple Examples
---------------


Supported Platforms
-------------------


'''


class NSD(object):
    '''
    Network service discovery facade.
    '''

    def register_service(self, service_info, proto, cb):
        '''
        Register local services to be advertised

        :param service_info:
        :param proto:

        :type service_info:
        :type proto: int
        '''
        self._register_service(service_info, proto, cb)

    def unregister_service(self, ):
        '''
        Unregister a previously-registered service
        '''
        self._unregister_service()

    def discover_services(self, service, proto, cb):
        '''
        Initiate service discovery to browse for instances of a service type.
        '''
        self._discover_services(service, proto, cb)

    def resolve_service(self, service_info, cb):
        '''
        Resolve a discovered service.

        :param service_info:
        :param proto:

        :type service_info:
        :type proto: int
        '''
        self._resolve_service(service_info, cb)

    # private

    def _register_service(self, service_info, proto, cb):
        raise NotImplementedError()

    def _unregister_service(self, ):
        raise NotImplementedError()

    def _discover_services(self, service, proto, cb):
        raise NotImplementedError()

    def _resolve_service(self, service_info, cb):
        raise NotImplementedError()
