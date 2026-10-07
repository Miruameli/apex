/**
 * Protocol-level error raised when a JSONL line does not satisfy the contract.
 *
 * Callers catch only this type; never a raw JSON.parse or type-coercion error.
 *
 * Layer: Shared (cross-cutting concern)
 */

export class ProtocolError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ProtocolError";
  }
}
