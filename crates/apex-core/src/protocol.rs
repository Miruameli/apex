//! JSONL stdio protocol types shared by Rust, Python, and TS.
//!
//! Round-trip contract: parse fixture -> serialize -> parse -> deep-equal.

use serde::{Deserialize, Serialize};
use serde_json::Value;

/// Request sent from the interface layer to the agent.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "type")]
pub enum AgentRequest {
    Chat { message: String },
    Fix { target: String },
    Review { path: String },
    Context { root: String },
}

/// Token usage reported in the terminal `Done` event.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Usage {
    pub prompt_tokens: u64,
    pub completion_tokens: u64,
}

/// Event streamed from the agent to the interface layer.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "type")]
pub enum AgentEvent {
    Thinking {
        content: String,
    },
    ToolCall {
        name: String,
        args: Value,
    },
    Diff {
        path: String,
        old: String,
        new: String,
    },
    Message {
        role: String,
        content: String,
    },
    Done {
        usage: Usage,
    },
    Error {
        message: String,
    },
}

/// Parse a JSON line into an agent request.
pub fn parse_request(line: &str) -> Result<AgentRequest, serde_json::Error> {
    serde_json::from_str(line)
}

/// Parse a JSON line into an agent event.
pub fn parse_event(line: &str) -> Result<AgentEvent, serde_json::Error> {
    serde_json::from_str(line)
}
