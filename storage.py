from datetime import datetime
from app.models import get_db




def insert_message(msg):
conn = get_db()
cur = conn.cursor()
try:
cur.execute(
"""
INSERT INTO messages (message_id, from_msisdn, to_msisdn, ts, text, created_at)
VALUES (?, ?, ?, ?, ?, ?)
""",
(
msg["message_id"],
msg["from"],
msg["to"],
msg["ts"],
msg.get("text"),
datetime.utcnow().isoformat() + "Z",
),
)
conn.commit()
return True
except Exception:
return False
finally:
conn.close()