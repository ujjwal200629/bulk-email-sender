import smtplib
import time
import re
from email.message import EmailMessage


def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)


def send_bulk_email(sender, password, subject, body, recipients):
    sent = 0
    failed = 0

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)

            for email in recipients:
                email = email.strip()
                if not is_valid_email(email):
                    print(f" Invalid email skipped: {email}")
                    failed += 1
                    continue

                try:
                    msg = EmailMessage()
                    msg["From"] = sender
                    msg["To"] = email
                    msg["Subject"] = subject
                    msg.set_content(body)

                    server.send_message(msg)
                    sent += 1
                    print(f"[SUCCESS] Successfully sent email to {email}")
                    time.sleep(3)  # spam safety
                except Exception as e:
                    failed += 1
                    print(f"[WARNING] Failed to send to {email}: {e}")
    except Exception as e:
        print(f"[ERROR] SMTP Connection/Authentication failed: {e}")
        failed += len(recipients) - sent - failed


    print(f"Emails sent: {sent}")
    print(f" Emails failed/skipped: {failed}")

