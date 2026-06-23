# Hermes Provider Data Handling

Date: 2026-06-23
Owner: Platform Operations

## Default

Hermes should use local oMLX for private and ordinary work. No new cloud provider was added in this pass.

## Provider Classes

| Provider class | Data handling |
|---|---|
| Local oMLX | Stays on this Mac at `127.0.0.1:18080`. Preferred for private work. |
| Local llama.cpp | Stays on this Mac at `127.0.0.1:8002`; manual lane. |
| Local Rapid-MLX | Stays on this Mac at `127.0.0.1:8010`; manual lab lane. |
| Direct cloud API | Sends prompts and tool context to provider; requires approval and budget control. |
| Aggregator/router | Sends data to aggregator and downstream model provider; avoid unless multi-provider routing is explicitly needed. |

## Approval Gate

Before cloud escalation, record:

- provider and model;
- data classification;
- reason local models are insufficient;
- expected cost;
- credential item in `Boneman`;
- fallback and retry limits.

Never commit provider keys, token prefixes, cookies, private keys, or raw credential files.
