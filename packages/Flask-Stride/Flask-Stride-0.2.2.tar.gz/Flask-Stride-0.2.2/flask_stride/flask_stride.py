from functools import wraps
import json
import uuid

import stride
from flask import Blueprint, request

from .module import Module
from .chatbot import ChatBot

class Stride(stride.Stride):
    def __init__(self, key=None, app=None, url_prefix=''):
        self.stride_key = key
        self.app = app
        super().__init__(cloud_id=None, client_id=None, client_secret=None)
        if app is not None:
            self.init_app(app)
        self.url_prefix = url_prefix
        self.lifecycle = {}
        self.modules = {}
        blueprint_name = 'stride_{}'.format(self.stride_key)
        self._blueprint = Blueprint(blueprint_name, __name__)

    def init_app(self, app):
        # In case we didn't pass the Flask app in the constructor
        if app is not None:
            self.app = app

        if self.stride_key is None:
            self._stride_key = app.config['STRIDE_DESCRIPTOR_KEY']
        self.cloud_id = app.config['STRIDE_CLOUD_ID']
        self.client_id = app.config['STRIDE_CLIENT_ID']
        self.client_secret = app.config['STRIDE_CLIENT_SECRET']

        if 'STRIDE_DESCRIPTOR_URL' in app.config:
            self.descriptor_path = app.config['STRIDE_DESCRIPTOR_URL']
        else:
            self.descriptor_path = '/app-descriptor.json'

        self._blueprint.add_url_rule(self.descriptor_path, 'app_descriptor', self.app_descriptor)

        # This must be done last
        self.app.register_blueprint(self._blueprint, url_prefix=self.url_prefix)

    def _add_module(self, module):
        """Register a module to the app."""
        # Make sure we are dealing with a Module object
        if not isinstance(module, Module):
            pass

        module_type = module.type

        # If this module is the first of its type, we need to add the key to the dict.
        if module_type not in self.modules:
            self.modules[module_type] = []

        self.modules[module_type].append(module)

    def chat_bot(self, key=None, mention_path=None, direct_message_path=None):
        """Decorator for declaring a function to run against a chat:bot module."""
        def module_decorator(func):
            module = ChatBot(key, mention_path, direct_message_path)
            self._add_module(module)

            @self._blueprint.route(mention_path, methods=['POST'])
            @self._blueprint.route(direct_message_path, methods=['POST'])
            @wraps(func)
            def func_wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return func_wrapper
        return module_decorator

    def installed(self, path='/installed'):
        """Decorator for declaring a function to run as part of the install lifecycle."""
        def installed_decorator(func):
            self.lifecycle['installed'] = path
            @self._blueprint.route(path, methods=['POST'])
            @wraps(func)
            def func_wrapper(*args, **kwargs):
                return fun(*args, **kwargs)
            return func_wrapper
        return installed_decorator

    def uninstalled(self, path='/uninstalled'):
        """Decorator for declaring a function to run as part of the uninstall lifecycle."""
        def uninstalled_decorator(func):
            self.lifecycle['uninstalled'] = path
            @self._blueprint.route(path, methods=['POST'])
            @wraps(func)
            def func_wrapper(*args, **kwargs):
                return fun(*args, **kwargs)
            return func_wrapper
        return uninstalled_decorator

    def app_descriptor(self):
        """Generate the app descriptor JSON text that Atlassian Connect is expecting."""
        descriptor = {}
        base_url = 'https://{}/{}'.format(request.host, self.url_prefix)
        descriptor['baseUrl'] = base_url
        descriptor['key'] = self.stride_key
        descriptor['lifecycle'] = {}
        for lifecycle_prop in ['installed', 'uninstalled']:
            if lifecycle_prop in self.lifecycle:
                descriptor['lifecycle'][lifecycle_prop] = self.lifecycle[lifecycle_prop]
            else:
                descriptor['lifecycle'][lifecycle_prop] = '/{}'.format(lifecycle_prop)

        descriptor['modules'] = {}
        for module_type in self.modules:
          descriptor['modules'][module_type] = [ m.to_descriptor() for m in self.modules[module_type] if m is not None ]

        return json.dumps(descriptor)
