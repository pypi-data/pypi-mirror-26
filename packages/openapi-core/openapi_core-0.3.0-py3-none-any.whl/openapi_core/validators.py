"""OpenAPI core validators module"""
from six import iteritems

from openapi_core.exceptions import (
    OpenAPIMappingError, MissingParameter, MissingBody,
)


class RequestParameters(dict):

    valid_locations = ['path', 'query', 'headers', 'cookies']

    def __getitem__(self, location):
        self.validate_location(location)

        return self.setdefault(location, {})

    def __setitem__(self, location, value):
        raise NotImplementedError

    @classmethod
    def validate_location(cls, location):
        if location not in cls.valid_locations:
            raise OpenAPIMappingError(
                "Unknown parameter location: {0}".format(str(location)))


class BaseValidationResult(object):

    def __init__(self, errors):
        self.errors = errors

    def raise_for_errors(self):
        for error in self.errors:
            raise error


class RequestValidationResult(BaseValidationResult):

    def __init__(self, errors, body=None, parameters=None):
        super(RequestValidationResult, self).__init__(errors)
        self.body = body
        self.parameters = parameters or RequestParameters()


class RequestValidator(object):

    def __init__(self, spec):
        self.spec = spec

    def validate(self, request):
        errors = []
        body = None
        parameters = RequestParameters()

        try:
            server = self.spec.get_server(request.full_url_pattern)
        # don't process if server errors
        except OpenAPIMappingError as exc:
            errors.append(exc)
            return RequestValidationResult(errors, body, parameters)

        operation_pattern = request.full_url_pattern.replace(
            server.default_url, '')

        try:
            operation = self.spec.get_operation(
                operation_pattern, request.method)
        # don't process if operation errors
        except OpenAPIMappingError as exc:
            errors.append(exc)
            return RequestValidationResult(errors, body, parameters)

        for param_name, param in iteritems(operation.parameters):
            try:
                raw_value = self._get_raw_value(request, param)
            except MissingParameter as exc:
                if param.required:
                    errors.append(exc)

                if not param.schema or param.schema.default is None:
                    continue
                raw_value = param.schema.default

            try:
                value = param.unmarshal(raw_value)
            except OpenAPIMappingError as exc:
                errors.append(exc)
            else:
                parameters[param.location][param_name] = value

        if operation.request_body is not None:
            try:
                media_type = operation.request_body[request.mimetype]
            except OpenAPIMappingError as exc:
                errors.append(exc)
            else:
                try:
                    raw_body = self._get_raw_body(request)
                except MissingBody as exc:
                    if operation.request_body.required:
                        errors.append(exc)
                else:
                    try:
                        body = media_type.unmarshal(raw_body)
                    except OpenAPIMappingError as exc:
                        errors.append(exc)

        return RequestValidationResult(errors, body, parameters)

    def _get_raw_value(self, request, param):
        try:
            return request.parameters[param.location][param.name]
        except KeyError:
            raise MissingParameter(
                "Missing required `{0}` parameter".format(param.name))

    def _get_raw_body(self, request):
        if not request.body:
            raise MissingBody("Missing required request body")

        return request.body
