/** Round-trip fixtures and reject everything outside the contract. */

import { assertEquals, assertThrows } from "@std/assert";
import { parseEvent, parseRequest, ProtocolError } from "./parse.ts";

const ROOT = new URL("../../tests/fixtures/protocol/", import.meta.url);

async function roundTrip(
  dir: string,
  parse: (line: string) => unknown,
): Promise<void> {
  for await (const entry of Deno.readDir(new URL(dir, ROOT))) {
    if (!entry.isFile || !entry.name.endsWith(".json")) continue;
    const text = await Deno.readTextFile(new URL(`${dir}/${entry.name}`, ROOT));
    const original = JSON.parse(text);
    const parsed = parse(text);
    const reparsed = JSON.parse(JSON.stringify(parsed));
    assertEquals(reparsed, original);
  }
}

Deno.test("request fixtures round-trip", async () => {
  await roundTrip("requests", parseRequest);
});

Deno.test("event fixtures round-trip", async () => {
  await roundTrip("events/stream", parseEvent);
  await roundTrip("events/terminal", parseEvent);
});

/**
 * Regression: `in` and bare property access both consult `Object.prototype`,
 * so the previous allowlist accepted these as protocol types. Rust and Python
 * reject all of them, so the TUI must too.
 */
const PROTOTYPE_KEYS = [
  "constructor",
  "toString",
  "__proto__",
  "valueOf",
  "hasOwnProperty",
];

for (const key of PROTOTYPE_KEYS) {
  Deno.test(`request rejects prototype key "${key}"`, () => {
    assertThrows(
      () => parseRequest(JSON.stringify({ type: key })),
      ProtocolError,
      "unknown request type",
    );
  });

  Deno.test(`event rejects prototype key "${key}"`, () => {
    assertThrows(
      () => parseEvent(JSON.stringify({ type: key })),
      ProtocolError,
      "unknown event type",
    );
  });
}

Deno.test("request rejects a missing field", () => {
  assertThrows(
    () => parseRequest(JSON.stringify({ type: "Chat" })),
    ProtocolError,
    "message must be string",
  );
});

Deno.test("request rejects a field of the wrong type", () => {
  assertThrows(
    () => parseRequest(JSON.stringify({ type: "Chat", message: 123 })),
    ProtocolError,
    "message must be string",
  );
});

Deno.test("event rejects an incomplete nested usage", () => {
  assertThrows(
    () => parseEvent(JSON.stringify({ type: "Done", usage: {} })),
    ProtocolError,
    "usage.prompt_tokens must be number",
  );
});

Deno.test("event accepts a complete nested usage", () => {
  const line = JSON.stringify({
    type: "Done",
    usage: { prompt_tokens: 3, completion_tokens: 5 },
  });
  assertEquals(parseEvent(line).type, "Done");
});

Deno.test("tool call args accept any JSON value", () => {
  const line = JSON.stringify({
    type: "ToolCall",
    name: "read",
    args: "path",
  });
  assertEquals(parseEvent(line).type, "ToolCall");
});

Deno.test("unknown extra fields are ignored, matching Python and Rust", () => {
  const line = JSON.stringify({ type: "Chat", message: "hi", extra: 1 });
  assertEquals(parseRequest(line).type, "Chat");
});

Deno.test("malformed JSON reports a protocol error", () => {
  assertThrows(
    () => parseRequest("{not json"),
    ProtocolError,
    "invalid JSON",
  );
});

Deno.test("a JSON array is not a request", () => {
  assertThrows(
    () => parseRequest("[]"),
    ProtocolError,
    "must be a JSON object",
  );
});
