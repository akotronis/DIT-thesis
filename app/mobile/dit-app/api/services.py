import asyncio
import os

import requests
from urllib.parse import urljoin

from api import constants as api_cnst

class RequestManager:
    methods = ['get', 'post', 'put', 'patch', 'delete']

    def __new__(cls, *args, **kwargs):
        """
        Override to define methods for 'get', 'post', 'put', 'patch', 'delete'
        on the class dynamicaly avoiding code duplication.
        """
        for method_name in cls.methods:
            setattr(cls, method_name, cls.build_request_method(method_name))
        return super().__new__(cls)

    def __init__(self, base_url=None, headers=None, auth=None, verify=None):
        self.base_url = base_url
        self.headers = headers or {}
        self.auth = auth
        self.verify = verify

    def handle_requests(self, request_method_obj, *args, **kwargs):
        """
        Intermediate method that actually executes the requests.
        Can be extended by child classes to implement custom logic
        like error handling.
        """
        return request_method_obj(*args, **kwargs)
    
    @staticmethod
    def build_request_method(method_name):
        """
        Method that creates and returns the requests module method.
        Used by `__new__` override
        """
        def request_method(self, url='/', **kwargs):
            args, kwargs = self.prepare_request_method_input(url, **kwargs)
            request_method_obj = getattr(requests, method_name)
            return self.handle_requests(request_method_obj, *args, **kwargs)
        return request_method

    @property
    def default_kwargs(self):
        return {'url':self.base_url, 'headers':self.headers, 'auth':self.auth, 'verify':self.verify}
    
    def prepare_request_method_input(self, url='/', **kwargs):
        """
        - Join passed `url` with `url` of `default_kwargs` (which is `base_url`)
          as common behaviour for all child classes.
        - Override to add custom functionality.
        """
        default_kwargs = self.default_kwargs
        passed_url_joined_with_base_url = urljoin(default_kwargs.pop('url'), url)
        args, kwargs = [passed_url_joined_with_base_url], {**default_kwargs, **kwargs}
        kwargs.pop('url', None)
        return args, kwargs
    
    def build_url(self, url='/', **kwargs):
        """
        Used to check the built url from passed args/kwargs without sending a request
        """
        args, kwargs = self.prepare_request_method_input(url, **kwargs)
        kwargs.pop('verify', None)
        return requests.Request(None, *args, **kwargs).prepare().url
    

class DitService(RequestManager):
    def __init__(self, base_url=None, headers=None):
        super().__init__(base_url or api_cnst.BACKEND_URL, headers)

    def prepare_request_method_input(self, url='/', **kwargs):
        """
        Override corresponding inherited method to implement common
        endpoint case specific behavior:
        - Add 'api' to url
        """
        api_prefixed_url = '/'.join(['api', url.lstrip('/')])
        return super().prepare_request_method_input(api_prefixed_url, **kwargs)

    def handle_requests(self, *args, **kwargs):
        """
        Perform error handling specific to the class
        request manager
        """
        response_json = None
        try:
            response = super().handle_requests(*args, **kwargs)
            status_code = response.status_code
            response_json = response.json() if status_code != 204 else {}
        except Exception as e:
            error_message = response_json or str(e)
            status_code, response_json = 500, {'ERROR': error_message}
        return status_code, response_json
    
    def register_user(self, email, password):
        return self.post('users', json={'email': email, 'password': password})
    
    def patch_user_visibility(self, id_, visible):
        return self.patch(f'users/{id_}', json={'visible': visible})
    
    def authenticate_user(self, email, password):
        data = {'email': email, 'password': password}
        return self.post('authenticate', json=data)
    
    def create_group(self, name):
        return self.post('groups', json={'name':name})
    
    def rename_group(self, id_, name):
        return self.patch(f'groups/{id_}', json={'name':name})
    
    def get_groups(self):
        return self.get('groups')
    
    def get_group(self, id_):
        return self.get(f'groups/{id_}')
    
    def invite_to_group(self, group_id, email):
        return self.post('invitations', json={'group':group_id, 'guest':email})
    
    def leave_group(self, id_):
        return self.patch(f'groups/{id_}', params={'leave':True})
    
    def delete_group(self, id_):
        return self.delete(f'groups/{id_}')
    
    def get_invitations(self, type_='host'):
        return self.get(f'invitations', params={'type':type_})
    
    def respond_to_invitation(self, id_, status):
        return self.patch(f'invitations/{id_}', json={'status':status})
    
    def create_group_zone(self, zone_data):
        return self.post('zones', json=zone_data)
    
    def delete_zone(self, id_):
        return self.delete(f'zones/{id_}')
    
    def create_location(self, location_data):
        return self.post('locations', json=location_data)
    
    def get_locations(self, user_ids=None, start=None, latest=None, mock=None, visible=None):
        params = {k:v for k,v in locals().items() if v is not None and k != 'self'}
        params['user_id'] = params.pop('user_ids', None)
        return self.get('locations', params=params)
    
    def get_notifications(self, seen=None):
        params = {'seen':seen} if seen is not None else {}
        return self.get('notifications', params=params)
    
    def patch_notification(self, id_, seen=None):
        data = {'seen':seen} if seen is not None else {}
        return self.patch(f'notifications/{id_}', json=data)
    
    async def patch_notification_async(self, id_, seen):
        await asyncio.to_thread(self.patch_notification, id_, seen)
    
    async def patch_notifications_async(self, ids, seen):
        await asyncio.gather(*[self.patch_notification_async(id_, seen) for id_ in ids])
    
    def patch_notifications(self, ids, seen=None):
        asyncio.run(self.patch_notifications_async(ids, seen))