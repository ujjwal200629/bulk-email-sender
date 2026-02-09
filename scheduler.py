import schedule
import time
from email_sender import send_bulk_email

def start_scheduler(email, password, subject, body, recipients, send_time):
    print(f"[SCHEDULER STARTED] {time.strftime('%H:%M:%S')}")
    print(f"[EMAIL TIME] {send_time}")

    schedule.every().day.at(send_time).do(
        send_bulk_email,
        email,
        password,
        subject,
        body,
        recipients
    )

    while True:
        schedule.run_pending()
        time.sleep(10)
