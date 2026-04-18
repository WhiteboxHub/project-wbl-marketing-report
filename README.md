# WBL Marketing Report Service

A standalone service that automatically generates and emails the **Daily Marketing Report** for Whitebox Learning candidates.

---

## How It Works

This service connects to the **WBL Backend API** to fetch live candidate data, formats it into a professional HTML email, and dispatches it to the configured recipients.

```
WBL Backend (Workflow Scheduler)
        │
        │  Marks "weekly_marketing_report" as DUE at 8:00 AM PST (15:00 UTC)
        ▼
wbl-marketing-report (main.py — polling every 5 minutes)
        │
        │  Sees schedule is DUE → Claims it (atomic lock, no duplicates)
        ▼
Fetches data from Production API  →  Formats HTML  →  Sends Email
        │
        └─ Logs "success" back to WBL Backend Workflow Logs ✅
```

---

## Report Contents

### Applications (Yesterday — 1-Day Window)
| Column | Data Source |
|---|---|
| Email Outreach | `automation_workflow_log` (workflow IDs: 1, 3, 6, 10) |
| LinkedIn Easy Apply | `job_activity_log` (job types containing "Linkedin") |
| Job Portal Automations | `automation_workflow_log` (workflow IDs: 7, 9) |
| Job Listings Clicks | `job_link_clicks` + `authuser` tables |

### Interviews & Feedback (Last 7 Days)
| Column | Data Source |
|---|---|
| Assessments, Recruiter, Technical, Onsite | `candidate_interview` table |
| Feedback (Positive / Negative / Pending) | `candidate_interview` table |

### Candidates
Only **active** candidates from the `candidate_marketing` table are included.

---

## Repository Structure

```
wbl-marketing-report/
├── main.py                  # Production: Polling service (runs continuously)
├── force_report.py          # Testing: Manual trigger (sends report immediately)
├── requirements.txt         # Python dependencies
├── .env                     # Configuration (credentials & API URL)
├── .env.example             # Template for .env setup
└── app/
    ├── api_client.py        # Fetches data from WBL Backend API
    ├── report_formatter.py  # Formats raw data into HTML email
    └── email_service.py     # Sends the email via SMTP
```

---

## Setup

### 1. Clone the repository
```bash
git clone <repo-url>
cd wbl-marketing-report
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure the `.env` file
Copy the example file and fill in your values:
```bash
cp .env.example .env
```

Edit `.env`:
```env
# API Key (must match REPORT_API_KEY in WBL Backend .env)
REPORT_API_KEY=wbl_marketing_report

# Set to false for production, true for local testing
USE_LOCAL_API=false
WBL_API_URL=https://api.whitebox-learning.com/api

# For local testing only:
# USE_LOCAL_API=true
# LOCAL_WBL_API_URL=http://localhost:8000/api

# Email credentials (Gmail App Password)
REPORT_EMAIL_USER=sindhu@whitebox-learning.com
REPORT_EMAIL_PASS=your_app_password_here
MARKETING_REPORT_RECIPIENTS=recipient1@email.com,recipient2@email.com
REPORT_SMTP_PORT=465
REPORT_SMTP_SERVER=smtp.gmail.com

# Workflow Configuration (must match WBL Backend database)
WORKFLOW_KEY=weekly_marketing_report
WORKFLOW_ID=11
```

---

## Usage

### Production (Automatic Daily Report)
Start the polling service **once** and leave it running:
```bash
python main.py
```
- Polls the WBL Backend scheduler every **5 minutes**
- Automatically sends the report when the backend marks it as due (**8:00 AM PST**)
- Logs success/failure back to the WBL Backend workflow logs
- Runs **forever** — one report per day, no duplicates

### Local Testing (Manual Trigger)
To immediately generate and send a test report:
```bash
python force_report.py
```
- Bypasses the scheduler completely
- Sends the report instantly
- Saves a preview to `preview_report.html` for visual inspection
- Requires the local WBL Backend to be running (`USE_LOCAL_API=true`)

---

## Scheduling Details

| Setting | Value |
|---|---|
| Schedule time | 8:00 AM PST / 15:00 UTC |
| Frequency | Daily |
| Duplicate protection | Atomic DB lock (only one worker can claim the schedule) |
| Retry on failure | Schedule stays "due" until successfully claimed |

> **Note:** The 8:00 AM PST schedule is stored in the WBL Backend database. This service simply polls the backend and fires when instructed.

---

## Switching Between Local and Production

| Environment | `.env` setting |
|---|---|
| **Local Testing** | `USE_LOCAL_API=true` + `LOCAL_WBL_API_URL=http://localhost:8000/api` |
| **Production** | `USE_LOCAL_API=false` + `WBL_API_URL=https://api.whitebox-learning.com/api` |

---

## Dependencies

The WBL Backend must have:
- `REPORT_API_KEY` set in its `.env` (must match this repo's `REPORT_API_KEY`)
- The `weekly_marketing_report` workflow enabled in the database
- The `/api/report-data/` endpoint active (`fapi/api/routes/report_data.py`)
