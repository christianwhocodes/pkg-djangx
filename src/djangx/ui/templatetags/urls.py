from django.template import Library

from ..settings import ADMIN_URL, HOME_URL, MEDIA_URL, STATIC_URL

register = Library()


@register.simple_tag
def home_url() -> str:
    """Get the home URL."""

    return HOME_URL


@register.simple_tag
def admin_url() -> str:
    """Get the admin URL."""

    return ADMIN_URL


@register.simple_tag
def static_url() -> str:
    """Get the static URL."""

    return STATIC_URL


@register.simple_tag
def media_url() -> str:
    """Get the media URL."""

    return MEDIA_URL
