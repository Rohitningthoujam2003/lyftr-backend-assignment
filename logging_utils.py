import json
import logging
from datetime import datetime
import uuid


logger = logging.getLogger("app")
logging.basicConfig(level=logging.INFO)




def log_event(**kwargs):
base = {
"ts": datetime.utcnow().isoformat() + "Z",
}
base.update(kwargs)
logger.info(json.dumps(base))




def generate_request_id():
return str(uuid.uuid4())