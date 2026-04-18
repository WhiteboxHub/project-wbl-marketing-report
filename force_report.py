import os
from dotenv import load_dotenv
from app.api_client import fetch_report_data
from app.report_formatter import format_report_html
from app.email_service import send_report_email

load_dotenv()

def preview_and_send():
    print("--- Running Full Report Test ---")
    
    # 1. Fetch data
    print("Step 1: Fetching data from local backend...")
    data = fetch_report_data()
    
    if not data or data.get("status") != "success":
        print("Error: Could not get data. Make sure your backend is running!")
        return

    # 2. Format the HTML
    print("Step 2: Formatting report HTML...")
    html_content = format_report_html(data)

    # 3. Save to a local file (for you to check)
    with open("preview_report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Step 3: Saved preview to preview_report.html")

    # 4. SEND THE EMAIL (Bypassing the scheduler)
    print("Step 4: Attempting to send email...")
    success = send_report_email(html_content)
    
    if success:
        print("\nSUCCESS! The email has been sent and the preview file is ready.")
    else:
        print("\nFAILED to send email. Check your SMTP settings in .env.")

if __name__ == "__main__":
    preview_and_send()
