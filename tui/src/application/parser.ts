/**
 * Public API for parsing JSONL protocol lines into typed agent messages.
 *
 * The agent process is the sole producer of these lines, but it is still a
 * separate process: its output is untrusted input to the TUI. Every parse
 * checks the `type` tag against an allowlist and verifies field types,
 * matching what the Rust core and Python agent accept.
 *
 * Re-exports ProtocolError so callers catch a single error type.
 *
 * Layer: Application (use-case orchestration)
 */

import type { AgentEvent, AgentRequest } from "../domain/protocol.ts";
import { parseLine } from "../infrastructure/validation/rules.ts";
import {
  EVENT_FIELDS,
  REQUEST_FIELDS,
} from "../infrastructure/validation/contract.ts";
import { ProtocolError } from "../shared/error.ts";

export { ProtocolError };

/** Parse one JSONL line into an agent request. */
export function parseRequest(line: string): AgentRequest {
  return parseLine<AgentRequest>(line, "request", REQUEST_FIELDS);
}

/** Parse one JSONL line into an agent event. */
export function parseEvent(line: string): AgentEvent {
  return parseLine<AgentEvent>(line, "event", EVENT_FIELDS);
}
