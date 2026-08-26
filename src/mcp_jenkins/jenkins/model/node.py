from typing import Optional

from pydantic import BaseModel


class Node(BaseModel):
    displayName: str
    offline: bool

    executors: list["NodeExecutor"]


class NodeExecutor(BaseModel):
    currentExecutable: Optional["NodeExecutorCurrentExecutable"] = None


class NodeExecutorCurrentExecutable(BaseModel):
    url: str = ""
    timestamp: int | None = None
    number: int | None = None
    fullDisplayName: str = ""
