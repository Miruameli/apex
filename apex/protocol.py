"""JSONL stdio protocol mirroring tests/fixtures/protocol/."""

from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, TypeAdapter


class Chat(BaseModel):
    type: Literal["Chat"] = "Chat"
    message: str


class Fix(BaseModel):
    type: Literal["Fix"] = "Fix"
    target: str


class Review(BaseModel):
    type: Literal["Review"] = "Review"
    path: str


class Context(BaseModel):
    type: Literal["Context"] = "Context"
    root: str


AgentRequest = Annotated[Chat | Fix | Review | Context, Field(discriminator="type")]


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int


class Thinking(BaseModel):
    type: Literal["Thinking"] = "Thinking"
    content: str


class ToolCall(BaseModel):
    type: Literal["ToolCall"] = "ToolCall"
    name: str
    args: Any


class Diff(BaseModel):
    type: Literal["Diff"] = "Diff"
    path: str
    old: str
    new: str


class Message(BaseModel):
    type: Literal["Message"] = "Message"
    role: str
    content: str


class Done(BaseModel):
    type: Literal["Done"] = "Done"
    usage: Usage


class ErrorEvent(BaseModel):
    type: Literal["Error"] = "Error"
    message: str


AgentEvent = Annotated[
    Thinking | ToolCall | Diff | Message | Done | ErrorEvent,
    Field(discriminator="type"),
]

request_adapter: TypeAdapter[AgentRequest] = TypeAdapter(AgentRequest)
event_adapter: TypeAdapter[AgentEvent] = TypeAdapter(AgentEvent)
