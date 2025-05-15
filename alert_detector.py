import time
from collections import defaultdict, deque
from config import FAILED_LOGIN_THRESHOLD, FAILED_LOGIN_TIME_WINDOW


class AlertDetector:
    def __init__(self):
        self.failed_logins = defaultdict(deque)

    def process_event(self, event):
        alerts = []
        if event.get("event") == "failed_login":
            # Logic for detecting suspicious ips with failed logins
            ip = event.get("ip_address")
            timestamp = time.time()
            dq = self.failed_logins[ip]
            dq.append(timestamp)
            
            # Remove old attempts outside the time window
            while dq and timestamp - dq[0] > FAILED_LOGIN_TIME_WINDOW:
                dq.popleft()

            # Too many attempts from one ip
            if len(dq) >= FAILED_LOGIN_THRESHOLD:
                alert = {
                    "type": "too_many_attempts_from_ip",
                    "ip_address": ip,
                    "timestamp": timestamp,
                    "attempts": len(dq)
                }
                alerts.append(alert)
        return alerts