import os
import smtplib

from email.message import EmailMessage

from dotenv import load_dotenv


load_dotenv()


EMAIL_SENDER = os.getenv(
    "EMAIL_SENDER"
)

EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD"
)


def send_arrival_email(
    employee_name,
    employee_email,
    shift_start,
    first_in,
    status,
    minutes
):
    """
    Send an early or late arrival notification.
    """

    if not EMAIL_SENDER or not EMAIL_PASSWORD:

        print(
            "Email configuration is missing."
        )

        return False

    message = EmailMessage()

    message["From"] = EMAIL_SENDER

    message["To"] = employee_email

    if status == "EARLY":

        message["Subject"] = (
            "Early Arrival Notification"
        )

        message.set_content(
            f"""
Hello {employee_name},

This is an automated attendance notification.

Your first arrival today was recorded earlier
than your scheduled shift.

Employee       : {employee_name}
Shift Start    : {shift_start}
First IN       : {first_in}
Arrival Status : EARLY
Early By       : {minutes} minutes

Please note that early arrival has been recorded
by the Employee Attendance System.

This is an automatically generated email.
Please do not reply to this email.

Regards,
Employee Attendance System
"""
        )

    elif status == "LATE":

        message["Subject"] = (
            "Late Arrival Notification"
        )

        message.set_content(
            f"""
Hello {employee_name},

This is an automated attendance notification.

Your first arrival today was recorded later
than your scheduled shift.

Employee       : {employee_name}
Shift Start    : {shift_start}
First IN       : {first_in}
Arrival Status : LATE
Late By        : {minutes} minutes

Please ensure that you follow your assigned
shift timings.

This is an automatically generated email.
Please do not reply to this email.

Regards,
Employee Attendance System
"""
        )

    else:

        print(
            "No arrival email required."
        )

        return False

    try:

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as server:

            server.starttls()

            server.login(
                EMAIL_SENDER,
                EMAIL_PASSWORD
            )

            server.send_message(
                message
            )

        print(
            f"Arrival email sent to {employee_email}"
        )

        return True

    except Exception as error:

        print(
            "Failed to send arrival email:"
        )

        print(error)

        return False


# ============================================================
# UNKNOWN PERSON SECURITY ALERT
# ============================================================

# Who receives the alert. Add SECURITY_ALERT_EMAIL=... to .env to
# send it to a different address. If it is not set, the alert goes
# to EMAIL_SENDER (the address already configured in .env).
ALERT_RECIPIENT = (
    os.getenv("SECURITY_ALERT_EMAIL")
    or EMAIL_SENDER
)


def send_unknown_person_email(
    detected_at,
    camera_name,
    match_score,
    snapshot_jpeg=None
):
    """
    Tell the head that a person who is NOT in the employee
    database was seen at the cubicle entrance.

    snapshot_jpeg : JPEG bytes of the camera frame (optional).
    """

    if not EMAIL_SENDER or not EMAIL_PASSWORD:

        print(
            "Email configuration is missing."
        )

        return False

    if not ALERT_RECIPIENT:

        print(
            "No alert recipient configured."
        )

        return False

    message = EmailMessage()

    message["From"] = EMAIL_SENDER

    message["To"] = ALERT_RECIPIENT

    message["Subject"] = (
        "SECURITY ALERT: Unknown person detected "
        "at cubicle entrance"
    )

    message.set_content(
        f"""
Hello,

This is an automated security alert from the
Employee Attendance System.

A person who is NOT registered as an employee was
detected entering the cubicle.

Detected At   : {detected_at}
Camera        : {camera_name}
Closest Match : {match_score:.2f} (below the employee
                recognition threshold)

{"A snapshot of the person is attached." if snapshot_jpeg else ""}

Please verify who this person is.

This is an automatically generated email.
Please do not reply to this email.

Regards,
Employee Attendance System
"""
    )

    if snapshot_jpeg:

        message.add_attachment(
            snapshot_jpeg,
            maintype="image",
            subtype="jpeg",
            filename="unknown_person.jpg"
        )

    try:

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as server:

            server.starttls()

            server.login(
                EMAIL_SENDER,
                EMAIL_PASSWORD
            )

            server.send_message(
                message
            )

        print(
            f"Unknown person alert sent to {ALERT_RECIPIENT}"
        )

        return True

    except Exception as error:

        print(
            "Failed to send unknown person alert:"
        )

        print(error)

        return False