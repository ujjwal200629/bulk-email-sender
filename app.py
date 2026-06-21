import streamlit as st
import pandas as pd
import threading
import os
from datetime import datetime
from dotenv import load_dotenv
from scheduler import start_scheduler, get_scheduler_info, is_scheduler_running, stop_scheduler
from email_sender import send_bulk_email

# Load environment variables from .env file
load_dotenv()

st.set_page_config(page_title="Email Automation", page_icon="📧")

# -----------------------------
# Sidebar Scheduler Status Dashboard
# -----------------------------
info = get_scheduler_info()
st.sidebar.title("⚙️ Control Panel")
if info["running"]:
    st.sidebar.success(f"🟢 Automation Active\n\n⏰ Time: {info['time']}\n\n👥 Recipients: {info['recipients']}")
    if st.sidebar.button("⏹️ Stop Automation"):
        stop_scheduler()
        st.sidebar.success("✅ Automation stopped!")
        st.rerun()
else:
    st.sidebar.info("🔴 Automation Inactive\n\nConfigure settings and start the daily scheduler.")

# -----------------------------
# Helper: Validate Time
# -----------------------------
def is_valid_time(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

# -----------------------------
# UI
# -----------------------------
st.title("📧 Automated Bulk Email Sender (FREE)")
st.write("Manual time scheduling • CSV/Excel support • Gmail only")

sender_email = st.text_input("📨 Your Gmail Address", value=os.getenv("SENDER_EMAIL", ""))
app_password = st.text_input("🔐 Gmail App Password", type="password", value=os.getenv("GMAIL_APP_PASSWORD", ""))

uploaded_file = st.file_uploader(
    "📂 Upload email file (CSV or Excel)",
    type=["csv", "xlsx"]
)

subject = st.text_input("✉️ Email Subject")
body = st.text_area("📝 Email Body", height=180)

send_time_str = st.text_input(
    "⏰ Daily Send Time (24-hour format HH:MM)",
    placeholder="e.g. 13:08 or 18:45"
)

# -----------------------------
# Utility: Read Emails
# -----------------------------
def get_recipients(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    emails = df.iloc[:, 0].dropna().astype(str).tolist()
    return emails

# -----------------------------
# SEND NOW (TEST)
# -----------------------------
if st.button("📤 Send Email NOW (Test)"):
    if not uploaded_file or not sender_email or not app_password:
        st.error("Please fill all fields and upload file.")
    else:
        recipients = get_recipients(uploaded_file)
        send_bulk_email(
            sender_email,
            app_password,
            subject,
            body,
            recipients
        )
        st.success("✅ Test email sent successfully!")

st.markdown("---")

# -----------------------------
# START DAILY AUTOMATION
# -----------------------------
if st.button("🚀 Start Daily Automation"):
    if not sender_email:
        st.error("Enter Gmail address.")
    elif not app_password:
        st.error("Enter Gmail App Password.")
    elif not uploaded_file:
        st.error("Upload CSV or Excel file.")
    elif not subject or not body:
        st.error("Enter email subject and body.")
    elif not send_time_str:
        st.error("Enter time in HH:MM format.")
    elif not is_valid_time(send_time_str):
        st.error("❌ Invalid time format. Use HH:MM (24-hour).")
    else:
        recipients = get_recipients(uploaded_file)

        scheduler_thread = threading.Thread(
            target=start_scheduler,
            args=(
                sender_email,
                app_password,
                subject,
                body,
                recipients,
                send_time_str
            ),
            daemon=True
        )
        scheduler_thread.start()

        st.success(f"✅ Emails scheduled daily at {send_time_str}")
        st.rerun()

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.info(
    "ℹ️ Important Notes:\n"
    "- Time must be in the FUTURE for same-day send\n"
    "- Laptop & terminal must stay ON\n"
    "- Internet required at send time\n"
    "- Gmail free limit ≈ 500 emails/day\n"
    "- Emails must be in FIRST column only"
)
