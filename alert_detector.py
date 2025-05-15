import time
from collections import defaultdict, deque
from config import FAILED_LOGIN_THRESHOLD, FAILED_LOGIN_TIME_WINDOW


class AlertDetector:
    def __init__(self):
        self.failed_logins = defaultdict(deque)
        self.last_location = {}
        self.used_device = defaultdict(lambda: deque(maxlen=50))

    def process_event(self, event):
        alerts = []
        
        ip = event.get("ip_address")
        timestamp = time.time()


        # Logic for detecting suspicious ips with failed logins
        if event.get("event") == "failed_login":
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
        

        # Logic for detecting different locations after successful login
        if event.get("event") == "login":
            previous_location = self.last_location.get(ip)
            current_location = event.get("location")

            if previous_location and current_location != previous_location:
                alert = {
                    "type": "different_location",
                    "ip_address": ip,
                    "timestamp": timestamp,
                    "from": previous_location,
                    "to": current_location
                }
                alerts.append(alert)

            # Update location (even if alert was not triggered)
            if current_location:
                self.last_location[ip] = current_location
        
        
        # Logic for detecting suspicious device switch    
        if event.get("event") == "login":
            device = event.get("device")
            dq = self.used_device[ip]
            dq.append(device)

            if len(dq) > 20:
                # Count how many times certain device was used
                device_counts = defaultdict(int)
                for d in dq:
                    device_counts[d] += 1

                # Calculate dominance ratio
                total = len(dq)
                most_common_device = max(device_counts, key=device_counts.get)
                dominance_ratio = device_counts[most_common_device] / total

                # Check if dominance ratio is over x% and if the used device is the one that dominates
                if dominance_ratio > 0.95 and most_common_device != device:
                    alert = {
                        "type": "suspicious_device_change",
                        "ip_address": ip,
                        "timestamp": timestamp,
                        "dominant_device": most_common_device,
                        "used_device": device,
                        "dominance_ratio": round(dominance_ratio, 2)
                    }
                    alerts.append(alert)


        return alerts