import re
from .models import ActionRequest, Decision

SUSPICIOUS_PATTERNS = [r"ignore (all |any |previous )?(instructions|rules|policy)", r"reveal (the )?(system prompt|secret|api key|password)", r"exfiltrat(e|ion)", r"bypass (security|guardrails|approval)"]
SECRET_PATTERNS = [r"\b(?:sk|api)[-_][A-Za-z0-9_-]{12,}\b", r"\bAKIA[0-9A-Z]{16}\b"]
HIGH_IMPACT_ACTIONS = {"send_email", "delete", "transfer_money", "publish", "execute"}
SENSITIVE_CLASSIFICATIONS = {"confidential", "restricted", "secret"}
ALLOWED_TOOLS = {"knowledge_search", "ticket_draft", "email", "file_reader", "database_query"}

def evaluate(request: ActionRequest) -> tuple[Decision, int, list[str]]:
    """Apply deterministic, explainable guardrails to a proposed agent action."""
    text = " ".join(filter(None, [request.payload, request.destination])).lower()
    reasons: list[str] = []
    score = 0
    if request.tool not in ALLOWED_TOOLS:
        reasons.append(f"Tool '{request.tool}' is not on the approved tool allowlist.")
        score += 80
    if any(re.search(pattern, text, re.IGNORECASE) for pattern in SUSPICIOUS_PATTERNS):
        reasons.append("Potential prompt-injection or policy-bypass instruction detected.")
        score += 80
    if any(re.search(pattern, request.payload) for pattern in SECRET_PATTERNS):
        reasons.append("Payload appears to contain a credential or secret.")
        score += 80
    if score >= 80:
        return Decision.BLOCK, min(score, 100), reasons
    if request.action in HIGH_IMPACT_ACTIONS:
        reasons.append(f"'{request.action}' is a high-impact action and needs human approval.")
        score += 45
    if request.data_classification.lower() in SENSITIVE_CLASSIFICATIONS:
        reasons.append("Sensitive data classification requires human approval.")
        score += 35
    if request.destination and request.tool == "email" and not request.destination.endswith("@example.com"):
        reasons.append("External email destination requires human approval.")
        score += 25
    if score:
        return Decision.REQUIRE_APPROVAL, min(score, 100), reasons
    return Decision.ALLOW, 0, ["Action complies with configured policy checks."]
