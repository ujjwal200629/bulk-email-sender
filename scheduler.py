import schedule
import time
import threading
from email_sender import send_bulk_email

# Global reference to stop event and lock for thread safety
_scheduler_stop_event = None
_scheduler_lock = threading.Lock()
_scheduled_time = None
_recipient_count = 0

def is_scheduler_running():
    global _scheduler_stop_event
    return _scheduler_stop_event is not None and not _scheduler_stop_event.is_set()

def stop_scheduler():
    global _scheduler_stop_event
    with _scheduler_lock:
        if _scheduler_stop_event is not None:
            _scheduler_stop_event.set()
            print("[SCHEDULER] Stop requested.")

def get_scheduler_info():
    global _scheduled_time, _recipient_count
    return {
        "running": is_scheduler_running(),
        "time": _scheduled_time,
        "recipients": _recipient_count
    }


def start_scheduler(email, password, subject, body, recipients, send_time):
    global _scheduler_stop_event, _scheduled_time, _recipient_count
    
    with _scheduler_lock:
        if _scheduler_stop_event is not None:
            print("[SCHEDULER] Stopping previous scheduler thread...")
            _scheduler_stop_event.set()
        _scheduler_stop_event = threading.Event()
        stop_event = _scheduler_stop_event
        _scheduled_time = send_time
        _recipient_count = len(recipients)

    print(f"[SCHEDULER STARTED] {time.strftime('%H:%M:%S')}")
    print(f"[EMAIL TIME] {send_time}")

    local_scheduler = schedule.Scheduler()
    local_scheduler.every().day.at(send_time).do(
        send_bulk_email,
        email,
        password,
        subject,
        body,
        recipients
    )

    while not stop_event.is_set():
        local_scheduler.run_pending()
        time.sleep(1)
    
    print("[SCHEDULER] Old scheduler thread stopped cleanly.")


