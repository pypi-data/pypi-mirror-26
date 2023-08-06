from functools import partial
from inspect import _empty

from ..definitions.base import create_attribute


def create_annotation_lookup(signature, bound_arguments):
    """Combine the signatures annotations with bound arguments to create a lookup dict
    for subsequent functions to identify arguments they need to use"""
    annotations_lookup = {param.name: param.annotation for param in signature.parameters.values()}
    return {annotations_lookup[name]: value for name, value in bound_arguments.items()}


def _arguments(endpoint, param_location):
    return ((parameter['name'], parameter['type']) for parameter in endpoint.parameters if
            parameter['located'] == param_location)


def _create_request_params(self, endpoint, arguments: dict, param_location: str):
    possible_arguments = _arguments(endpoint, param_location)

    def lookup():
        for name, typ in possible_arguments:
            try:
                result = arguments[typ]
            except KeyError:
                try:
                    result = self.default_parameters[typ]
                except KeyError:
                    print(f"WARNING: missing {typ.__name__} in {param_location}")
                    continue
            yield name, result

    return dict(lookup())


def create_url(self, endpoint, arguments):
    endpoint_path = endpoint.path(arguments, default=self.default_parameters)
    host = self.hosts[endpoint.host]
    return host(path=endpoint_path)


def create_body(request_schema, arguments):
    """Create the JSON body to add to the HTTP request

    Args:
        request_schema: -- the endpoints request schema
        arguments: -- dict of user supplied arguments

    Returns:
        Dict containing the formatted data
    """

    # Reverse the request schema to allow for lookups

    def dumps():
        """Iterate over the arguments returning json_dicts of matching objects"""
        for key, value in arguments.items():
            try:
                key = request_schema[key]
            except KeyError:
                continue
            else:
                try:
                    value = value.json_dict()
                except AttributeError:
                    pass
                yield key, value

    return dict(tuple(dumps()))


header_params = partial(_create_request_params, param_location='header')

query_params = partial(_create_request_params, param_location='query')


def construct_arguments(annotation_lookup: dict):
    """Construct passed arguments into corresponding objects"""
    annotation_lookup.pop(_empty, None)  # Remove self parameter
    result = {annotation: create_attribute(annotation, value) for annotation, value in annotation_lookup.items()}
    return result


def create_request_kwargs(self, endpoint, sig, *args, **kwargs):
    """Format arguments to be passed to an aiohttp request"""
    arguments = sig.bind(self, *args, **kwargs).arguments
    arguments = construct_arguments(create_annotation_lookup(sig, arguments))

    json = create_body(endpoint.request_schema, arguments)

    headers = header_params(self, endpoint, arguments)
    url = create_url(self, endpoint, arguments)
    parameters = query_params(self, endpoint, arguments)

    request_kwargs = {
        'method': endpoint.method,
        'url': url,
        'headers': headers,
        'params': parameters,
        'json': json,
    }

    if endpoint.host == 'STREAM':
        request_kwargs.update({'timeout': 0})

    return request_kwargs
