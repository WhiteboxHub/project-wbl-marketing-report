import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

def send_report_email(html_content):
    """
    Sends the HTML report to the configured recipient list using SMTP and App Password.
    Handles both Port 587 (TLS) and Port 465 (SSL) automatically.
    """
    smtp_server = os.getenv("REPORT_SMTP_SERVER")
    smtp_port = int(os.getenv("REPORT_SMTP_PORT", 587))
    email_user = os.getenv("REPORT_EMAIL_USER")
    email_pass = os.getenv("REPORT_EMAIL_PASS") 
    recipients_raw = os.getenv("MARKETING_REPORT_RECIPIENTS", "")
    
    if not all([smtp_server, email_user, email_pass, recipients_raw]):
        logger.error("Email configuration missing in .env")
        return False
        
    recipients = [r.strip() for r in recipients_raw.split(",") if r.strip()]
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"WBL Daily Marketing Report - {formatdate(localtime=False)}"
    msg['From'] = f"WBL Marketing <{email_user}>"
    msg['To'] = ", ".join(recipients)
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = make_msgid()

    text_content = "Please use an HTML compatible email client to view the Marketing Report."
    
    part1 = MIMEText(text_content, 'plain')
    part2 = MIMEText(html_content, 'html')
    
    msg.attach(part1)
    msg.attach(part2)
    
    try:
        logger.info(f"Attempting to send via {smtp_server}:{smtp_port}...")
        
        # Logic for SSL (465)
        if smtp_port == 465:
            logger.info("Using SMTP_SSL for port 465...")
            with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=60) as server:
                server.login(email_user, email_pass)
                server.sendmail(email_user, recipients, msg.as_string())
        
        # Logic for TLS (587 or others)
        else:
            logger.info(f"Using standard SMTP for port {smtp_port}...")
            with smtplib.SMTP(smtp_server, smtp_port, timeout=60) as server:
                server.starttls()
                server.login(email_user, email_pass)
                server.sendmail(email_user, recipients, msg.as_string())
                
        logger.info("Email sent successfully!")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {type(e).__name__} - {e}")
        return False
