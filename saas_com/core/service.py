from django.contrib.contenttypes.models import ContentType
from .exceptions import InvalidContentType
from django.utils.http import url_has_allowed_host_and_scheme

def get_content_type(content_type_str , valid_content_types):
    if content_type_str not in valid_content_types:
        raise InvalidContentType("Invalid content type")
    return ContentType.objects.get_for_model(valid_content_types[content_type_str])

def is_safe_url(url , allowed_hosts):
    if url_has_allowed_host_and_scheme(url , allowed_hosts = allowed_hosts):
        return url
    return "/"