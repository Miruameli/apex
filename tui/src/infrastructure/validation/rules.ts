/**
 * Validation primitives for protocol field checking.
 *
 * These functions implement the reusable logic that walks a parsed JSON
 * value against a contract table, reporting the first violation.
 *
 * Layer: Infrastructure / Validation (runtime validation logic)
 */

import { ProtocolError } from "../../shared/error.ts";
import type { Field } from "./contract.ts";

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

/**
 * Parse `line` as JSON and validate it against one contract table.
 *
 * Throws ProtocolError for invalid JSON or contract violations.
 */
export function parseLine<T>(
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
