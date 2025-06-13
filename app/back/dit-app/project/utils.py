from collections import OrderedDict


def validate_from_request(serializer, request, *, attr='data', instance=None, data=None, **kwargs):
    if attr not in ['data', 'query_params']:
        return OrderedDict()
    instance = None if attr == 'query_params' else instance
    input_data = data or getattr(request, attr, {})
    _serializer = serializer(instance=instance, data=input_data, context={'request': request}, **kwargs)
    _serializer.is_valid(raise_exception=True)
    validated_data = _serializer.validated_data
    return validated_data