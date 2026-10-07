/**
 * Wire types for the JSONL stdio protocol.
 *
 * These declarations describe the shapes named in `tests/fixtures/protocol/`.
 * Runtime validation of untrusted input lives in `parse.ts`; nothing here
 * executes, so importing this module costs no work.
 */

export interface Usage {
  prompt_tokens: number;
  completion_tokens: number;
}

export interface ChatRequest {
  type: "Chat";
  message: string;
}
export interface FixRequest {
  type: "Fix";
  target: string;
}
export interface ReviewRequest {
  type: "Review";
  path: string;
}
export interface ContextRequest {
  type: "Context";
  root: string;
}
export type AgentRequest =
  | ChatRequest
  | FixRequest
  | ReviewRequest
  | ContextRequest;

export interface ThinkingEvent {
  type: "Thinking";
  content: string;
}
export interface ToolCallEvent {
  type: "ToolCall";
  name: string;
  args: unknown;
}
export interface DiffEvent {
  type: "Diff";
  path: string;
  old: string;
  new: string;
}
export interface MessageEvent {
  type: "Message";
  role: string;
  content: string;
}
export interface DoneEvent {
  type: "Done";
  usage: Usage;
}
export interface ErrorEvent {
  type: "Error";
  message: string;
}
export type AgentEvent =
  | ThinkingEvent
  | ToolCallEvent
  | DiffEvent
  | MessageEvent
  | DoneEvent
  | ErrorEvent;
