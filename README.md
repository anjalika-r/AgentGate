# AgentGate

**A policy-enforcement gateway for tool-using AI agents.**

AgentGate evaluates a proposed action before an AI agent reaches a tool. It returns an explicit, auditable `allow`, `require_approval`, or `block` decision.

## Why it exists

Giving an LLM access to tools changes a bad output into a potentially harmful action. AgentGate provides an explainable policy layer for prompt injection, credential-like secrets, unauthorised tools, external communications, and sensitive data.

```text
Agent proposes tool action → AgentGate policy engine → allow / approval / block
                                        ↓
                                  SQLite audit log
```

## Quick start

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn agentgate.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation. Run `python demo.py` for three sample decisions and `pytest -q` for the automated test suite.

## Example

```json
{
  "agent_id": "support-agent",
  "tool": "email",
  "action": "send_email",
  "destination": "client@outside.com",
  "payload": "Status update"
}
```

This is returned as `require_approval`: external email and sending messages are deliberately treated as higher-risk actions.

## Scope

This is a compact reference implementation. Its rules are deterministic and transparent; production extensions would add identity-aware authorisation, signed policy bundles, immutable logging, model-assisted classifiers, and adversarial evaluation datasets.
