import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Standardized URL resolution
USE_LOCAL = os.getenv("USE_LOCAL_API", "true").lower() == "true"
BASE_URL = os.getenv("LOCAL_WBL_API_URL" if USE_LOCAL else "WBL_API_URL")

# API Key
API_KEY = os.getenv("REPORT_API_KEY")

def get_full_url(endpoint: str) -> str:
    """Helper to construct the full URL for any API endpoint."""
    base = BASE_URL.rstrip('/')
    ext = endpoint.lstrip('/')
    return f"{base}/{ext}"

def fetch_report_data():
    """
    Fetches raw marketing data from the Backend API using the unified URL format.
    """
    if not API_KEY:
        logger.error("REPORT_API_KEY not configured in .env")
        return None
        
    try:
        # Endpoint for the data is report-data/
        url = get_full_url("report-data/")
        logger.info(f"Fetching data from {url}...")
        
        response = requests.get(
            url, 
            headers={"X-API-KEY": API_KEY},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch report data: {e}")
        return None

def get_due_schedules():
    """
    Polls the Backend Orchestrator for any due marketing reports.
    """
    try:
        url = get_full_url("orchestrator/schedules/due")
        response = requests.get(url, headers={"X-API-KEY": API_KEY}, timeout=15)
        response.raise_for_status()
        schedules = response.json()
        
        target_key = os.getenv("WORKFLOW_KEY", "weekly_marketing_report")
        return [s for s in schedules if s.get('workflow_key') == target_key]
    except Exception as e:
        logger.error(f"Failed to check orchestrator: {e}")
        return []

def lock_schedule(schedule_id):
    """
    Attempts to atomically claim a schedule so no one else runs it.
    """
    try:
        url = get_full_url(f"orchestrator/schedules/{schedule_id}/lock")
        response = requests.post(url, headers={"X-API-KEY": API_KEY}, timeout=15)
        return response.status_code == 200
    except Exception as e:
        logger.error(f"Failed to lock schedule {schedule_id}: {e}")
        return False

def create_log(workflow_id, schedule_id, run_id, status, metadata=None):
    """
    Sends execution logs back to the Backend database.
    """
    try:
        url = get_full_url("orchestrator/logs")
        payload = {
            "workflow_id": workflow_id,
            "schedule_id": schedule_id,
            "run_id": run_id,
            "status": status,
            "execution_metadata": metadata or {}
        }
        requests.post(url, json=payload, headers={"X-API-KEY": API_KEY}, timeout=15)
    except Exception as e:
        logger.error(f"Failed to update logs: {e}")
