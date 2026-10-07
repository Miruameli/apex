/**
 * Contract definitions for protocol validation.
 *
 * Each entry declares a required field, its expected JSON type, and
 * optionally nested sub-field contracts for object-typed fields.
 *
 * Layer: Infrastructure / Validation (static contract data)
 */

/** A required field and the JSON type its value must carry. */
export interface Field {
  readonly name: string;
  readonly kind: "string" | "number" | "object" | "any";
  /** Required sub-fields, when this field carries a nested object. */
  readonly nested?: readonly Field[];
}

/** Token counters nested inside the Done event. */
export const USAGE_FIELDS: readonly Field[] = [
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
export const REQUEST_FIELDS: Record<string, readonly Field[]> = {
  Chat: [{ name: "message", kind: "string" }],
  Fix: [{ name: "target", kind: "string" }],
  Review: [{ name: "path", kind: "string" }],
  Context: [{ name: "root", kind: "string" }],
};

export const EVENT_FIELDS: Record<string, readonly Field[]> = {
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
