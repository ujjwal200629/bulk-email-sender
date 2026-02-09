import smtplib
import time
import re
from email.message import EmailMessage


def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


def send_bulk_email(sender, password, subject, body, recipients):
    msg = EmailMessage()
    msg["From"] = sender
    msg["Subject"] = subject
    msg.set_content(body)

    sent = 0
    failed = 0

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)

        for email in recipients:
            if not is_valid_email(email):
                print(f" Invalid email skipped: {email}")
                failed += 1
                continue

            try:
                msg["To"] = email
                server.send_message(msg)
                sent += 1
                time.sleep(3)  # spam safety
                del msg["To"]
            except Exception as e:
                failed += 1
                print(f"⚠️ Failed to send to {email}: {e}")

    print(f"Emails sent: {sent}")
    print(f" Emails failed/skipped: {failed}")
