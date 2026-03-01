import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from todo_service import get_tasks, mark_reminder_sent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RECIPIENT_EMAIL = "yafi3155816@gmail.com"


def send_email_reminder(task):
    """שליחת מייל תזכורת למשימה"""
    sender_email = os.getenv('GMAIL_USER')
    sender_password = os.getenv('GMAIL_PASSWORD')
    
    if not sender_email or not sender_password:
        logger.error("Gmail credentials not configured")
        return False
    
    subject = f"תזכורת: {task['title']}"
    body = f"""
    שלום,
    
    זוהי תזכורת למשימה שלך:
    
    כותרת: {task['title']}
    תיאור: {task['description']}
    תאריך יעד: {datetime.fromisoformat(task['due_date']).strftime('%d/%m/%Y %H:%M')}
    
    המשימה צריכה להיות מושלמת בעוד שעתיים!
    
    בהצלחה,
    מערכת ניהול המשימות
    """
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        logger.info(f"Email sent for task {task['id']}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


def check_and_send_reminders():
    """בודק משימות ושולח תזכורות לפי הצורך"""
    tasks = get_tasks()['tasks']
    now = datetime.now()
    
    for task in tasks:
        if task['completed'] or task['reminder_sent'] or not task['due_date']:
            continue
        
        try:
            due_date = datetime.fromisoformat(task['due_date'])
            time_until_due = due_date - now
            
            # שליחה שעתיים לפני
            if timedelta(hours=1, minutes=50) <= time_until_due <= timedelta(hours=2, minutes=10):
                if send_email_reminder(task):
                    mark_reminder_sent(task['id'])
                    logger.info(f"Reminder sent for task {task['id']}")
        except Exception as e:
            logger.error(f"Error processing task {task['id']}: {e}")
