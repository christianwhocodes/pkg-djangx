from os import environ

from .... import PKG_NAME
from ...settings import USE_ASGI

environ.setdefault("DJANGO_SETTINGS_MODULE", f"{PKG_NAME}.settings")

if USE_ASGI:
    from .asgi import application

else:
    from .wsgi import application


__all__ = ["application"]
