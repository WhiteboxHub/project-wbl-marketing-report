import logging
import time
import os
from datetime import datetime
from app.api_client import fetch_report_data, get_due_schedules, lock_schedule, create_log
from app.report_formatter import format_report_html, create_report_pdf
from app.email_service import send_report_email

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("WBLReportRunner")

def validate_setup():
    """Validates configuration before starting."""
    required = [
        "REPORT_EMAIL_USER", "REPORT_EMAIL_PASS", 
        "MARKETING_REPORT_RECIPIENTS", "REPORT_SMTP_SERVER",
        "REPORT_API_KEY", "WORKFLOW_KEY"
    ]
    missing = [r for r in required if not os.getenv(r)]
    if missing:
        logger.error(f"Missing required configuration: {missing}")
        return False
    return True

def run_orchestrated_report():
    """
    Checks if a report is due in the Backend and executes it.
    """
    if os.getenv("VALIDATE_SECRETS_AT_STARTUP", "true").lower() == "true":
        if not validate_setup():
            return

    logger.info("--- Checking Orchestrator for Due Reports ---")
    
    # 1. Ask Backend: "Is any report due?"
    due_schedules = get_due_schedules()
    
    if not due_schedules:
        logger.info("No due marketing reports found in Scheduler.")
        return

    # Use Workflow ID from .env if available, fallback to 11
    wf_id_config = int(os.getenv("WORKFLOW_ID", 11))

    for schedule in due_schedules:
        schedule_id = schedule.get('id')
        workflow_id = schedule.get('workflow_id', wf_id_config)
        run_id = f"external_run_{int(time.time())}"
        
        logger.info(f"Found due schedule: {schedule_id}. Attempting to claim...")
        
        if os.getenv("DRY_RUN", "false").lower() == "true":
            logger.info("DRY_RUN active. Skipping actual execution.")
            continue

        # 2. Claim the task (Atomic Lock)
        if not lock_schedule(schedule_id):
            logger.warning(f"Failed to claim schedule {schedule_id}. Another worker might have taken it.")
            continue

        # 3. Inform Backend we are starting
        create_log(workflow_id, schedule_id, run_id, "running")

        try:
            # 4. Fetch data via API
            data = fetch_report_data()
            if not data:
                raise Exception("Could not get data from API.")

            # 5. Format HTML and generate PDF
            html_content = format_report_html(data)
            pdf_content = create_report_pdf(data)

            # 6. Dispatch Email
            send_result = send_report_email(html_content, pdf_content)
            if not send_result:
                raise Exception("Email delivery failed.")

            # 7. Success! Log it back
            logger.info("--- Report Execution Successful ---")
            create_log(workflow_id, schedule_id, run_id, "success", {"message": "Professional dispatch complete"})

        except Exception as e:
            logger.error(f"Report Execution Failed: {e}")
            create_log(workflow_id, schedule_id, run_id, "failed", {"error": str(e)})

if __name__ == "__main__":
    run_orchestrated_report()
