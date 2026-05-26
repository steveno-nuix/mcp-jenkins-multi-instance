from typing import Any, Literal

from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.middleware import Middleware as ASGIMiddleware

from mcp_jenkins.core import AuthMiddleware, LifespanContext, lifespan

__all__ = ["mcp"]


class JenkinsMCP(FastMCP[LifespanContext]):
    def http_app(
        self,
        path: str | None = None,
        middleware: list[ASGIMiddleware] | None = None,
        transport: Literal["http", "streamable-http", "sse"] = "http",
        **kwargs: Any,  # noqa: ANN401
    ) -> "Starlette":
        """Override to add JenkinsAuthMiddleware"""
        jenkins_auth_mw = ASGIMiddleware(AuthMiddleware)

        final_middleware_list = [jenkins_auth_mw]
        if middleware:
            final_middleware_list.extend(middleware)

        return super().http_app(
            path=path, middleware=final_middleware_list, transport=transport, **kwargs
        )


mcp = JenkinsMCP("mcp-jenkins", lifespan=lifespan)

# Import tool modules to register them with the MCP server
# This must happen after mcp is created so the @mcp.tool() decorators can reference it
from mcp_jenkins.server import (  # noqa: E402
    build,  # noqa: F401
    instance,  # noqa: F401
    item,  # noqa: F401
    node,  # noqa: F401
    plugin,  # noqa: F401
    queue,  # noqa: F401
    view,  # noqa: F401
)
