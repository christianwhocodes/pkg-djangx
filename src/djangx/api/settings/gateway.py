from ... import PKG_NAME, Conf, ConfField


class ApiGatewayConfig(Conf):
    """api configuration settings."""

    use_asgi = ConfField(env="API_USE_ASGI", toml="api.use-asgi", type=bool, default=False)


_API_GATEWAY = ApiGatewayConfig()

USE_ASGI: bool = _API_GATEWAY.use_asgi

WSGI_APPLICATION: str = f"{PKG_NAME}.api.backends.gateway.wsgi.application"


__all__ = ["USE_ASGI", "WSGI_APPLICATION"]
