import json
import sqlite3
from pathlib import Path
from .models import ActionRequest, AuditRecord, Decision

class AuditStore:
    def __init__(self, database_path: str = "agentgate.db"):
        self.database_path = Path(database_path)
        self._initialise()
    def _connect(self): return sqlite3.connect(self.database_path)
    def _initialise(self):
        with self._connect() as c:
            c.execute("CREATE TABLE IF NOT EXISTS audit_log (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, agent_id TEXT NOT NULL, tool TEXT NOT NULL, action TEXT NOT NULL, destination TEXT, decision TEXT NOT NULL, risk_score INTEGER NOT NULL, reasons TEXT NOT NULL)")
    def record(self, request: ActionRequest, decision: Decision, score: int, reasons: list[str]) -> int:
        with self._connect() as c:
            cur = c.execute("INSERT INTO audit_log (agent_id, tool, action, destination, decision, risk_score, reasons) VALUES (?, ?, ?, ?, ?, ?, ?)", (request.agent_id, request.tool, request.action, request.destination, decision.value, score, json.dumps(reasons)))
            return int(cur.lastrowid)
    def recent(self, limit: int = 20) -> list[AuditRecord]:
        with self._connect() as c:
            rows = c.execute("SELECT id, timestamp, agent_id, tool, action, destination, decision, risk_score, reasons FROM audit_log ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [AuditRecord(id=r[0], timestamp=r[1], agent_id=r[2], tool=r[3], action=r[4], destination=r[5], decision=Decision(r[6]), risk_score=r[7], reasons=json.loads(r[8])) for r in rows]
