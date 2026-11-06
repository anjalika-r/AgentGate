import os
from fastapi import FastAPI, Query
from .models import ActionRequest, AuditRecord, EvaluationResponse
from .policy import evaluate
from .store import AuditStore

app = FastAPI(title="AgentGate", version="0.1.0", description="Policy enforcement for tool-using AI agents.")
store = AuditStore(os.getenv("AGENTGATE_DB", "agentgate.db"))
@app.get("/health")
def health(): return {"status": "ok"}
@app.post("/v1/evaluate", response_model=EvaluationResponse)
def evaluate_action(request: ActionRequest):
    decision, risk_score, reasons = evaluate(request)
    return EvaluationResponse(decision=decision, risk_score=risk_score, reasons=reasons, audit_id=store.record(request, decision, risk_score, reasons))
@app.get("/v1/audit", response_model=list[AuditRecord])
def get_audit(limit: int = Query(default=20, ge=1, le=100)): return store.recent(limit)
