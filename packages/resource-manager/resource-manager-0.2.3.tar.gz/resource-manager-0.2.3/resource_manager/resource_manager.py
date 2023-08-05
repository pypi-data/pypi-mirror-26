import functools
import json
import os
import warnings
from collections import OrderedDict

from .tree_analysis import SyntaxTree
from .parser import parse_file
from .structures import *


class ResourceManager:
    def __init__(self, source_path: str, get_module: callable):
        self.get_module = get_module
        # this information is redundant for now
        self._imported = OrderedDict()
        self._defined_resources = {}
        self._request_stack = []
        # TODO: no need for stack
        self._modules_stack = []
        self._undefined_resources = {}

        source_path = os.path.realpath(source_path)
        self._import(source_path)

        tree = SyntaxTree(self._undefined_resources)
        message = ''
        if tree.cycles:
            message += 'Cyclic dependency found in the following resources:\n    ' \
                       '{}'.format('\n    '.join(tree.cycles))
        if tree.undefined:
            message += '\nUndefined resources found:\n    {}'.format(', '.join(tree.undefined))
        if message:
            raise RuntimeError(message)

    def __getattribute__(self, name: str):
        # TODO: looks kinda ugly. not sure if it's worth it
        try:
            value = super().__getattribute__(name)
            if value is not TempPlaceholder:
                return value
        except AttributeError:
            pass
        # a whole new request, so clear the stack
        self._request_stack = []
        return self._get_resource(name)
        # self._modules_stack = []
        # try:
        # except BaseException as e:
        # module_type, module_name = self._modules_stack[-1]
        # raise RuntimeError('An exception occurred while building the resource ' +
        # '%s:%s (Line %d)' % (module_type.body, module_name.body, module_type.line)) from e

    def get(self, name: str, default=None):
        try:
            return getattr(self, name)
        except AttributeError:
            return default

    def set(self, name, value, override=False):
        warnings.warn("Manually modifying the ResourceManager's state is highly not recommended", RuntimeWarning)
        if name in self._defined_resources and not override:
            raise RuntimeError('Attempt to overwrite resource {}'.format(name))
        self._defined_resources[name] = value
        self._add_to_dict(name, value)

    def save_config(self, path):
        with open(path, 'w') as file:
            file.write(self._get_whole_config())

    def _get_whole_config(self):
        result = ''
        for name, value in self._undefined_resources.items():
            result += '{} = {}\n\n'.format(name, value.to_str(0))

        return result[:-1]

    def _add_to_dict(self, name, value):
        # adding support for interactive shells and notebooks:
        # TODO: this may be ugly, but is the only way I found to avoid triggering getattr
        if name not in self.__dict__:
            setattr(self, name, value)

    def _import(self, absolute_path):
        if absolute_path in self._imported:
            return
        self._imported[absolute_path] = None

        definitions, parents = parse_file(absolute_path)
        result = {}
        for definition in definitions:
            def_name = definition.name.body
            if def_name in result:
                raise SyntaxError('Duplicate definition of resource "{}" '
                                  'in config file {}'.format(def_name, absolute_path))
            result[def_name] = definition.value

            if def_name not in self._undefined_resources:
                self._undefined_resources[def_name] = definition.value
                self._add_to_dict(def_name, TempPlaceholder)

        for parent in parents:
            parent = os.path.join(os.path.dirname(absolute_path), parent)
            self._import(parent)

        self._imported[absolute_path] = result

    def _get_resource(self, name: str):
        if name in self._defined_resources:
            return self._defined_resources[name]
        # avoiding cycles
        if name in self._request_stack:
            self._request_stack = []
            prefix = " -> ".join(self._request_stack)
            raise RuntimeError('Cyclic dependency found in the following resource:\n  '
                               '{} -> {}'.format(prefix, name))
        self._request_stack.append(name)

        try:
            node = self._undefined_resources[name]
        except KeyError:
            raise AttributeError('Resource "{}" is not defined'.format(name)) from None

        resource = self._define_resource(node)
        self._defined_resources[name] = resource

        self._request_stack.pop()
        return resource

    def _define_resource(self, node):
        if type(node) is Value:
            return json.loads(node.value.body)
        if type(node) is Array:
            return [self._define_resource(x) for x in node.values]
        if type(node) is Dictionary:
            return {json.loads(name.body): self._define_resource(value) for name, value in node.dictionary.items()}
        if type(node) is Resource:
            return self._get_resource(node.name.body)
        if type(node) is GetAttribute:
            data = self._define_resource(node.data)
            return getattr(data, node.name.body)
        if type(node) is Module:
            # self._modules_stack.append((node.module_type, node.module_name))
            result = self.get_module(node.module_type.body, node.module_name.body)
            # self._modules_stack.pop()
            return result
        if type(node) is Partial:
            target = self._define_resource(node.target)
            kwargs = {param.name.body: self._define_resource(param.value) for param in node.params}
            if node.lazy:
                return functools.partial(target, **kwargs)
            else:
                return target(**kwargs)

        raise TypeError('Undefined resource description of type {}'.format(type(node)))


class TempPlaceholder:
    pass
