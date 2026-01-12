from enum import StrEnum

from ... import PKG_NAME, Conf, ConfField
from ..types import TemplatesDict

# ===============================================================
# Apps
# ===============================================================


class _Apps(StrEnum):
    """Django applications enumeration."""

    ADMIN = "django.contrib.admin"
    AUTH = "django.contrib.auth"
    CONTENTTYPES = "django.contrib.contenttypes"
    SESSIONS = "django.contrib.sessions"
    MESSAGES = "django.contrib.messages"
    STATICFILES = "django.contrib.staticfiles"
    BROWSER_RELOAD = "django_browser_reload"
    WATCHFILES = "django_watchfiles"


class AppsConf(Conf):
    """Apps configuration settings."""

    extend = ConfField(env="APPS_EXTEND", toml="apps.extend", type=list)
    remove = ConfField(env="APPS_REMOVE", toml="apps.remove", type=list)


_APPS_CONF = AppsConf()


def _get_installed_apps() -> list[str]:
    """Build the final list of installed Django applications."""
    base_apps: list[str] = [f"{PKG_NAME}.cli", f"{PKG_NAME}.ui", "app"]

    django_apps: list[str] = [
        _Apps.ADMIN,
        _Apps.AUTH,
        _Apps.CONTENTTYPES,
        _Apps.SESSIONS,
        _Apps.MESSAGES,
        _Apps.STATICFILES,
        _Apps.BROWSER_RELOAD,
        _Apps.WATCHFILES,
    ]

    # Collect apps that should be removed except for base apps
    apps_to_remove = [app for app in _APPS_CONF.remove if app not in base_apps]

    # Remove apps that are in the remove list
    django_apps = [app for app in django_apps if app not in apps_to_remove]

    # Add custom apps
    all_apps = base_apps + django_apps + _APPS_CONF.extend

    # Remove duplicates while preserving order
    return list(dict.fromkeys(all_apps))


INSTALLED_APPS: list[str] = _get_installed_apps()


# ===============================================================
# TEMPLATES & CONTEXT PROCESSORS
# ===============================================================


class _ContextProcessors(StrEnum):
    """Django template context processors enumeration."""

    CSP = "django.template.context_processors.csp"
    REQUEST = "django.template.context_processors.request"
    AUTH = "django.contrib.auth.context_processors.auth"
    MESSAGES = "django.contrib.messages.context_processors.messages"


_APP_CONTEXT_PROCESSOR_MAP: dict[_Apps, list[_ContextProcessors]] = {
    _Apps.AUTH: [_ContextProcessors.AUTH],
    _Apps.MESSAGES: [_ContextProcessors.MESSAGES],
}


class ContextProcessorsConf(Conf):
    """Context processors configuration settings."""

    extend = ConfField(
        env="CONTEXT_PROCESSORS_EXTEND",
        toml="context-processors.extend",
        type=list,
    )
    remove = ConfField(
        env="CONTEXT_PROCESSORS_REMOVE",
        toml="context-processors.remove",
        type=list,
    )


_CONTEXT_PROCESSORS_CONF = ContextProcessorsConf()


def _get_context_processors(installed_apps: list[str]) -> list[str]:
    """Build the final list of context processors based on installed apps."""
    base_context_processors: list[str] = [
        _ContextProcessors.CSP,
        _ContextProcessors.REQUEST,
        _ContextProcessors.AUTH,
        _ContextProcessors.MESSAGES,
    ]

    # Collect context processors that should be removed based on missing apps
    context_processors_to_remove: set[str] = set(_CONTEXT_PROCESSORS_CONF.remove)
    for app, processor_list in _APP_CONTEXT_PROCESSOR_MAP.items():
        if app not in installed_apps:
            context_processors_to_remove.update(processor_list)

    # Filter out context processors whose apps are not installed or explicitly removed
    base_context_processors = [
        cp for cp in base_context_processors if cp not in context_processors_to_remove
    ]

    # Add custom context processors
    all_context_processors = base_context_processors + _CONTEXT_PROCESSORS_CONF.extend

    # Remove duplicates while preserving order
    return list(dict.fromkeys(all_context_processors))


TEMPLATES: TemplatesDict = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": _get_context_processors(INSTALLED_APPS),
            "builtins": [f"{PKG_NAME}.ui.templatetags.org"],
        },
    },
]


# ===============================================================
# MIDDLEWARE
# ===============================================================


class _Middlewares(StrEnum):
    """Django middleware enumeration."""

    SECURITY = "django.middleware.security.SecurityMiddleware"
    SESSION = "django.contrib.sessions.middleware.SessionMiddleware"
    COMMON = "django.middleware.common.CommonMiddleware"
    CSRF = "django.middleware.csrf.CsrfViewMiddleware"
    AUTH = "django.contrib.auth.middleware.AuthenticationMiddleware"
    MESSAGES = "django.contrib.messages.middleware.MessageMiddleware"
    CLICKJACKING = "django.middleware.clickjacking.XFrameOptionsMiddleware"
    CSP = "django.middleware.csp.ContentSecurityPolicyMiddleware"
    BROWSER_RELOAD = "django_browser_reload.middleware.BrowserReloadMiddleware"


_APP_MIDDLEWARE_MAP: dict[_Apps, list[_Middlewares]] = {
    _Apps.SESSIONS: [_Middlewares.SESSION],
    _Apps.AUTH: [_Middlewares.AUTH],
    _Apps.MESSAGES: [_Middlewares.MESSAGES],
    _Apps.BROWSER_RELOAD: [_Middlewares.BROWSER_RELOAD],
}


class MiddlewareConf(Conf):
    """Middleware configuration settings."""

    extend = ConfField(env="MIDDLEWARE_EXTEND", toml="middleware.extend", type=list)
    remove = ConfField(env="MIDDLEWARE_REMOVE", toml="middleware.remove", type=list)


_MIDDLEWARE_CONF = MiddlewareConf()


def _get_middleware(installed_apps: list[str]) -> list[str]:
    """Build the final list of middleware based on installed apps."""
    base_middleware: list[str] = [
        _Middlewares.SECURITY,
        _Middlewares.SESSION,
        _Middlewares.COMMON,
        _Middlewares.CSRF,
        _Middlewares.AUTH,
        _Middlewares.MESSAGES,
        _Middlewares.CLICKJACKING,
        _Middlewares.CSP,
        _Middlewares.BROWSER_RELOAD,
    ]

    # Collect middleware that should be removed based on missing apps
    middleware_to_remove: set[str] = set(_MIDDLEWARE_CONF.remove)
    for app, middleware_list in _APP_MIDDLEWARE_MAP.items():
        if app not in installed_apps:
            middleware_to_remove.update(middleware_list)

    # Filter out middleware whose apps are not installed or explicitly removed
    base_middleware = [m for m in base_middleware if m not in middleware_to_remove]

    # Add custom middleware
    all_middleware = base_middleware + _MIDDLEWARE_CONF.extend

    # Remove duplicates while preserving order
    return list(dict.fromkeys(all_middleware))


MIDDLEWARE: list[str] = _get_middleware(INSTALLED_APPS)


# ===============================================================
# ROOT URLCONF
# ===============================================================

ROOT_URLCONF: str = f"{PKG_NAME}.ui.urls"


# ===============================================================
# EXPORTS
# ===============================================================

__all__ = ["INSTALLED_APPS", "TEMPLATES", "MIDDLEWARE", "ROOT_URLCONF"]
