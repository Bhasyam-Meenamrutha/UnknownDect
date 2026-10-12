"""
Send ONE sample "unknown person" alert email to check that the
email settings in .env work.

    python test_unknown_alert.py
"""

import cv2
import numpy as np

from datetime import datetime

import email_service


# A plain test picture with a red box, so the attachment can be checked.
frame = np.full((480, 640, 3), 40, dtype=np.uint8)

cv2.rectangle(frame, (220, 100), (420, 340), (0, 0, 255), 3)

cv2.putText(
    frame,
    "TEST - UNKNOWN PERSON",
    (150, 60),
    cv2.FONT_HERSHEY_SIMPLEX,
    1,
    (255, 255, 255),
    2
)

ok, encoded = cv2.imencode(".jpg", frame)

print(f"Sending test alert to: {email_service.ALERT_RECIPIENT}")

sent = email_service.send_unknown_person_email(
    detected_at=datetime.now().strftime("%d-%b-%Y %I:%M:%S %p"),
    camera_name="ENTRY (test)",
    match_score=0.21,
    snapshot_jpeg=encoded.tobytes() if ok else None
)

print("SENT" if sent else "FAILED - check EMAIL_SENDER / EMAIL_PASSWORD in .env")