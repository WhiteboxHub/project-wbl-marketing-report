from jinja2 import Template
from datetime import datetime, timezone

def format_report_html(data):
    """
    Formats the raw JSON data into a professional dashboard exactly matching the Backend template.
    """
    if not data or data.get("status") != "success":
        return None
        
    candidates = data.get("candidates", [])
    summary = data.get("summary", {})
    
    # Professional Template HTML
    template_html = """
    <html>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f3f4f6; margin: 0; padding: 40px 20px;">
        <div style="max-width: 950px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); overflow: hidden;">
            
            <!-- Header -->
            <div style="background-color: #1f2937; color: #ffffff; padding: 30px; text-align: center;">
                <h1 style="margin: 0; font-size: 24px; font-weight: 600; letter-spacing: 0.5px;">Weekly Marketing Report</h1>
                <p style="margin: 10px 0 0 0; font-size: 14px; color: #9ca3af;">{{ summary.start_date }} &mdash; {{ summary.end_date }}</p>
            </div>
            
            <div style="padding: 30px;">
                <!-- Summary Boxes -->
                <table width="100%" cellpadding="0" cellspacing="5" style="margin-bottom: 30px;">
                    <tr>
                        <td width="25%" style="background-color: #f9fafb; padding: 20px 10px; text-align: center; border-radius: 6px; border: 1px solid #e5e7eb;">
                            <div style="font-size: 28px; font-weight: bold; color: #3b82f6; margin-bottom: 4px;">{{ summary.total_candidates }}</div>
                            <div style="font-size: 11px; color: #6b7280; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Candidates</div>
                        </td>
                        <td width="25%" style="background-color: #f9fafb; padding: 20px 10px; text-align: center; border-radius: 6px; border: 1px solid #e5e7eb;">
                            <div style="font-size: 28px; font-weight: bold; color: #10b981; margin-bottom: 4px;">{{ summary.total_interviews }}</div>
                            <div style="font-size: 11px; color: #6b7280; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Interviews</div>
                        </td>
                        <td width="25%" style="background-color: #f9fafb; padding: 20px 10px; text-align: center; border-radius: 6px; border: 1px solid #e5e7eb;">
                            <div style="font-size: 28px; font-weight: bold; color: #f59e0b; margin-bottom: 4px;">{{ summary.total_clicks }}</div>
                            <div style="font-size: 11px; color: #6b7280; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Job Clicks</div>
                        </td>
                        <td width="25%" style="background-color: #f9fafb; padding: 15px 10px; text-align: left; border-radius: 6px; border: 1px solid #e5e7eb; vertical-align: top;">
                            <div style="font-size: 11px; font-weight: 600; color: #8b5cf6; margin-bottom: 6px; text-align: center; text-transform: uppercase; letter-spacing: 0.5px;">Daily Automations</div>
                            <ul style="font-size: 10px; color: #4b5563; margin: 0; padding-left: 20px; line-height: 1.4;">
                                <li style="margin-bottom: 2px;">LinkedIn</li>
                                <li style="margin-bottom: 2px;">Vendor Mass Emails</li>
                                <li>Manual Applications</li>
                            </ul>
                        </td>
                    </tr>
                </table>

                <div style="overflow-x: auto;">
                    <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse: separate; border-spacing: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 10px; border: 1px solid #e2e8f0; border-radius: 12px 12px 0 0;">
                        <thead>
                            <tr style="color: #ffffff; font-weight: 700;">
                                <th rowspan="2" style="padding: 15px 10px; text-align: center; vertical-align: middle; background-color: #3b5998; border-right: 1px solid #ffffff; width: 14%; border-top-left-radius: 11px; font-size: 11px;">Candidate</th>
                                <th colspan="4" style="padding: 12px; text-align: center; background-color: #4d71bb; border-right: 1px solid #ffffff; text-transform: uppercase; letter-spacing: 1.5px; font-size: 11px;">APPLICATIONS</th>
                                <th colspan="4" style="padding: 12px; text-align: center; background-color: #6d8acb; border-right: 1px solid #ffffff; text-transform: uppercase; letter-spacing: 1.5px; font-size: 11px;">INTERVIEWS</th>
                                <th rowspan="2" style="padding: 15px 10px; text-align: center; vertical-align: middle; background-color: #38ada9; border-right: 1px solid #ffffff; width: 6%; font-size: 11px;">Total</th>
                                <th colspan="3" style="padding: 12px; text-align: center; background-color: #8da3dc; border-right: 1px solid #ffffff; text-transform: uppercase; letter-spacing: 1.5px; font-size: 11px; border-top-right-radius: 11px;">FEEDBACK</th>
                            </tr>
                            <tr style="background-color: #f0f4f8; color: #334e81; font-weight: 700; text-transform: uppercase; font-size: 9px;">
                                <th style="padding: 12px 4px; text-align: center; border-right: 1px solid #e2e8f0; line-height: 1.3;">EMAIL<br>OUTREACH</th>
                                <th style="padding: 12px 4px; text-align: center; border-right: 1px solid #e2e8f0; line-height: 1.3;">LINKEDIN<br>EASYAPPLY</th>
                                <th style="padding: 12px 4px; text-align: center; border-right: 1px solid #e2e8f0; line-height: 1.3;">JOB PORTAL<br>AUTOMATIONS</th>
                                <th style="padding: 12px 4px; text-align: center; border-right: 1px solid #e2e8f0; line-height: 1.3;">JOB<br>LISTINGS<br>CLICKS</th>
                                <th style="padding: 12px 4px; text-align: center; border-right: 1px solid #e2e8f0; line-height: 1.3;">ASSESSMENTS</th>
                                <th style="padding: 12px 4px; text-align: center; border-right: 1px solid #e2e8f0; line-height: 1.3;">RECRUITER</th>
                                <th style="padding: 12px 4px; text-align: center; border-right: 1px solid #e2e8f0; line-height: 1.3;">TECHNICAL</th>
                                <th style="padding: 12px 4px; text-align: center; border-right: 1px solid #e2e8f0; line-height: 1.3;">ONSITE</th>
                                <th style="padding: 12px 4px; text-align: center; border-right: 1px solid #e2e8f0; line-height: 1.3; color: #16a34a;">POSITIVE</th>
                                <th style="padding: 12px 4px; text-align: center; border-right: 1px solid #e2e8f0; line-height: 1.3; color: #ef4444;">NEGATIVE</th>
                                <th style="padding: 12px 4px; text-align: center; border-right: 1px solid #e2e8f0; line-height: 1.3; color: #d97706;">PENDING</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for c in candidates %}
                            <tr style="background-color: {{ '#ffffff' if loop.index0 % 2 == 0 else '#f8fafc' }};">
                                <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; color: #1e293b; font-weight: 600;">{{ c.full_name }}</td>
                                <td style="padding: 12px 8px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; text-align: center; color: #334155; font-weight: bold;">{{ c.outreach_count or '-' }}</td>
                                <td style="padding: 12px 8px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; text-align: center; color: #334155; font-weight: bold;">{{ c.linkedin_easy_apply_count or '-' }}</td>
                                <td style="padding: 12px 8px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; text-align: center; color: #334155; font-weight: bold;">{{ c.job_portal_automation_count or '-' }}</td>
                                <td style="padding: 12px 8px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; text-align: center; color: #ea580c; font-weight: 700;">{{ c.job_clicks or '-' }}</td>
                                <td style="padding: 12px 8px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; text-align: center; color: #334155; font-weight: bold;">{{ c.assessment_count or '-' }}</td>
                                <td style="padding: 12px 8px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; text-align: center; color: #334155; font-weight: bold;">{{ c.recruiter_call_count or '-' }}</td>
                                <td style="padding: 12px 8px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; text-align: center; color: #334155; font-weight: bold;">{{ c.technical_count or '-' }}</td>
                                <td style="padding: 12px 8px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; text-align: center; color: #334155; font-weight: bold;">{{ c.onsite_count or '-' }}</td>
                                <td style="padding: 12px 8px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; text-align: center; color: #0f172a; font-weight: 800; background-color: #ecfdf5;">{{ c.total_interviews or '0' }}</td>
                                <td style="padding: 12px 8px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; text-align: center; color: #16a34a; font-weight: bold;">{{ c.feedback_positive or '-' }}</td>
                                <td style="padding: 12px 8px; border-bottom: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; text-align: center; color: #ef4444; font-weight: bold;">{{ c.feedback_negative or '-' }}</td>
                                <td style="padding: 12px 8px; border-bottom: 1px solid #e2e8f0; text-align: center; color: #d97706; font-weight: bold;">{{ c.feedback_pending or '-' }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <!-- Footer -->
            <div style="background-color: #f9fafb; padding: 20px; text-align: center; border-top: 1px solid #e5e7eb;">
                <p style="margin: 0; font-size: 11px; color: #9ca3af;">Automated Daily Marketing Report</p>
                <p style="margin: 4px 0 0 0; font-size: 11px; color: #9ca3af;">Generated on {{ now_str }} UTC</p>
            </div>
            
        </div>
    </body>
    </html>
    """
    
    now_str = datetime.now(timezone.utc).strftime('%B %d, %Y at %H:%M')
    template = Template(template_html)
    return template.render(
        candidates=candidates, 
        summary=summary,
        now_str=now_str
    )
