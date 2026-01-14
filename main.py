import hmac
import hashlib
import time
from fastapi import FastAPI, Request, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import re


from app.config import WEBHOOK_SECRET
from app.models import init_db, get_db
from app.storage import insert_message
from app.logging_utils import log_event, generate_request_id


app = FastAPI()


class WebhookMessage(BaseModel):
message_id: str
from_: str = Field(alias="from")
to: str
ts: str
text: Optional[str] = None


@app.on_event("startup")
def startup():
if not WEBHOOK_SECRET:
raise RuntimeError("WEBHOOK_SECRET not set")
init_db()


@app.get("/health/live")
def live():
return {"status": "alive"}


@app.get("/health/ready")
def ready():
try:
conn = get_db()
conn.execute("SELECT 1")
conn.close()
if not WEBHOOK_SECRET:
raise Exception()
return {"status": "ready"}
except:
raise HTTPException(status_code=503)


@app.post("/webhook")
async def webhook(req: Request):
start = time.time()
request_id = generate_request_id()
raw = await req.body()
sig = req.headers.get("X-Signature")


expected = hmac.new(WEBHOOK_SECRET.encode(), raw, hashlib.sha256).hexdigest()


if not sig or not hmac.compare_digest(sig, expected):
log_event(level="error", request_id=request_id, path="/webhook", result="invalid_signature")
raise HTTPException(status_code=401, detail="invalid signature")


body = await req.json()


ok = insert_message(body)
result = "created" if ok else "duplicate"


latency = int((time.time() - start) * 1000)


log_event(
level="info",
request_id=request_id,
method="POST",
path="/webhook",
status=200,
latency_ms=latency,
message_id=body.get("message_id"),
dup=not ok,
result=result,
)


return {"status": "ok"}


@app.get("/messages")
def list_messages(
limit: int = Query(50, ge=1, le=100),
offset: int = Query(0, ge=0),
from_: Optional[str] = Query(None, alias="from"),
):
}