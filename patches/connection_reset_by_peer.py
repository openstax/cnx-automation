import urllib3

from selenium.webdriver.remote.remote_connection import (
    RemoteConnection,
    parse,
    common_utils,
    Command,
    LOGGER,
)


def __init__(self, remote_server_addr, keep_alive=False, resolve_ip=True):
    # Attempt to resolve the hostname and get an IP address.
    self.keep_alive = keep_alive
    parsed_url = parse.urlparse(remote_server_addr)
    if parsed_url.hostname and resolve_ip:
        port = parsed_url.port or None
        if parsed_url.scheme == "https":
            ip = parsed_url.hostname
        else:
            ip = common_utils.find_connectable_ip(parsed_url.hostname, port=port)
        if ip:
            netloc = ip
            if parsed_url.port:
                netloc = common_utils.join_host_port(netloc, parsed_url.port)
            if parsed_url.username:
                auth = parsed_url.username
                if parsed_url.password:
                    auth += ":%s" % parsed_url.password
                netloc = "%s@%s" % (auth, netloc)
            remote_server_addr = parse.urlunparse(
                (
                    parsed_url.scheme,
                    netloc,
                    parsed_url.path,
                    parsed_url.params,
                    parsed_url.query,
                    parsed_url.fragment,
                )
            )
        else:
            LOGGER.info("Could not get IP address for host: %s" % parsed_url.hostname)

    self._url = remote_server_addr
    if keep_alive:
        self._conn = urllib3.PoolManager()

    self._commands = {
        Command.STATUS: ("GET", "/status"),
        Command.NEW_SESSION: ("POST", "/session"),
        Command.GET_ALL_SESSIONS: ("GET", "/sessions"),
        Command.QUIT: ("DELETE", "/session/$sessionId"),
        Command.GET_CURRENT_WINDOW_HANDLE: ("GET", "/session/$sessionId/window_handle"),
        Command.W3C_GET_CURRENT_WINDOW_HANDLE: ("GET", "/session/$sessionId/window"),
        Command.GET_WINDOW_HANDLES: ("GET", "/session/$sessionId/window_handles"),
        Command.W3C_GET_WINDOW_HANDLES: ("GET", "/session/$sessionId/window/handles"),
        Command.GET: ("POST", "/session/$sessionId/url"),
        Command.GO_FORWARD: ("POST", "/session/$sessionId/forward"),
        Command.GO_BACK: ("POST", "/session/$sessionId/back"),
        Command.REFRESH: ("POST", "/session/$sessionId/refresh"),
        Command.EXECUTE_SCRIPT: ("POST", "/session/$sessionId/execute"),
        Command.W3C_EXECUTE_SCRIPT: ("POST", "/session/$sessionId/execute/sync"),
        Command.W3C_EXECUTE_SCRIPT_ASYNC: ("POST", "/session/$sessionId/execute/async"),
        Command.GET_CURRENT_URL: ("GET", "/session/$sessionId/url"),
        Command.GET_TITLE: ("GET", "/session/$sessionId/title"),
        Command.GET_PAGE_SOURCE: ("GET", "/session/$sessionId/source"),
        Command.SCREENSHOT: ("GET", "/session/$sessionId/screenshot"),
        Command.ELEMENT_SCREENSHOT: ("GET", "/session/$sessionId/element/$id/screenshot"),
        Command.FIND_ELEMENT: ("POST", "/session/$sessionId/element"),
        Command.FIND_ELEMENTS: ("POST", "/session/$sessionId/elements"),
        Command.W3C_GET_ACTIVE_ELEMENT: ("GET", "/session/$sessionId/element/active"),
        Command.GET_ACTIVE_ELEMENT: ("POST", "/session/$sessionId/element/active"),
        Command.FIND_CHILD_ELEMENT: ("POST", "/session/$sessionId/element/$id/element"),
        Command.FIND_CHILD_ELEMENTS: ("POST", "/session/$sessionId/element/$id/elements"),
        Command.CLICK_ELEMENT: ("POST", "/session/$sessionId/element/$id/click"),
        Command.CLEAR_ELEMENT: ("POST", "/session/$sessionId/element/$id/clear"),
        Command.SUBMIT_ELEMENT: ("POST", "/session/$sessionId/element/$id/submit"),
        Command.GET_ELEMENT_TEXT: ("GET", "/session/$sessionId/element/$id/text"),
        Command.SEND_KEYS_TO_ELEMENT: ("POST", "/session/$sessionId/element/$id/value"),
        Command.SEND_KEYS_TO_ACTIVE_ELEMENT: ("POST", "/session/$sessionId/keys"),
        Command.UPLOAD_FILE: ("POST", "/session/$sessionId/file"),
        Command.GET_ELEMENT_VALUE: ("GET", "/session/$sessionId/element/$id/value"),
        Command.GET_ELEMENT_TAG_NAME: ("GET", "/session/$sessionId/element/$id/name"),
        Command.IS_ELEMENT_SELECTED: ("GET", "/session/$sessionId/element/$id/selected"),
        Command.SET_ELEMENT_SELECTED: ("POST", "/session/$sessionId/element/$id/selected"),
        Command.IS_ELEMENT_ENABLED: ("GET", "/session/$sessionId/element/$id/enabled"),
        Command.IS_ELEMENT_DISPLAYED: ("GET", "/session/$sessionId/element/$id/displayed"),
        Command.GET_ELEMENT_LOCATION: ("GET", "/session/$sessionId/element/$id/location"),
        Command.GET_ELEMENT_LOCATION_ONCE_SCROLLED_INTO_VIEW: (
            "GET",
            "/session/$sessionId/element/$id/location_in_view",
        ),
        Command.GET_ELEMENT_SIZE: ("GET", "/session/$sessionId/element/$id/size"),
        Command.GET_ELEMENT_RECT: ("GET", "/session/$sessionId/element/$id/rect"),
        Command.GET_ELEMENT_ATTRIBUTE: ("GET", "/session/$sessionId/element/$id/attribute/$name"),
        Command.GET_ELEMENT_PROPERTY: ("GET", "/session/$sessionId/element/$id/property/$name"),
        Command.ELEMENT_EQUALS: ("GET", "/session/$sessionId/element/$id/equals/$other"),
        Command.GET_ALL_COOKIES: ("GET", "/session/$sessionId/cookie"),
        Command.ADD_COOKIE: ("POST", "/session/$sessionId/cookie"),
        Command.DELETE_ALL_COOKIES: ("DELETE", "/session/$sessionId/cookie"),
        Command.DELETE_COOKIE: ("DELETE", "/session/$sessionId/cookie/$name"),
        Command.SWITCH_TO_FRAME: ("POST", "/session/$sessionId/frame"),
        Command.SWITCH_TO_PARENT_FRAME: ("POST", "/session/$sessionId/frame/parent"),
        Command.SWITCH_TO_WINDOW: ("POST", "/session/$sessionId/window"),
        Command.CLOSE: ("DELETE", "/session/$sessionId/window"),
        Command.GET_ELEMENT_VALUE_OF_CSS_PROPERTY: (
            "GET",
            "/session/$sessionId/element/$id/css/$propertyName",
        ),
        Command.IMPLICIT_WAIT: ("POST", "/session/$sessionId/timeouts/implicit_wait"),
        Command.EXECUTE_ASYNC_SCRIPT: ("POST", "/session/$sessionId/execute_async"),
        Command.SET_SCRIPT_TIMEOUT: ("POST", "/session/$sessionId/timeouts/async_script"),
        Command.SET_TIMEOUTS: ("POST", "/session/$sessionId/timeouts"),
        Command.DISMISS_ALERT: ("POST", "/session/$sessionId/dismiss_alert"),
        Command.W3C_DISMISS_ALERT: ("POST", "/session/$sessionId/alert/dismiss"),
        Command.ACCEPT_ALERT: ("POST", "/session/$sessionId/accept_alert"),
        Command.W3C_ACCEPT_ALERT: ("POST", "/session/$sessionId/alert/accept"),
        Command.SET_ALERT_VALUE: ("POST", "/session/$sessionId/alert_text"),
        Command.W3C_SET_ALERT_VALUE: ("POST", "/session/$sessionId/alert/text"),
        Command.GET_ALERT_TEXT: ("GET", "/session/$sessionId/alert_text"),
        Command.W3C_GET_ALERT_TEXT: ("GET", "/session/$sessionId/alert/text"),
        Command.SET_ALERT_CREDENTIALS: ("POST", "/session/$sessionId/alert/credentials"),
        Command.CLICK: ("POST", "/session/$sessionId/click"),
        Command.W3C_ACTIONS: ("POST", "/session/$sessionId/actions"),
        Command.W3C_CLEAR_ACTIONS: ("DELETE", "/session/$sessionId/actions"),
        Command.DOUBLE_CLICK: ("POST", "/session/$sessionId/doubleclick"),
        Command.MOUSE_DOWN: ("POST", "/session/$sessionId/buttondown"),
        Command.MOUSE_UP: ("POST", "/session/$sessionId/buttonup"),
        Command.MOVE_TO: ("POST", "/session/$sessionId/moveto"),
        Command.GET_WINDOW_SIZE: ("GET", "/session/$sessionId/window/$windowHandle/size"),
        Command.SET_WINDOW_SIZE: ("POST", "/session/$sessionId/window/$windowHandle/size"),
        Command.GET_WINDOW_POSITION: ("GET", "/session/$sessionId/window/$windowHandle/position"),
        Command.SET_WINDOW_POSITION: ("POST", "/session/$sessionId/window/$windowHandle/position"),
        Command.SET_WINDOW_RECT: ("POST", "/session/$sessionId/window/rect"),
        Command.GET_WINDOW_RECT: ("GET", "/session/$sessionId/window/rect"),
        Command.MAXIMIZE_WINDOW: ("POST", "/session/$sessionId/window/$windowHandle/maximize"),
        Command.W3C_MAXIMIZE_WINDOW: ("POST", "/session/$sessionId/window/maximize"),
        Command.SET_SCREEN_ORIENTATION: ("POST", "/session/$sessionId/orientation"),
        Command.GET_SCREEN_ORIENTATION: ("GET", "/session/$sessionId/orientation"),
        Command.SINGLE_TAP: ("POST", "/session/$sessionId/touch/click"),
        Command.TOUCH_DOWN: ("POST", "/session/$sessionId/touch/down"),
        Command.TOUCH_UP: ("POST", "/session/$sessionId/touch/up"),
        Command.TOUCH_MOVE: ("POST", "/session/$sessionId/touch/move"),
        Command.TOUCH_SCROLL: ("POST", "/session/$sessionId/touch/scroll"),
        Command.DOUBLE_TAP: ("POST", "/session/$sessionId/touch/doubleclick"),
        Command.LONG_PRESS: ("POST", "/session/$sessionId/touch/longclick"),
        Command.FLICK: ("POST", "/session/$sessionId/touch/flick"),
        Command.EXECUTE_SQL: ("POST", "/session/$sessionId/execute_sql"),
        Command.GET_LOCATION: ("GET", "/session/$sessionId/location"),
        Command.SET_LOCATION: ("POST", "/session/$sessionId/location"),
        Command.GET_APP_CACHE: ("GET", "/session/$sessionId/application_cache"),
        Command.GET_APP_CACHE_STATUS: ("GET", "/session/$sessionId/application_cache/status"),
        Command.CLEAR_APP_CACHE: ("DELETE", "/session/$sessionId/application_cache/clear"),
        Command.GET_NETWORK_CONNECTION: ("GET", "/session/$sessionId/network_connection"),
        Command.SET_NETWORK_CONNECTION: ("POST", "/session/$sessionId/network_connection"),
        Command.GET_LOCAL_STORAGE_ITEM: ("GET", "/session/$sessionId/local_storage/key/$key"),
        Command.REMOVE_LOCAL_STORAGE_ITEM: ("DELETE", "/session/$sessionId/local_storage/key/$key"),
        Command.GET_LOCAL_STORAGE_KEYS: ("GET", "/session/$sessionId/local_storage"),
        Command.SET_LOCAL_STORAGE_ITEM: ("POST", "/session/$sessionId/local_storage"),
        Command.CLEAR_LOCAL_STORAGE: ("DELETE", "/session/$sessionId/local_storage"),
        Command.GET_LOCAL_STORAGE_SIZE: ("GET", "/session/$sessionId/local_storage/size"),
        Command.GET_SESSION_STORAGE_ITEM: ("GET", "/session/$sessionId/session_storage/key/$key"),
        Command.REMOVE_SESSION_STORAGE_ITEM: (
            "DELETE",
            "/session/$sessionId/session_storage/key/$key",
        ),
        Command.GET_SESSION_STORAGE_KEYS: ("GET", "/session/$sessionId/session_storage"),
        Command.SET_SESSION_STORAGE_ITEM: ("POST", "/session/$sessionId/session_storage"),
        Command.CLEAR_SESSION_STORAGE: ("DELETE", "/session/$sessionId/session_storage"),
        Command.GET_SESSION_STORAGE_SIZE: ("GET", "/session/$sessionId/session_storage/size"),
        Command.GET_LOG: ("POST", "/session/$sessionId/log"),
        Command.GET_AVAILABLE_LOG_TYPES: ("GET", "/session/$sessionId/log/types"),
        Command.CURRENT_CONTEXT_HANDLE: ("GET", "/session/$sessionId/context"),
        Command.CONTEXT_HANDLES: ("GET", "/session/$sessionId/contexts"),
        Command.SWITCH_TO_CONTEXT: ("POST", "/session/$sessionId/context"),
        Command.FULLSCREEN_WINDOW: ("POST", "/session/$sessionId/window/fullscreen"),
        Command.MINIMIZE_WINDOW: ("POST", "/session/$sessionId/window/minimize"),
    }


RemoteConnection.__init__ = __init__
