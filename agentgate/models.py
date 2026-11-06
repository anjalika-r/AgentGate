from enum import Enum
from pydantic import BaseModel, Field

class Decision(str, Enum):
    ALLOW = "allow"
    REQUIRE_APPROVAL = "require_approval"
    BLOCK = "block"

class ActionRequest(BaseModel):
    agent_id: str = Field(min_length=1, max_length=100)
    tool: str = Field(min_length=1, max_length=100)
    action: str = Field(min_length=1, max_length=100)
    destination: str | None = Field(default=None, max_length=300)
    payload: str = Field(default="", max_length=20_000)
    data_classification: str = Field(default="internal")

class EvaluationResponse(BaseModel):
    decision: Decision
    risk_score: int
    reasons: list[str]
    audit_id: int

class AuditRecord(BaseModel):
    id: int
    timestamp: str
    agent_id: str
    tool: str
    action: str
    destination: str | None
    decision: Decision
    risk_score: int
    reasons: list[str]
