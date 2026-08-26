import base64
from typing import Any

from fastmcp import Context

from mcp_jenkins.core.lifespan import jenkins
from mcp_jenkins.jenkins.model.item import FreeStyleProject, Job, MultiBranchProject
from mcp_jenkins.server import mcp


@mcp.tool(tags={"read"})
async def get_running_builds(
    ctx: Context, instance: str | None = None
) -> list[dict[str, Any]]:
    """Get all running builds from Jenkins

    Args:
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        A list of all running builds
    """
    return [
        item.model_dump(include={"number", "url", "building", "timestamp"})
        for item in jenkins(ctx, instance=instance).get_running_builds()
    ]


@mcp.tool(tags={"read"})
async def get_build(
    ctx: Context, fullname: str, number: int | None = None, instance: str | None = None
) -> dict[str, Any]:
    """Get specific build info from Jenkins

    Args:
        fullname: The fullname of the job
        number: The number of the build, if None, get the last build
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        The build info
    """
    if number is None:
        item = jenkins(ctx, instance=instance).get_item(fullname=fullname, depth=1)
        # Type guard to ensure we have a job type with lastBuild
        if (
            isinstance(item, (Job, FreeStyleProject, MultiBranchProject))
            and item.lastBuild is not None
        ):
            number = item.lastBuild.number
        else:
            msg = f"No builds found for job '{fullname}'"
            raise ValueError(msg)

    return (
        jenkins(ctx, instance=instance)
        .get_build(fullname=fullname, number=number)
        .model_dump(exclude_none=True)
    )


@mcp.tool(tags={"read"})
async def get_build_scripts(
    ctx: Context, fullname: str, number: int | None = None, instance: str | None = None
) -> list[str]:
    """Get the scripts used in a specific build in Jenkins

    Args:
        fullname: The fullname of the job
        number: The number of the build, if None, get the last build
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        A list of scripts used in the build
    """
    if number is None:
        item = jenkins(ctx, instance=instance).get_item(fullname=fullname, depth=1)
        # Type guard to ensure we have a job type with lastBuild
        if (
            isinstance(item, (Job, FreeStyleProject, MultiBranchProject))
            and item.lastBuild is not None
        ):
            number = item.lastBuild.number
        else:
            msg = f"No builds found for job '{fullname}'"
            raise ValueError(msg)

    return (
        jenkins(ctx, instance=instance)
        .get_build_replay(fullname=fullname, number=number)
        .scripts
    )


@mcp.tool(tags={"read"})
async def get_build_console_output(
    ctx: Context,
    fullname: str,
    number: int | None = None,
    pattern: str | None = None,
    offset: int = 0,
    limit: int | None = None,
    instance: str | None = None,
) -> str:
    """Get the console output of a specific build in Jenkins

    Args:
        fullname: The fullname of the job
        number: The number of the build, if None, get the last build
        pattern: Optional regex pattern to filter lines (only matching lines are returned)
        offset: Number of lines to skip from the beginning after filtering, default 0
        limit: Maximum number of lines to return after filtering and offset
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        The console output of the build
    """
    if number is None:
        item = jenkins(ctx, instance=instance).get_item(fullname=fullname, depth=1)
        # Type guard to ensure we have a job type with lastBuild
        if (
            isinstance(item, (Job, FreeStyleProject, MultiBranchProject))
            and item.lastBuild is not None
            and item.lastBuild.number is not None
        ):
            number = item.lastBuild.number
        else:
            msg = f"No build found for job: {fullname}"
            raise ValueError(msg)

    return jenkins(ctx, instance=instance).get_build_console_output(
        fullname=fullname, number=number, pattern=pattern, offset=offset, limit=limit
    )


@mcp.tool(tags={"read"})
async def get_build_test_report(
    ctx: Context, fullname: str, number: int | None = None, instance: str | None = None
) -> dict[str, Any]:
    """Get the test report of a specific build in Jenkins

    Args:
        fullname: The fullname of the job
        number: The number of the build, if None, get the last build
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        The test report of the build
    """
    if number is None:
        item = jenkins(ctx, instance=instance).get_item(fullname=fullname, depth=1)
        # Type guard to ensure we have a job type with lastBuild
        if (
            isinstance(item, (Job, FreeStyleProject, MultiBranchProject))
            and item.lastBuild is not None
        ):
            number = item.lastBuild.number
        else:
            msg = f"No builds found for job '{fullname}'"
            raise ValueError(msg)

    return jenkins(ctx, instance=instance).get_build_test_report(
        fullname=fullname, number=number
    )


@mcp.tool(tags={"read"})
async def get_build_parameters(
    ctx: Context, fullname: str, number: int | None = None, instance: str | None = None
) -> dict[str, Any]:
    """Get the parameters of a specific build in Jenkins

    Args:
        fullname: The fullname of the job
        number: The number of the build, if None, get the last build
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        A dictionary of build parameter names and their values
    """
    if number is None:
        item = jenkins(ctx, instance=instance).get_item(fullname=fullname, depth=1)
        # Type guard to ensure we have a job type with lastBuild
        if (
            isinstance(item, (Job, FreeStyleProject, MultiBranchProject))
            and item.lastBuild is not None
        ):
            number = item.lastBuild.number
        else:
            msg = f"No builds found for job '{fullname}'"
            raise ValueError(msg)

    return jenkins(ctx, instance=instance).get_build_parameters(
        fullname=fullname, number=number
    )


@mcp.tool(tags={"write"})
async def stop_build(
    ctx: Context, fullname: str, number: int, instance: str | None = None
) -> None:
    """Stop a specific build in Jenkins

    Args:
        fullname: The fullname of the job
        number: The number of the build to stop
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.
    """
    return jenkins(ctx, instance=instance).stop_build(fullname=fullname, number=number)


@mcp.tool(tags={"read"})
async def get_all_build_artifacts(
    ctx: Context, fullname: str, number: int | None = None, instance: str | None = None
) -> list[dict[str, Any]]:
    """List the artifacts of a specific build in Jenkins

    Args:
        fullname: The fullname of the job
        number: The number of the build, if None, get the last build
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        A list of artifact metadata dicts with fileName, relativePath, and displayPath
    """
    if number is None:
        item = jenkins(ctx, instance=instance).get_item(fullname=fullname, depth=1)
        # Type guard to ensure we have a job type with lastBuild
        if (
            isinstance(item, (Job, FreeStyleProject, MultiBranchProject))
            and item.lastBuild is not None
        ):
            number = item.lastBuild.number
        else:
            msg = f"No builds found for job '{fullname}'"
            raise ValueError(msg)

    return [
        artifact.model_dump(exclude_none=True)
        for artifact in jenkins(ctx, instance=instance).get_build_artifacts(
            fullname=fullname, number=number
        )
    ]


@mcp.tool(tags={"read"})
async def get_build_artifact(
    ctx: Context,
    fullname: str,
    relative_path: str,
    number: int | None = None,
    instance: str | None = None,
) -> dict[str, str]:
    """Download an artifact from a specific build in Jenkins

    Binary files are returned as base64-encoded content; text files are returned as plain text.

    Args:
        fullname: The fullname of the job
        relative_path: The relative path of the artifact (e.g. playwright-report/index.html)
        number: The number of the build, if None, get the last build
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        A dict with 'content' (str) and 'encoding' ('utf-8' or 'base64')
    """
    if number is None:
        item = jenkins(ctx, instance=instance).get_item(fullname=fullname, depth=1)
        # Type guard to ensure we have a job type with lastBuild
        if (
            isinstance(item, (Job, FreeStyleProject, MultiBranchProject))
            and item.lastBuild is not None
        ):
            number = item.lastBuild.number
        else:
            msg = f"No builds found for job '{fullname}'"
            raise ValueError(msg)

    content = jenkins(ctx, instance=instance).get_build_artifact(
        fullname=fullname, number=number, relative_path=relative_path
    )

    try:
        return {"content": content.decode("utf-8"), "encoding": "utf-8"}
    except UnicodeDecodeError:
        return {
            "content": base64.b64encode(content).decode("ascii"),
            "encoding": "base64",
        }


@mcp.tool(tags={"read"})
async def get_build_artifact_url(
    ctx: Context,
    fullname: str,
    relative_path: str,
    number: int | None = None,
    instance: str | None = None,
) -> str:
    """Get the direct URL of an artifact from a specific build in Jenkins

    Args:
        fullname: The fullname of the job
        relative_path: The relative path of the artifact (e.g. playwright-report/index.html)
        number: The number of the build, if None, get the last build
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        The direct Jenkins URL of the artifact
    """
    if number is None:
        item = jenkins(ctx, instance=instance).get_item(fullname=fullname, depth=1)
        # Type guard to ensure we have a job type with lastBuild
        if (
            isinstance(item, (Job, FreeStyleProject, MultiBranchProject))
            and item.lastBuild is not None
        ):
            number = item.lastBuild.number
        else:
            msg = f"No builds found for job '{fullname}'"
            raise ValueError(msg)

    return jenkins(ctx, instance=instance).get_build_artifact_url(
        fullname=fullname, number=number, relative_path=relative_path
    )
