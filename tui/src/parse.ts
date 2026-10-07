/**
 * Runtime validation for the JSONL stdio protocol.
 *
 * The agent is the only producer of these lines, but it is still a separate
 * process: its output is untrusted input to the TUI. Every parse therefore
 * checks the `type` tag against an allowlist and checks that each declared
 * field is present with the right JSON type, matching what the Rust core and
 * the Python agent accept. See ADR-0007.
 */

import type { AgentEvent, AgentRequest } from "./protocol.ts";

/** A required field and the JSON type its value must carry. */
interface Field {
  readonly name: string;
  readonly kind: "string" | "number" | "object" | "any";
  /** Required sub-fields, when this field carries a nested object. */
  readonly nested?: readonly Field[];
}

/** Raised when a line is not valid protocol. Callers catch only this type. */
export class ProtocolError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ProtocolError";
  }
}

const USAGE_FIELDS: readonly Field[] = [
  { name: "prompt_tokens", kind: "number" },
  { name: "completion_tokens", kind: "number" },
];

/**
 * Contract tables keyed by `type` tag.
 *
 * Lookups go through `Object.hasOwn`, never `in` or bare property access. Both
 * of those walk `Object.prototype`, so a plain table would accept
 * `constructor`, `toString`, and `__proto__` as protocol types. Own-key checks
 * reject them.
 */
const REQUEST_FIELDS: Record<string, readonly Field[]> = {
  Chat: [{ name: "message", kind: "string" }],
  Fix: [{ name: "target", kind: "string" }],
  Review: [{ name: "path", kind: "string" }],
  Context: [{ name: "root", kind: "string" }],
};

const EVENT_FIELDS: Record<string, readonly Field[]> = {
  Thinking: [{ name: "content", kind: "string" }],
  ToolCall: [
    { name: "name", kind: "string" },
    { name: "args", kind: "any" },
  ],
  Diff: [
    { name: "path", kind: "string" },
    { name: "old", kind: "string" },
    { name: "new", kind: "string" },
  ],
  Message: [
    { name: "role", kind: "string" },
    { name: "content", kind: "string" },
  ],
  Done: [{ name: "usage", kind: "object", nested: USAGE_FIELDS }],
  Error: [{ name: "message", kind: "string" }],
};

/** Own-key lookup, so prototype members are not mistaken for protocol types. */
function lookupFields(
  table: Record<string, readonly Field[]>,
  tag: unknown,
): readonly Field[] | undefined {
  if (typeof tag !== "string") return undefined;
  return Object.hasOwn(table, tag) ? table[tag] : undefined;
}

function hasKind(kind: Field["kind"], value: unknown): boolean {
  switch (kind) {
    case "string":
      return typeof value === "string";
    case "number":
      return typeof value === "number";
    case "object":
      return typeof value === "object" && value !== null &&
        !Array.isArray(value);
    case "any":
      return true;
  }
}

/** Report the first field that does not satisfy the contract, else null. */
function firstViolation(
  fields: readonly Field[],
  value: Record<string, unknown>,
  prefix = "",
): string | null {
  for (const field of fields) {
    const path = `${prefix}${field.name}`;
    const actual = value[field.name];
    if (!hasKind(field.kind, actual)) {
      return `${path} must be ${field.kind}`;
    }
    if (field.nested !== undefined) {
      const nested = firstViolation(
        field.nested,
        actual as Record<string, unknown>,
        `${path}.`,
      );
      if (nested !== null) return nested;
    }
  }
  return null;
}

/** Parse `line` as JSON and validate it against one contract table. */
function parseLine<T>(
  line: string,
  label: string,
  table: Record<string, readonly Field[]>,
): T {
  let value: unknown;
  try {
    value = JSON.parse(line);
  } catch (error) {
    throw new ProtocolError(
      `invalid JSON in ${label}: ${(error as Error).message}`,
    );
  }

  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new ProtocolError(`${label} must be a JSON object`);
  }

  const record = value as Record<string, unknown>;
  const tag = record.type;
  const fields = lookupFields(table, tag);
  if (fields === undefined) {
    throw new ProtocolError(`unknown ${label} type: ${String(tag)}`);
  }

  const violation = firstViolation(fields, record);
  if (violation !== null) {
    throw new ProtocolError(`invalid ${tag} ${label}: ${violation}`);
  }

  return record as T;
}

/** Parse one JSONL line into an agent request. */
export function parseRequest(line: string): AgentRequest {
  return parseLine<AgentRequest>(line, "request", REQUEST_FIELDS);
}

/** Parse one JSONL line into an agent event. */
export function parseEvent(line: string): AgentEvent {
  return parseLine<AgentEvent>(line, "event", EVENT_FIELDS);
}
