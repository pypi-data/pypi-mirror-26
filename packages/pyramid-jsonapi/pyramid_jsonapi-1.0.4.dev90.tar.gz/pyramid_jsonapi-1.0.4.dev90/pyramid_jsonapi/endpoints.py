"""Classes to store and manipulate endpoints and routes."""


class RoutePatternConstructor():
    """Construct pyramid_jsonapi route patterns."""

    def __init__(
            self, sep='/', main_prefix='',
            api_prefix='api', metadata_prefix='metadata'
    ):
        self.sep = sep
        self.main_prefix = main_prefix
        self.api_prefix = api_prefix
        self.metadata_prefix = metadata_prefix

    def pattern_from_components(self, *components):
        """Construct a route pattern from components.

        Join components together with self.sep. Remove all occurrences of '',
        except at the beginning, so that there are no double or trailing
        separators.

        Arguments:
            *components (str): route pattern components.
        """
        components = components or []
        new_comps = []
        for i, component in enumerate(components):
            if component == '' and (i != 0):
                continue
            new_comps.append(component)
        return self.sep.join(new_comps)

    def api_pattern(self, name, *components):
        """Generate a route pattern from a collection name and suffix components.

        Arguments:
            name (str): A collection name.
            *components (str): components to add after collection name.
        """
        return self.pattern_from_components(
            '', self.main_prefix, self.api_prefix, name, *components
        )

    def metadata_pattern(self, metadata_type, *components):
        """Generate a metadata route pattern.

        Arguments:
            metadata_type (str): Metadata type (e.g. swagger, json-schema).
            *components (str): components to add after metadata type.
        """
        return self.pattern_from_components(
            '', self.main_prefix, self.metadata_prefix,
            metadata_type, *components
        )


class EndpointData():
    """Class to hold endpoint data and utility methods.

    Arguments:
        api: A PyramidJSONAPI object.

    """

    def __init__(self, api):
        self.config = api.config
        settings = api.settings
        self.route_name_prefix = settings.route_name_prefix
        self.route_pattern_prefix = settings.route_pattern_prefix
        self.route_name_sep = settings.route_name_sep
        self.route_pattern_sep = settings.route_pattern_sep
        self.api_prefix = ''
        if settings.metadata_endpoints:
            self.api_prefix = settings.route_pattern_api_prefix
        self.metadata_prefix = settings.route_pattern_metadata_prefix
        self.rp_constructor = RoutePatternConstructor(
            sep=self.route_pattern_sep,
            main_prefix=self.route_pattern_prefix,
            api_prefix=self.api_prefix,
            metadata_prefix=self.metadata_prefix,
        )

        # Mapping of endpoints, http_methods and options for constructing routes and views.
        # Update this dictionary prior to calling create_jsonapi()
        # Mandatory 'endpoint' keys: http_methods
        # Optional 'endpoint' keys: route_pattern_suffix
        # Mandatory 'http_method' keys: function
        # Optional 'http_method' keys: renderer
        self.endpoints = {
            'collection': {
                'http_methods': {
                    'GET': {
                        'function': 'collection_get',
                    },
                    'POST': {
                        'function': 'collection_post',
                    },
                },
            },
            'item': {
                'route_pattern_suffix': '{id}',
                'http_methods': {
                    'DELETE': {
                        'function': 'delete',
                    },
                    'GET': {
                        'function': 'get',
                    },
                    'PATCH': {
                        'function': 'patch',
                    },
                },
            },
            'related': {
                'route_pattern_suffix': '{id}/{relationship}',
                'http_methods': {
                    'GET': {
                        'function': 'related_get',
                    },
                },
            },
            'relationships': {
                'route_pattern_suffix': '{id}/relationships/{relationship}',
                'http_methods': {
                    'DELETE': {
                        'function': 'relationships_delete',
                    },
                    'GET': {
                        'function': 'relationships_get',
                    },
                    'PATCH': {
                        'function': 'relationships_patch',
                    },
                    'POST': {
                        'function': 'relationships_post',
                    },
                },
            },
        }

    def make_route_name(self, name, suffix=''):
        """Attach prefix and suffix to name to generate a route_name.

        Arguments:
            name: A pyramid route name.

        Keyword Arguments:
            suffix: An (optional) suffix to append to the route name.
        """
        return self.route_name_sep.join(
            (self.route_name_prefix, name, suffix)
        ).rstrip(self.route_name_sep)

    def add_routes_views(self, view):
        """Generate routes and views from the endpoints data object.

        Arguments:
            view: A view_class to associate routes and views with.
        """

        for endpoint, endpoint_opts in self.endpoints.items():
            route_name = self.make_route_name(
                view.collection_name,
                suffix=endpoint
            )
            route_pattern = self.rp_constructor.api_pattern(
                view.collection_name,
                endpoint_opts.get('route_pattern_suffix', '')
            ).rstrip(self.rp_constructor.sep)
            self.config.add_route(route_name, route_pattern)
            for http_method, method_opts in endpoint_opts['http_methods'].items():
                self.config.add_view(
                    view,
                    attr=method_opts['function'],
                    request_method=http_method,
                    route_name=route_name,
                    renderer=method_opts.get('renderer', 'json')
                )
