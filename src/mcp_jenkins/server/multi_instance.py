"""Multi-instance parallel query tools for MCP Jenkins."""

import asyncio
from typing import Any

from fastmcp import Context

from mcp_jenkins.core.lifespan import jenkins
from mcp_jenkins.server import mcp


@mcp.tool(tags={"read"})
async def get_all_items_multi_instance(
    ctx: Context, instances: list[str] | None = None
) -> dict[str, list[dict[str, Any]] | dict[str, str]]:
    """Get all items from multiple Jenkins instances in parallel.

    Args:
        instances: List of instance names to query. If None, queries all configured instances.

    Returns:
        Dictionary mapping instance names to their items lists or error info.
    """
    lifespan_ctx = ctx.request_context.lifespan_context  # type: ignore[union-attr]
    if not lifespan_ctx.instances:
        msg = "Multi-instance mode not enabled. Use --config-file to enable."
        raise ValueError(msg)

    target_instances = instances or list(lifespan_ctx.instances.instances.keys())

    async def get_items_for_instance(
        instance_name: str,
    ) -> tuple[str, list[dict[str, Any]] | dict[str, str]]:
        try:
            items = [
                item.model_dump(exclude_none=True)
                for item in jenkins(ctx, instance=instance_name).get_items()
            ]
            return instance_name, items
        except Exception as e:  # noqa: BLE001
            return instance_name, {"error": str(e)}

    tasks = [get_items_for_instance(instance) for instance in target_instances]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out exceptions and convert to dict
    valid_results = [r for r in results if not isinstance(r, BaseException)]
    return dict(valid_results)


@mcp.tool(tags={"read"})
async def get_running_builds_multi_instance(
    ctx: Context, instances: list[str] | None = None
) -> dict[str, list[dict[str, Any]] | dict[str, str]]:
    """Get running builds from multiple Jenkins instances in parallel.

    Args:
        instances: List of instance names to query. If None, queries all configured instances.

    Returns:
        Dictionary mapping instance names to their running builds lists or error info.
    """
    lifespan_ctx = ctx.request_context.lifespan_context  # type: ignore[union-attr]
    if not lifespan_ctx.instances:
        msg = "Multi-instance mode not enabled. Use --config-file to enable."
        raise ValueError(msg)

    target_instances = instances or list(lifespan_ctx.instances.instances.keys())

    async def get_builds_for_instance(
        instance_name: str,
    ) -> tuple[str, list[dict[str, Any]] | dict[str, str]]:
        try:
            builds = [
                build.model_dump(exclude_none=True)
                for build in jenkins(ctx, instance=instance_name).get_running_builds()
            ]
            return instance_name, builds
        except Exception as e:  # noqa: BLE001
            return instance_name, {"error": str(e)}

    tasks = [get_builds_for_instance(instance) for instance in target_instances]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out exceptions and convert to dict
    valid_results = [r for r in results if not isinstance(r, BaseException)]
    return dict(valid_results)


@mcp.tool(tags={"read"})
async def get_all_nodes_multi_instance(
    ctx: Context, instances: list[str] | None = None
) -> dict[str, list[dict[str, Any]] | dict[str, str]]:
    """Get all nodes from multiple Jenkins instances in parallel.

    Args:
        instances: List of instance names to query. If None, queries all configured instances.

    Returns:
        Dictionary mapping instance names to their nodes lists or error info.
    """
    lifespan_ctx = ctx.request_context.lifespan_context  # type: ignore[union-attr]
    if not lifespan_ctx.instances:
        msg = "Multi-instance mode not enabled. Use --config-file to enable."
        raise ValueError(msg)

    target_instances = instances or list(lifespan_ctx.instances.instances.keys())

    async def get_nodes_for_instance(
        instance_name: str,
    ) -> tuple[str, list[dict[str, Any]] | dict[str, str]]:
        try:
            nodes = [
                node.model_dump(exclude_none=True)
                for node in jenkins(ctx, instance=instance_name).get_nodes()
            ]
            return instance_name, nodes
        except Exception as e:  # noqa: BLE001
            return instance_name, {"error": str(e)}

    tasks = [get_nodes_for_instance(instance) for instance in target_instances]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out exceptions and convert to dict
    valid_results = [r for r in results if not isinstance(r, BaseException)]
    return dict(valid_results)


@mcp.tool(tags={"read"})
async def get_all_queue_items_multi_instance(
    ctx: Context, instances: list[str] | None = None
) -> dict[str, list[dict[str, Any]] | dict[str, str]]:
    """Get all queue items from multiple Jenkins instances in parallel.

    Args:
        instances: List of instance names to query. If None, queries all configured instances.

    Returns:
        Dictionary mapping instance names to their queue items lists or error info.
    """
    lifespan_ctx = ctx.request_context.lifespan_context  # type: ignore[union-attr]
    if not lifespan_ctx.instances:
        msg = "Multi-instance mode not enabled. Use --config-file to enable."
        raise ValueError(msg)

    target_instances = instances or list(lifespan_ctx.instances.instances.keys())

    async def get_queue_for_instance(
        instance_name: str,
    ) -> tuple[str, list[dict[str, Any]] | dict[str, str]]:
        try:
            queue_items = [
                item.model_dump(exclude_none=True)
                for item in jenkins(ctx, instance=instance_name).get_queue().items
            ]
            return instance_name, queue_items
        except Exception as e:  # noqa: BLE001
            return instance_name, {"error": str(e)}

    tasks = [get_queue_for_instance(instance) for instance in target_instances]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out exceptions and convert to dict
    valid_results = [r for r in results if not isinstance(r, BaseException)]
    return dict(valid_results)


@mcp.tool(tags={"read"})
async def query_items_multi_instance(
    ctx: Context,
    instances: list[str] | None = None,
    class_pattern: str | None = None,
    fullname_pattern: str | None = None,
    color_pattern: str | None = None,
    folder_depth: int | None = None,
) -> dict[str, list[dict[str, Any]] | dict[str, str]]:
    """Query items from multiple Jenkins instances in parallel with filters.

    Args:
        instances: List of instance names to query. If None, queries all configured instances.
        class_pattern: The pattern of the _class
        fullname_pattern: The pattern of the fullname
        color_pattern: The pattern of the color
        folder_depth: The maximum depth of folders to traverse. If None, traverses all levels.

    Returns:
        Dictionary mapping instance names to their filtered items lists or error info.
    """
    lifespan_ctx = ctx.request_context.lifespan_context  # type: ignore[union-attr]
    if not lifespan_ctx.instances:
        msg = "Multi-instance mode not enabled. Use --config-file to enable."
        raise ValueError(msg)

    target_instances = instances or list(lifespan_ctx.instances.instances.keys())

    async def query_items_for_instance(
        instance_name: str,
    ) -> tuple[str, list[dict[str, Any]] | dict[str, str]]:
        try:
            items = [
                item.model_dump(exclude_none=True)
                for item in jenkins(ctx, instance=instance_name).query_items(
                    class_pattern=class_pattern,
                    fullname_pattern=fullname_pattern,
                    color_pattern=color_pattern,
                    folder_depth=folder_depth,
                )
            ]
            return instance_name, items
        except Exception as e:  # noqa: BLE001
            return instance_name, {"error": str(e)}

    tasks = [query_items_for_instance(instance) for instance in target_instances]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Filter out exceptions and convert to dict
    valid_results = [r for r in results if not isinstance(r, BaseException)]
    return dict(valid_results)
